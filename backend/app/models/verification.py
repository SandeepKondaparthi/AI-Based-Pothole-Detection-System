"""
AI verification data models
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId


class VerificationBase(BaseModel):
    """Base verification model"""
    is_pothole: bool
    confidence_score: float = Field(..., ge=0, le=100)


class VerificationInDB(VerificationBase):
    """Verification model as stored in database"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    report_id: PyObjectId
    verified_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class VerificationResponse(VerificationBase):
    """Verification response model"""
    id: str = Field(..., alias="_id")
    report_id: str
    verified_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
