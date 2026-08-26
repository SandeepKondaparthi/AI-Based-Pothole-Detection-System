"""
Repair action routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
from app.config.database import get_database
from app.models.repair import RepairActionCreate, RepairActionResponse, RepairActionUpdate, RepairActionInDB
from app.models.user import TokenData
from app.utils.auth import require_authority

router = APIRouter(prefix="/repairs", tags=["Repair Actions"])


@router.post("", response_model=RepairActionResponse, status_code=status.HTTP_201_CREATED)
async def create_repair_action(
    repair_data: RepairActionCreate,
    current_user: TokenData = Depends(require_authority),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a new repair action for a risk zone (Authority only)

    - **zone_id**: ID of the risk zone
    - **assigned_department**: Department responsible for repair
    - **repair_status**: Initial status (default: pending)
    """
    # Validate zone exists
    if not ObjectId.is_valid(repair_data.zone_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid zone ID"
        )

    zone = await db.risk_zones.find_one({"_id": ObjectId(repair_data.zone_id)})
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found"
        )

    # Create repair action
    repair = RepairActionInDB(
        zone_id=ObjectId(repair_data.zone_id),
        assigned_department=repair_data.assigned_department,
        repair_status=repair_data.repair_status
    )

    # Insert into database
    result = await db.repair_actions.insert_one(repair.dict(by_alias=True, exclude={"id"}))
    repair.id = result.inserted_id

    return RepairActionResponse(
        _id=str(repair.id),
        zone_id=str(repair.zone_id),
        **repair.dict(exclude={"id", "zone_id"})
    )


@router.get("", response_model=List[RepairActionResponse])
async def get_repair_actions(
    status_filter: Optional[str] = None,
    current_user: TokenData = Depends(require_authority),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get all repair actions (Authority only)

    - **status**: Filter by repair status (pending, in_progress, completed)
    """
    # Build query
    query = {}
    if status_filter:
        if status_filter not in ["pending", "in_progress", "completed"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status filter"
            )
        query["repair_status"] = status_filter

    # Fetch repairs
    cursor = db.repair_actions.find(query).sort("start_date", -1)
    repairs = await cursor.to_list(length=None)

    # Convert to response models
    return [
        RepairActionResponse(
            _id=str(repair["_id"]),
            zone_id=str(repair["zone_id"]),
            assigned_department=repair["assigned_department"],
            repair_status=repair["repair_status"],
            start_date=repair["start_date"],
            end_date=repair.get("end_date")
        )
        for repair in repairs
    ]


@router.get("/{repair_id}", response_model=RepairActionResponse)
async def get_repair_action(
    repair_id: str,
    current_user: TokenData = Depends(require_authority),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get specific repair action by ID (Authority only)"""
    if not ObjectId.is_valid(repair_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid repair ID"
        )

    repair = await db.repair_actions.find_one({"_id": ObjectId(repair_id)})

    if not repair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repair action not found"
        )

    return RepairActionResponse(
        _id=str(repair["_id"]),
        zone_id=str(repair["zone_id"]),
        **{k: v for k, v in repair.items() if k not in ["_id", "zone_id"]}
    )


@router.put("/{repair_id}", response_model=RepairActionResponse)
async def update_repair_action(
    repair_id: str,
    update_data: RepairActionUpdate,
    current_user: TokenData = Depends(require_authority),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Update repair action status (Authority only)

    - **repair_status**: New status (pending, in_progress, completed)
    - **assigned_department**: Update responsible department (optional)
    """
    if not ObjectId.is_valid(repair_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid repair ID"
        )

    # Build update document
    update_doc = {"repair_status": update_data.repair_status}

    if update_data.assigned_department:
        update_doc["assigned_department"] = update_data.assigned_department

    # Set end_date if status is completed
    if update_data.repair_status == "completed":
        update_doc["end_date"] = datetime.utcnow()

    # Update repair
    result = await db.repair_actions.find_one_and_update(
        {"_id": ObjectId(repair_id)},
        {"$set": update_doc},
        return_document=True
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repair action not found"
        )

    return RepairActionResponse(
        _id=str(result["_id"]),
        zone_id=str(result["zone_id"]),
        **{k: v for k, v in result.items() if k not in ["_id", "zone_id"]}
    )
