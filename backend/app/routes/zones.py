"""
Risk zone routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List
from app.config.database import get_database
from app.models.risk_zone import RiskZoneResponse
from app.models.user import TokenData
from app.utils.auth import get_current_user, require_authority
from app.services.clustering_service import clustering_service

router = APIRouter(prefix="/zones", tags=["Risk Zones"])


@router.get("", response_model=List[RiskZoneResponse])
async def get_risk_zones(
    risk_level: str = None,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get all risk zones

    - **risk_level**: Filter by risk level (low, medium, high)
    """
    # Build query
    query = {}
    if risk_level:
        if risk_level not in ["low", "medium", "high"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid risk level"
            )
        query["risk_level"] = risk_level

    # Fetch zones
    cursor = db.risk_zones.find(query).sort("pothole_count", -1)
    zones = await cursor.to_list(length=None)

    # Convert to response models
    return [
        RiskZoneResponse(
            _id=str(zone["_id"]),
            center_location=zone["center_location"],
            pothole_count=zone["pothole_count"],
            risk_level=zone["risk_level"],
            h3_index=zone["h3_index"],
            report_ids=[str(rid) for rid in zone["report_ids"]],
            created_at=zone["created_at"],
            updated_at=zone["updated_at"]
        )
        for zone in zones
    ]


@router.get("/high-risk", response_model=List[RiskZoneResponse])
async def get_high_risk_zones(
    current_user: TokenData = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get only high-risk zones"""
    zones = await db.risk_zones.find({"risk_level": "high"}).sort("pothole_count", -1).to_list(length=None)

    return [
        RiskZoneResponse(
            _id=str(zone["_id"]),
            center_location=zone["center_location"],
            pothole_count=zone["pothole_count"],
            risk_level=zone["risk_level"],
            h3_index=zone["h3_index"],
            report_ids=[str(rid) for rid in zone["report_ids"]],
            created_at=zone["created_at"],
            updated_at=zone["updated_at"]
        )
        for zone in zones
    ]


@router.post("/recalculate", status_code=status.HTTP_200_OK)
async def recalculate_zones(
    current_user: TokenData = Depends(require_authority),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Recalculate all risk zones based on current verified reports (Authority only)

    This endpoint triggers the clustering algorithm to group nearby potholes
    and determine risk levels.
    """
    created_zones = await clustering_service.recalculate_risk_zones(db)

    return {
        "message": "Risk zones recalculated successfully",
        "zones_created": len(created_zones)
    }
