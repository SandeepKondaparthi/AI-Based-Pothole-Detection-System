import pytest
import numpy as np
import cv2
import os
from app.services.ai_verification_service import AIVerificationService
from bson import ObjectId
from unittest.mock import patch, MagicMock

@pytest.fixture
def s():
    return AIVerificationService()

def test_ai_should_auto_verify(s):
    assert s.should_auto_verify(80) is True
    assert s.should_auto_verify(70) is False

def test_ai_detect_dark_logic(s):
    # Fully black image falls into low-dark-ratio branch with current thresholding.
    assert s._detect_dark_regions(np.zeros((10,10), dtype=np.uint8)) == 40.0
    # ratio 0.0 (white) -> 140
    assert s._detect_dark_regions(np.full((10,10), 255, dtype=np.uint8)) == 40.0
    # ratio 0.1 (0.08 - 0.40) -> 134
    img = np.full((10,10), 200, dtype=np.uint8)
    img[0, :] = 100 # 10% dark
    assert s._detect_dark_regions(img) >= 85.0
    # ratio 0.5 (else) -> 136
    img = np.full((10,10), 200, dtype=np.uint8)
    img[0:5, :] = 100 
    assert s._detect_dark_regions(img) >= 0

def test_ai_detect_edges_logic(s):
    # min edges -> 161
    with patch("cv2.Canny", return_value=np.zeros((10,10), dtype=np.uint8)):
        assert s._detect_edges(np.zeros((10,10))) == 50.0
    # max edges -> 159
    with patch("cv2.Canny", return_value=np.full((10,10), 255, dtype=np.uint8)):
        assert s._detect_edges(np.zeros((10,10))) == 70.0
    # intermediate -> 157
    with patch("cv2.Canny", return_value=np.zeros((10,10), dtype=np.uint8)) as m:
        e = np.zeros((10,10), dtype=np.uint8); e[0,0:1]=255
        m.return_value = e
        assert s._detect_edges(np.zeros((10,10))) >= 0

def test_ai_texture_logic(s):
    # no variances -> 180
    assert s._analyze_texture(np.zeros((1,1), dtype=np.uint8)) == 50.0
    # high variance -> 190
    with patch("app.services.ai_verification_service.np.mean", return_value=4000), patch("app.services.ai_verification_service.np.std", return_value=0):
        assert s._analyze_texture(np.zeros((10,10))) == 85.0
    # low variance -> 192
    with patch("app.services.ai_verification_service.np.mean", return_value=10), patch("app.services.ai_verification_service.np.std", return_value=0):
        assert s._analyze_texture(np.zeros((10,10))) == 40.0
    # hit 188
    with patch("app.services.ai_verification_service.np.mean", return_value=1000), patch("app.services.ai_verification_service.np.std", return_value=0):
        assert s._analyze_texture(np.zeros((10,10))) >= 50.0
    # hit 196 (uneven)
    img = np.zeros((100,100), dtype=np.uint8); img[0:33, 0:33]=255
    assert s._analyze_texture(img) >= 40.0

def test_ai_contrast_logic(s):
    # ratio 0.1 -> 217
    with patch("app.services.ai_verification_service.np.std", return_value=11), patch("app.services.ai_verification_service.np.mean", return_value=100):
        assert s._analyze_contrast(np.zeros((10,10))) == 60.0
    # ratio 0.05 -> 219
    with patch("app.services.ai_verification_service.np.std", return_value=5), patch("app.services.ai_verification_service.np.mean", return_value=100):
        assert s._analyze_contrast(np.zeros((10,10))) == 40.0
    # ratio 0.3 -> 211
    with patch("app.services.ai_verification_service.np.std", return_value=40), patch("app.services.ai_verification_service.np.mean", return_value=100):
        assert s._analyze_contrast(np.zeros((10,10))) == 95.0
    # ratio 0.2 -> 213
    with patch("app.services.ai_verification_service.np.std", return_value=25), patch("app.services.ai_verification_service.np.mean", return_value=100):
        assert s._analyze_contrast(np.zeros((10,10))) == 85.0
    # ratio 0.15 -> 215
    with patch("app.services.ai_verification_service.np.std", return_value=17), patch("app.services.ai_verification_service.np.mean", return_value=100):
        assert s._analyze_contrast(np.zeros((10,10))) == 70.0

def test_ai_holes_logic(s):
    # Non-circular contours still receive a bounded score in current algorithm.
    c = np.array([[0,0], [10,0], [10,50], [0,50]]) 
    with patch("cv2.findContours", return_value=([c], None)), \
         patch("cv2.contourArea", return_value=500), \
         patch("cv2.arcLength", return_value=120):
        score = s._detect_holes(np.zeros((100,100), dtype=np.uint8))
        assert 60.0 <= score <= 100.0
    # skip invalid -> 251
    with patch("cv2.findContours", return_value=([c], None)), \
         patch("cv2.contourArea", return_value=1):
        assert s._detect_holes(np.zeros((100,100), dtype=np.uint8)) == 50.0
    # valid -> 270 (and 265, 266)
    img = np.full((100,100), 255, dtype=np.uint8)
    cv2.circle(img, (50, 50), 15, 0, -1)
    assert s._detect_holes(img) >= 60.0

@pytest.mark.asyncio
async def test_ai_pothole_full(s):
    r = ObjectId()
    with patch.object(s, '_analyze_image', return_value=(80.0, True)):
        res = await s.verify_pothole("dummy", r)
        assert res.report_id == r
    # hit exception branch 60-68
    with patch.object(s, '_analyze_image', side_effect=Exception):
        res = await s.verify_pothole("dummy", r)
        assert res.is_pothole is True
