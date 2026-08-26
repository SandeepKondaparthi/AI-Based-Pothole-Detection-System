import pytest
import httpx
import os
import cv2
import numpy as np
from app.main import app
from app.config import settings
from unittest.mock import patch, MagicMock, AsyncMock
from bson import ObjectId

@pytest.mark.asyncio
async def test_full_pipeline_extreme():
    # Simulate a full report flow: Upload -> AI Verify -> DB Save
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        # 1. Login to get token (Mocked)
        token = "test_token"
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Upload Report with Image
        # Mock the auth and DB
        valid_user_id = str(ObjectId())
        with patch("app.utils.auth.decode_token", return_value=MagicMock(user_id=valid_user_id, email="a@b.com", role="user")), \
             patch("app.routes.reports.IMAGE_SERVICE.save_image", new_callable=AsyncMock) as mock_save, \
             patch("app.routes.reports.ai_service.verify_pothole", new_callable=AsyncMock) as mock_ai:
            
            mock_save.return_value = "uploads/test_pothole.jpg"
            mock_ai.return_value = MagicMock(is_pothole=True, confidence_score=95.0)

            # Ensure DB writes are awaitable in this integration path.
            from app.config.database import db
            db.database.pothole_reports.insert_one = AsyncMock()
            db.database.image_verification.insert_one = AsyncMock()
            
            payload = {
                "latitude": 34.0522,
                "longitude": -118.2437,
                "description": "Severe pothole at intersection"
            }
            
            files = {'image': ('test.jpg', b'dummy_content', 'image/jpeg')}
            
            response = await ac.post(
                "/api/reports",
                data=payload,
                files=files,
                headers=headers
            )
            
            # Since we mock the DB in conftest, it should return 200/201 if successful
            assert response.status_code in [200, 201]
            data = response.json()
            assert "_id" in data
            assert data["status"] == "verified"
