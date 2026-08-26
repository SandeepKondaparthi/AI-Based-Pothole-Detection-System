import pytest
import httpx
from app.main import app
from app.config import settings
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_api_health_extreme():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_api_root_extreme():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_api_reports_unauthorized():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        # GET
        res = await ac.get("/api/reports")
        assert res.status_code in [401, 403]
        # POST
        res = await ac.post("/api/reports", json={})
        assert res.status_code in [401, 403]

@pytest.mark.asyncio
async def test_api_users_login_fail():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post("/api/auth/login", json={"email": "wrong@test.com", "password": "x"})
        assert res.status_code == 401

@pytest.mark.asyncio
async def test_api_zones_unauthorized():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/zones")
        # HTTPBearer may return 401 or 403 when auth header is missing.
        assert response.status_code in [401, 403]
