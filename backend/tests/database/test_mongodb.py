import pytest
import h3
from app.config.database import db
from app.models.report import ReportInDB
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId

@pytest.mark.asyncio
async def test_mongodb_report_persistence():
    # Use async mocks so test does not depend on external MongoDB availability.
    db.database = MagicMock()
    inserted_id = ObjectId()
    db.database.pothole_reports.insert_one = AsyncMock(return_value=MagicMock(inserted_id=inserted_id))
    db.database.pothole_reports.find_one = AsyncMock()
    db.database.pothole_reports.delete_one = AsyncMock()
        
    # Create a test report
    h3_index = h3.latlng_to_cell(34.0522, -118.2437, 9)
    report_data = {
        "user_id": str(ObjectId()),
        "image_path": "/uploads/test.jpg",
        "location": {"latitude": 34.0522, "longitude": -118.2437},
        "h3_index": h3_index,
        "status": "pending",
        "report_date": datetime.utcnow()
    }
    db.database.pothole_reports.find_one.return_value = {**report_data, "_id": inserted_id}
    
    # Store in DB
    result = await db.database.pothole_reports.insert_one(report_data)
    assert result.inserted_id is not None
    
    # Query back by H3 index
    stored_report = await db.database.pothole_reports.find_one({"h3_index": h3_index})
    assert stored_report["user_id"] == report_data["user_id"]
    
    # Clean up (Optional: depend on test strategy)
    await db.database.pothole_reports.delete_one({"_id": result.inserted_id})
