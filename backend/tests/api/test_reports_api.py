import pytest
import httpx
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_root_endpoint():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "Pothole Detection System API" in response.json()["message"]

@pytest.mark.asyncio
async def test_unauthorized_reports_access():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/reports")
    # Missing auth can return 401 or 403 based on auth backend behavior.
    assert response.status_code in [401, 403]
