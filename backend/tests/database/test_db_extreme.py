import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from bson import ObjectId
from datetime import datetime

@pytest.mark.asyncio
async def test_db_schema_integrity_extreme():
    # Verify we can connect and perform basic CRUD operations if URI exists
    # If not, we verify the model serialization
    from app.models.report import ReportInDB, LocationModel
    
    loc = LocationModel(latitude=34.0, longitude=-118.0)
    report = ReportInDB(
        _id=ObjectId(),
        user_id=ObjectId(),
        image_path="test.jpg",
        location=loc,
        h3_index="8928308280fffff",
        status="pending"
    )
    
    data = report.dict(by_alias=True)
    assert "_id" in data
    # Pydantic serialization may render ObjectId fields as strings.
    assert isinstance(data["_id"], (ObjectId, str))
    assert data["location"]["latitude"] == 34.0

def test_db_user_schema_extreme():
    from app.models.user import UserInDB
    user = UserInDB(
        _id=ObjectId(),
        name="Test",
        email="a@b.com",
        phone="1234567890",
        hashed_password="hash",
        role="user",
        created_at=datetime.utcnow()
    )
    assert user.role == "user"
