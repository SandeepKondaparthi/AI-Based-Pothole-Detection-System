import pytest
from unittest.mock import MagicMock, AsyncMock
from bson import ObjectId
from app.services.clustering_service import ClusteringService

@pytest.mark.asyncio
async def test_clustering_with_h3_indices():
    # Mock DB
    db = MagicMock()
    service = ClusteringService()
    
    # Sample reports with H3 indices (Res 9)
    # These indices are close to each other
    h3_index = "8960145b483ffff"
    reports = [
        {"_id": ObjectId(), "location": {"latitude": 34.05, "longitude": -118.24}, "h3_index": h3_index, "status": "verified"},
        {"_id": ObjectId(), "location": {"latitude": 34.0501, "longitude": -118.2401}, "h3_index": h3_index, "status": "verified"}
    ]
    
    # Mock find().to_list()
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=reports)
    db.pothole_reports.find.return_value = mock_cursor
    db.risk_zones.delete_many = AsyncMock()
    db.risk_zones.insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))
    
    # Run recalculation
    zones = await service.recalculate_risk_zones(db)
    
    # Should have 1 zone because they share the same H3 index
    assert len(zones) == 1
    assert zones[0]["h3_index"] == h3_index
    assert zones[0]["pothole_count"] == 2

@pytest.mark.asyncio
async def test_clustering_legacy_fallback():
    # Test that reports without h3_index are handled correctly
    db = MagicMock()
    service = ClusteringService()
    
    reports = [
        {"_id": ObjectId(), "location": {"latitude": 34.05, "longitude": -118.24}, "status": "verified"}
    ]
    
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=reports)
    db.pothole_reports.find.return_value = mock_cursor
    db.risk_zones.delete_many = AsyncMock()
    db.risk_zones.insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))
    
    zones = await service.recalculate_risk_zones(db)
    
    assert len(zones) == 1
    assert zones[0]["pothole_count"] == 1
    assert zones[0]["h3_index"] is not None
