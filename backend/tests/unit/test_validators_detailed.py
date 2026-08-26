import pytest
from fastapi import UploadFile, HTTPException
from app.utils.validators import validate_image_file, validate_coordinates
from unittest.mock import MagicMock

def test_validate_image_file_success():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.jpg"
    mock_file.content_type = "image/jpeg"
    # Should not raise
    validate_image_file(mock_file)

    mock_file.filename = "test.png"
    mock_file.content_type = "image/png"
    validate_image_file(mock_file)

def test_validate_image_file_invalid_extension():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.txt"
    mock_file.content_type = "image/jpeg"
    with pytest.raises(HTTPException) as exc:
        validate_image_file(mock_file)
    assert exc.value.status_code == 400
    assert "Invalid file type" in exc.value.detail

def test_validate_image_file_invalid_mime():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.jpg"
    mock_file.content_type = "application/pdf"
    with pytest.raises(HTTPException) as exc:
        validate_image_file(mock_file)
    assert exc.value.status_code == 400
    assert "Invalid MIME type" in exc.value.detail

def test_validate_coordinates_success():
    validate_coordinates(0, 0)
    validate_coordinates(90, 180)
    validate_coordinates(-90, -180)
    validate_coordinates(45.5, -73.6)

def test_validate_coordinates_lat_high():
    with pytest.raises(HTTPException) as exc:
        validate_coordinates(90.1, 0)
    assert "Latitude" in exc.value.detail

def test_validate_coordinates_lat_low():
    with pytest.raises(HTTPException) as exc:
        validate_coordinates(-90.1, 0)
    assert "Latitude" in exc.value.detail

def test_validate_coordinates_lon_high():
    with pytest.raises(HTTPException) as exc:
        validate_coordinates(0, 180.1)
    assert "Longitude" in exc.value.detail

def test_validate_coordinates_lon_low():
    with pytest.raises(HTTPException) as exc:
        validate_coordinates(0, -180.1)
    assert "Longitude" in exc.value.detail
