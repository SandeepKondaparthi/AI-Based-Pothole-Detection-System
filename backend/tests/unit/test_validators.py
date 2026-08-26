import pytest
from fastapi import HTTPException
from app.utils.validators import validate_coordinates

def test_validate_coordinates_valid():
    # Should not raise exception
    validate_coordinates(34.0522, -118.2437)
    validate_coordinates(0, 0)
    validate_coordinates(90, 180)
    validate_coordinates(-90, -180)

def test_validate_coordinates_invalid_latitude():
    with pytest.raises(HTTPException) as excinfo:
        validate_coordinates(91, 0)
    assert excinfo.value.status_code == 400
    assert "Latitude" in excinfo.value.detail

    with pytest.raises(HTTPException):
        validate_coordinates(-90.1, 0)

def test_validate_coordinates_invalid_longitude():
    with pytest.raises(HTTPException) as excinfo:
        validate_coordinates(0, 181)
    assert excinfo.value.status_code == 400
    assert "Longitude" in excinfo.value.detail

    with pytest.raises(HTTPException):
        validate_coordinates(0, -180.1)
