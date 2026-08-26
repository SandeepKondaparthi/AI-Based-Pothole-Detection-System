"""
Risk zone data models
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId
from app.models.report import LocationModel


class RiskZoneBase(BaseModel):
    """Base risk zone model"""
    center_location: LocationModel
    pothole_count: int = Field(default=0, ge=0)
    risk_level: str = Field(..., pattern="^(low|medium|high)$")


class RiskZoneInDB(RiskZoneBase):
    """Risk zone model as stored in database"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    report_ids: List[PyObjectId] = Field(default_factory=list)
    h3_index: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RiskZoneResponse(RiskZoneBase):
    """Risk zone response model"""
    id: str = Field(..., alias="_id")
    report_ids: List[str]
    h3_index: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
