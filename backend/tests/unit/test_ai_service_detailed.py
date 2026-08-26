import pytest
import numpy as np
from app.services.ai_verification_service import ai_service
from bson import ObjectId
from unittest.mock import patch, MagicMock

@pytest.fixture
def service():
    return ai_service

@pytest.mark.asyncio
async def test_verify_pothole_success(service):
    report_id = ObjectId()
    # Mock _analyze_image to avoid CV2 calls
    with patch.object(service, '_analyze_image', return_value=(80.0, True)) as mock_analyze:
        result = await service.verify_pothole("dummy_path", report_id)
        assert result.report_id == report_id
        assert result.is_pothole is True
        # Boosted confidence: 80 * 1.15 = 92
        assert result.confidence_score == 92.0

@pytest.mark.asyncio
async def test_verify_pothole_failure_exception(service):
    report_id = ObjectId()
    with patch.object(service, '_analyze_image', side_effect=Exception("CV2 error")):
        result = await service.verify_pothole("dummy_path", report_id)
        assert result.is_pothole is True
        assert result.confidence_score == 70.0

@pytest.mark.asyncio
async def test_analyze_image_no_image(service):
    with patch("cv2.imread", return_value=None):
        conf, is_pothole = await service._analyze_image("invalid")
        assert conf == 0.0
        assert is_pothole is False

@pytest.mark.asyncio
async def test_analyze_image_full_logic(service):
    # Test with a dummy black image to hit all private method calls
    img_path = "dummy_black.jpg"
    with patch("cv2.imread", return_value=np.zeros((100,100,3), dtype=np.uint8)):
        conf, is_pothole = await service._analyze_image(img_path)
        assert isinstance(conf, float)
        assert isinstance(is_pothole, bool)

def test_detect_dark_regions_logic(service):
    # Fully black image yields avg brightness 0, resulting in low dark_ratio branch.
    assert service._detect_dark_regions(np.zeros((10, 10), dtype=np.uint8)) == 40.0
    
    # White image -> low dark ratio -> score 40 (line 140)
    assert service._detect_dark_regions(np.full((10, 10), 255, dtype=np.uint8)) == 40.0

def test_detect_edges_logic(service):
    # low edges -> score 50 (line 161)
    with patch("cv2.Canny", return_value=np.zeros((10,10), dtype=np.uint8)):
        assert service._detect_edges(np.zeros((10,10))) == 50.0
    
    # high edges -> score 70 (line 159)
    with patch("cv2.Canny", return_value=np.full((10,10), 255, dtype=np.uint8)):
        assert service._detect_edges(np.zeros((10,10))) == 70.0

def test_analyze_texture_logic(service):
    # high variance -> score 85 (line 190)
    with patch("app.services.ai_verification_service.np.mean", return_value=4000), patch("app.services.ai_verification_service.np.std", return_value=0):
        assert service._analyze_texture(np.zeros((10,10), dtype=np.uint8)) == 85.0
        
    # low variance -> score 40 (line 192)
    with patch("app.services.ai_verification_service.np.mean", return_value=10), patch("app.services.ai_verification_service.np.std", return_value=0):
        assert service._analyze_texture(np.zeros((10,10), dtype=np.uint8)) == 40.0

def test_analyze_contrast_logic(service):
    # ratio 0.1 -> score 60 (line 217)
    with patch("app.services.ai_verification_service.np.std", return_value=11), patch("app.services.ai_verification_service.np.mean", return_value=100):
        assert service._analyze_contrast(np.zeros((10,10))) == 60.0
        
    # ratio 0.05 -> score 40 (line 219)
    with patch("app.services.ai_verification_service.np.std", return_value=5), patch("app.services.ai_verification_service.np.mean", return_value=100):
        assert service._analyze_contrast(np.zeros((10,10))) == 40.0

def test_detect_holes_logic_circularity(service):
    # Non-circular contours still receive a bounded score in current algorithm.
    contour = np.array([[0,0], [0,10], [50,10], [50,0]]) # Non-circular
    with patch("cv2.findContours", return_value=([contour], None)), \
         patch("cv2.contourArea", return_value=500), \
         patch("cv2.arcLength", return_value=120):
        score = service._detect_holes(np.zeros((100,100), dtype=np.uint8))
        assert 60.0 <= score <= 100.0
    
    # no valid contours -> hit 251 (return 50)
    with patch("cv2.findContours", return_value=([contour], None)), \
         patch("cv2.contourArea", return_value=1): # Too small
        assert service._detect_holes(np.full((100,100), 255, dtype=np.uint8)) == 50.0

def test_detect_holes_logic_basic(service):
    # No holes
    img = np.full((100, 100), 255, dtype=np.uint8)
    assert service._detect_holes(img) == 50.0
    
    # Artificial hole
    img = np.full((100, 100), 255, dtype=np.uint8)
    import cv2
    cv2.circle(img, (50, 50), 20, 0, -1) # Dark circle
    score = service._detect_holes(img)
    assert score >= 50.0

def test_should_auto_verify(service):
    assert service.should_auto_verify(80) is True
    assert service.should_auto_verify(70) is False
