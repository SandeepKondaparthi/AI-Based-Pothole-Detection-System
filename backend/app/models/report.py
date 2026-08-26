"""
Pothole report data models
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId


class LocationModel(BaseModel):
    """GPS location coordinates"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class ReportBase(BaseModel):
    """Base report model"""
    description: Optional[str] = Field(None, max_length=500)
    location: LocationModel


class ReportCreate(ReportBase):
    """Report creation model (from form submission)"""
    pass


class ReportInDB(ReportBase):
    """Report model as stored in database"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId
    image_path: str
    h3_index: Optional[str] = Field(default=None, index=True)
    status: str = Field(default="pending", pattern="^(pending|verified|rejected)$")
    report_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        from_attributes = True


class ReportResponse(ReportBase):
    """Report response model"""
    id: str = Field(..., alias="_id")
    user_id: str
    image_path: str
    h3_index: Optional[str] = None
    status: str
    report_date: datetime
    ai_confidence: Optional[float] = Field(None, description="AI verification confidence score (0-100)")
    ai_verified: Optional[bool] = Field(None, description="Whether AI detected a pothole")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        from_attributes = True


class ReportStatusUpdate(BaseModel):
    """Model for updating report status"""
    status: str = Field(..., pattern="^(pending|verified|rejected)$")
    notes: Optional[str] = Field(None, max_length=500)
