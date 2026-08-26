import pytest
import h3
from app.services.clustering_service import ClusteringService
from app.models.report import LocationModel
from unittest.mock import MagicMock, AsyncMock
from bson import ObjectId

@pytest.fixture
def service():
    return ClusteringService()

def test_determine_risk_level(service):
    assert service.determine_risk_level(10) == "high"
    assert service.determine_risk_level(5) == "high"
    assert service.determine_risk_level(4) == "medium"
    assert service.determine_risk_level(3) == "medium"
    assert service.determine_risk_level(2) == "low"
    assert service.determine_risk_level(0) == "low"

def test_calculate_center(service):
    locs = [
        LocationModel(latitude=10, longitude=10),
        LocationModel(latitude=20, longitude=20)
    ]
    center = service.calculate_center(locs)
    assert center.latitude == 15
    assert center.longitude == 15

def test_calculate_center_empty(service):
    center = service.calculate_center([])
    assert center.latitude == 0
    assert center.longitude == 0

@pytest.mark.asyncio
async def test_recalculate_risk_zones_empty(service):
    db_mock = MagicMock()
    # Mock cursor to list conversion
    cursor_mock = MagicMock()
    cursor_mock.to_list = AsyncMock(return_value=[])
    db_mock.pothole_reports.find.return_value = cursor_mock
    
    result = await service.recalculate_risk_zones(db_mock)
    assert result == []

@pytest.mark.asyncio
async def test_recalculate_risk_zones_with_data(service):
    db_mock = MagicMock()
    
    # Mock 1 verified report
    report = {
        "_id": ObjectId(),
        "location": {"latitude": 34.0522, "longitude": -118.2437},
        "status": "verified",
        "h3_index": h3.latlng_to_cell(34.0522, -118.2437, 9)
    }
    
    cursor_mock = MagicMock()
    cursor_mock.to_list = AsyncMock(return_value=[report])
    db_mock.pothole_reports.find.return_value = cursor_mock
    
    # Mock insert
    db_mock.risk_zones.insert_one = AsyncMock(return_value=MagicMock(inserted_id="zone1"))
    # Mock delete
    db_mock.risk_zones.delete_many = AsyncMock()
    
    result = await service.recalculate_risk_zones(db_mock)
    assert len(result) == 1
    assert result[0]["risk_level"] == "low"
    assert result[0]["pothole_count"] == 1

@pytest.mark.asyncio
async def test_recalculate_risk_zones_legacy_fallback(service):
    db_mock = MagicMock()
    
    # Mock 1 report missing h3_index
    report = {
        "_id": ObjectId(),
        "location": {"latitude": 34.0522, "longitude": -118.2437},
        "status": "verified"
        # h3_index missing
    }
    
    cursor_mock = MagicMock()
    cursor_mock.to_list = AsyncMock(return_value=[report])
    db_mock.pothole_reports.find.return_value = cursor_mock
    db_mock.risk_zones.insert_one = AsyncMock(return_value=MagicMock(inserted_id="zone2"))
    db_mock.risk_zones.delete_many = AsyncMock()
    
    result = await service.recalculate_risk_zones(db_mock)
    assert len(result) == 1
    assert result[0]["h3_index"] is not None

@pytest.mark.asyncio
async def test_recalculate_risk_zones_multi_cluster(service):
    db_mock = MagicMock()
    # Mock multiple reports in different clusters
    reports = [
        {"_id": ObjectId(), "location": {"latitude": 34, "longitude": -118}, "status": "verified"},
        {"_id": ObjectId(), "location": {"latitude": 40, "longitude": -74}, "status": "verified"}
    ]
    cursor_mock = MagicMock()
    cursor_mock.to_list = AsyncMock(return_value=reports)
    db_mock.pothole_reports.find.return_value = cursor_mock
    db_mock.risk_zones.insert_one = AsyncMock(return_value=MagicMock(inserted_id="z"))
    db_mock.risk_zones.delete_many = AsyncMock()
    
    result = await service.recalculate_risk_zones(db_mock)
    assert len(result) == 2
