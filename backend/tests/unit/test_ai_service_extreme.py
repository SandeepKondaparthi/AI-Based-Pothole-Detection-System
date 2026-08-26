import pytest
import numpy as np
import cv2
from app.services.ai_verification_service import AIVerificationService
from bson import ObjectId

@pytest.fixture
def service():
    return AIVerificationService()

def test_detect_dark_regions_exhaustive(service):
    # Case: dark_ratio > 0.5 (line 138)
    img = np.zeros((10, 10), dtype=np.uint8)
    assert service._detect_dark_regions(img) == 40.0
    
    # Case: dark_ratio < 0.03 (line 140)
    img = np.full((10, 10), 255, dtype=np.uint8)
    assert service._detect_dark_regions(img) == 40.0

def test_detect_edges_exhaustive(service):
    # Case: edge_ratio > 0.30 (line 159)
    img = np.zeros((100, 100), dtype=np.uint8)
    # Fill with edges (Canny will hit everything)
    img[::2, ::2] = 255
    score = service._detect_edges(img)
    assert score >= 50.0

def test_analyze_texture_exhaustive(service):
    # Case: variances empty (line 180) - impossible with 100x100 but maybe with 1x1
    assert service._analyze_texture(np.zeros((1, 1), dtype=np.uint8)) == 50.0
    
    # Case: non-trivial texture should stay within valid scoring bounds.
    img = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
    assert 40.0 <= service._analyze_texture(img) <= 100.0
    
    # Case: avg_variance < 100 (line 192)
    assert service._analyze_texture(np.zeros((100, 100), dtype=np.uint8)) == 40.0

def test_analyze_contrast_exhaustive(service):
    # Case: 0.1 < ratio <= 0.15 (line 216)
    # std/avg ~ 0.12
    img = np.full((10, 10), 100, dtype=np.uint8)
    img[0, 0] = 50 
    score = service._analyze_contrast(img)
    assert score >= 40.0
    
    # Case: ratio <= 0.1 (line 219)
    img = np.full((10, 10), 100, dtype=np.uint8)
    assert service._analyze_contrast(img) == 40.0

def test_detect_holes_exhaustive(service):
    # Case: No contours (line 237)
    img = np.full((100, 100), 255, dtype=np.uint8)
    assert service._detect_holes(img) == 50.0
    
    # Case: Valid hole (hits 246, 247, 260, 270)
    img = np.full((100, 100), 255, dtype=np.uint8)
    cv2.circle(img, (50, 50), 15, 0, -1)
    assert service._detect_holes(img) >= 60.0

@pytest.mark.asyncio
async def test_detect_dark_regions_intermediate(service):
    # ratio in (0.08, 0.40) -> hit 134
    img = np.full((10, 10), 200, dtype=np.uint8)
    img[0, 0:2] = 0 # 20% dark
    score = service._detect_dark_regions(img)
    assert score >= 40.0

def test_detect_edges_intermediate(service):
    # ratio in (0.02, 0.30) -> hit 157
    from unittest.mock import patch
    with patch("cv2.Canny", return_value=np.zeros((10,10), dtype=np.uint8)) as m:
        edges = np.zeros((10,10), dtype=np.uint8)
        edges[0, 0] = 255 # 1%
        m.return_value = edges
        assert service._detect_edges(np.zeros((10,10))) == 50.0

def test_analyze_texture_uneven(service):
    # hit 196 (variance_std > 50)
    img = np.zeros((100, 100), dtype=np.uint8)
    img[0:33, 0:33] = 255 # One block high variance
    score = service._analyze_texture(img)
    assert score >= 40.0

def test_analyze_contrast_steps(service):
    # ratio > 0.3 -> hit 211
    # std=100, avg=100 -> ratio=1.0
    from unittest.mock import patch
    with patch("app.services.ai_verification_service.np.std", return_value=100), patch("app.services.ai_verification_service.np.mean", return_value=100):
        assert service._analyze_contrast(np.zeros((10,10))) == 95.0

@pytest.mark.asyncio
async def test_verify_pothole_full(service):
    # Real image test (hits 51-58)
    # We need a dummy file
    dummy_file = "test_pothole.jpg"
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(dummy_file, img)
    try:
        report_id = ObjectId()
        result = await service.verify_pothole(dummy_file, report_id)
        assert result.report_id == report_id
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)

import os
