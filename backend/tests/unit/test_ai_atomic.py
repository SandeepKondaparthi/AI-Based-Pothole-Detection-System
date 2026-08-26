import pytest
import numpy as np
from app.services.ai_verification_service import ai_service
from bson import ObjectId

@pytest.fixture
def atomic_service():
    return ai_service

def test_atomic_should_auto_verify(atomic_service):
    # Hit line 283
    atomic_service.auto_verify_threshold = 75.0
    assert atomic_service.should_auto_verify(76) is True
    assert atomic_service.should_auto_verify(74) is False

def test_atomic_dark_regions_hit_134_138(atomic_service):
    # Fully black image falls into low-dark-ratio branch with current thresholding.
    img_black = np.zeros((10,10), dtype=np.uint8)
    assert atomic_service._detect_dark_regions(img_black) == 40.0
    
    # ratio 0.2 (0.08 - 0.40) -> 134
    img = np.full((10,10), 200, dtype=np.uint8)
    img[0:2, :] = 0
    assert atomic_service._detect_dark_regions(img) >= 85.0
