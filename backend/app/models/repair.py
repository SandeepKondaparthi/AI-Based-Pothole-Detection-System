"""
Repair action data models
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId


class RepairActionBase(BaseModel):
    """Base repair action model"""
    assigned_department: str = Field(..., min_length=2, max_length=100)
    repair_status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")


class RepairActionCreate(RepairActionBase):
    """Repair action creation model"""
    zone_id: str


class RepairActionInDB(RepairActionBase):
    """Repair action model as stored in database"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    zone_id: PyObjectId
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RepairActionResponse(RepairActionBase):
    """Repair action response model"""
    id: str = Field(..., alias="_id")
    zone_id: str
    start_date: datetime
    end_date: Optional[datetime]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class RepairActionUpdate(BaseModel):
    """Model for updating repair action"""
    repair_status: str = Field(..., pattern="^(pending|in_progress|completed)$")
    assigned_department: Optional[str] = Field(None, min_length=2, max_length=100)
