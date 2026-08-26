"""
Pothole report routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import h3
from typing import List, Optional
from app.config.database import get_database
from app.models.report import ReportCreate, ReportResponse, ReportInDB, ReportStatusUpdate, LocationModel
from app.models.user import TokenData
from app.utils.auth import get_current_user, require_authority
from app.services.image_service import IMAGE_SERVICE
from app.services.ai_verification_service import ai_service
from app.models.verification import VerificationInDB

router = APIRouter(prefix="/reports", tags=["Pothole Reports"])


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    description: Optional[str] = Form(None),
    current_user: TokenData = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Submit a new pothole report

    - **image**: Image file (JPEG/PNG)
    - **latitude**: GPS latitude (-90 to 90)
    - **longitude**: GPS longitude (-180 to 180)
    - **description**: Optional description or landmarks
    """
    # Save uploaded image
    image_path = await IMAGE_SERVICE.save_image(image)

    # Create location model
    location = LocationModel(latitude=latitude, longitude=longitude)

    # Pre-generate ID for AI service
    report_id = ObjectId()

    # Calculate H3 index (Resolution 9 ~0.1 km2)
    h3_index = h3.latlng_to_cell(latitude, longitude, 9)

    # Create report model
    report = ReportInDB(
        _id=report_id,
        user_id=ObjectId(current_user.user_id),
        image_path=image_path,
        location=location,
        h3_index=h3_index,
        description=description,
        status="pending"
    )

    # Run AI verification
    verification = await ai_service.verify_pothole(image_path, report_id)

    # Prepare report data
    report_dict = report.dict(by_alias=True)
    report_dict["ai_confidence"] = verification.confidence_score
    report_dict["ai_verified"] = verification.is_pothole

    # Auto-verify/reject based on AI
    if verification.is_pothole and ai_service.should_auto_verify(verification.confidence_score):
        report_dict["status"] = "verified"
        report.status = "verified"
    elif not verification.is_pothole:
        report_dict["status"] = "rejected"
        report.status = "rejected"

    # Save to database
    await db.pothole_reports.insert_one(report_dict)

    # Also save to verification history
    await db.image_verification.insert_one(verification.dict(by_alias=True, exclude={"id"}))

    # Return response
    return ReportResponse(
        _id=str(report_id),
        user_id=str(report.user_id),
        status=report.status,
        ai_confidence=verification.confidence_score,
        ai_verified=verification.is_pothole,
        **report.dict(exclude={"id", "user_id", "status"})
    )


@router.get("", response_model=List[ReportResponse])
async def get_reports(
    status_filter: Optional[str] = None,
    limit: int = 100,
    skip: int = 0,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get list of pothole reports

    - **status**: Filter by status (pending, verified, rejected)
    - **limit**: Maximum number of results (default 100)
    - **skip**: Number of results to skip for pagination

    Regular users see only their own reports.
    Authorities see all reports.
    """
    # Build query
    query = {}

    # Regular users can only see their own reports
    if current_user.role == "user":
        query["user_id"] = ObjectId(current_user.user_id)

    # Apply status filter if provided
    if status_filter:
        if status_filter not in ["pending", "verified", "rejected"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status filter"
            )
        query["status"] = status_filter

    # Build aggregation pipeline
    pipeline = [
        {"$match": query},
        {"$lookup": {
            "from": "image_verification",
            "localField": "_id",
            "foreignField": "report_id",
            "as": "verification_data"
        }},
        {"$addFields": {
            "ai_confidence": {
                "$ifNull": ["$ai_confidence", {"$arrayElemAt": ["$verification_data.confidence_score", 0]}]
            },
            "ai_verified": {
                "$ifNull": ["$ai_verified", {"$arrayElemAt": ["$verification_data.is_pothole", 0]}]
            }
        }},
        {"$sort": {"report_date": -1}},
        {"$skip": skip},
        {"$limit": limit}
    ]

    # Fetch reports
    cursor = db.pothole_reports.aggregate(pipeline)
    reports = await cursor.to_list(length=limit)

    # Convert to response models
    return [
        ReportResponse(
            _id=str(report["_id"]),
            user_id=str(report["user_id"]),
            image_path=report["image_path"],
            location=report["location"],
            h3_index=report.get("h3_index"),
            description=report.get("description"),
            status=report["status"],
            report_date=report["report_date"],
            ai_confidence=report.get("ai_confidence"),
            ai_verified=report.get("ai_verified")
        )
        for report in reports
    ]


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get specific report by ID"""
    # Validate ObjectId
    if not ObjectId.is_valid(report_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report ID"
        )

    # Fetch report with verification data using aggregation
    pipeline = [
        {"$match": {"_id": ObjectId(report_id)}},
        {"$lookup": {
            "from": "image_verification",
            "localField": "_id",
            "foreignField": "report_id",
            "as": "verification_data"
        }},
        {"$addFields": {
            "ai_confidence": {
                "$ifNull": ["$ai_confidence", {"$arrayElemAt": ["$verification_data.confidence_score", 0]}]
            },
            "ai_verified": {
                "$ifNull": ["$ai_verified", {"$arrayElemAt": ["$verification_data.is_pothole", 0]}]
            }
        }}
    ]

    cursor = db.pothole_reports.aggregate(pipeline)
    results = await cursor.to_list(length=1)
    report = results[0] if results else None

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    # Check authorization (users can only see their own)
    if current_user.role == "user" and str(report["user_id"]) != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this report"
        )

    return ReportResponse(
        _id=str(report["_id"]),
        user_id=str(report["user_id"]),
        image_path=report["image_path"],
        location=report["location"],
        h3_index=report.get("h3_index"),
        description=report.get("description"),
        status=report["status"],
        report_date=report["report_date"],
        ai_confidence=report.get("ai_confidence"),
        ai_verified=report.get("ai_verified")
    )


@router.put("/{report_id}/status", response_model=ReportResponse)
async def update_report_status(
    report_id: str,
    status_update: ReportStatusUpdate,
    current_user: TokenData = Depends(require_authority),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Update report status (Authority only)

    - **status**: New status (pending, verified, rejected)
    - **notes**: Optional notes about the status change
    """
    # Validate ObjectId
    if not ObjectId.is_valid(report_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report ID"
        )

    # Update status
    result = await db.pothole_reports.find_one_and_update(
        {"_id": ObjectId(report_id)},
        {"$set": {"status": status_update.status}},
        return_document=True
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return ReportResponse(
        _id=str(result["_id"]),
        user_id=str(result["user_id"]),
        **{k: v for k, v in result.items() if k not in ["_id", "user_id"]}
    )
