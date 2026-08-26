import pytest
import os
from fastapi import UploadFile, HTTPException
from app.services.image_service import IMAGE_SERVICE
from unittest.mock import MagicMock, patch
import io
from PIL import Image

@pytest.mark.asyncio
async def test_save_image_success():
    # Mock UploadFile
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.jpg"
    mock_file.content_type = "image/jpeg"
    
    # Create valid image bytes
    img = Image.new('RGB', (10, 10), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    mock_file.read.return_value = img_byte_arr.read()
    mock_file.file = img_byte_arr
    
    with patch("builtins.open", MagicMock()):
        path = await IMAGE_SERVICE.save_image(mock_file)
        assert "pothole_" in path

@pytest.mark.asyncio
async def test_save_image_corrupted():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.jpg"
    mock_file.content_type = "image/jpeg"
    mock_file.read.return_value = b"not an image"
    mock_file.file = io.BytesIO(b"not an image")
    
    with pytest.raises(HTTPException) as exc:
        await IMAGE_SERVICE.save_image(mock_file)
    assert exc.value.status_code == 400

def test_delete_image():
    with patch("os.path.exists", return_value=True), patch("os.remove", return_value=None):
        assert IMAGE_SERVICE.delete_image("any_path") is True
    
    with patch("os.path.exists", return_value=False):
        assert IMAGE_SERVICE.delete_image("any_path") is False

def test_delete_image_oserror():
    with patch("os.path.exists", return_value=True), patch("os.remove", side_effect=OSError("Permission denied")):
        assert IMAGE_SERVICE.delete_image("any_path") is False

@pytest.mark.asyncio
async def test_save_image_value_error():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.jpg"
    mock_file.content_type = "image/jpeg"
    mock_file.read.return_value = b"some bytes"
    mock_file.file = io.BytesIO(b"some bytes")
    # Mocking Image.open to raise ValueError for img.verify()
    with patch("PIL.Image.open") as mock_open:
        mock_img = MagicMock()
        mock_img.verify.side_effect = ValueError("Corrupted")
        mock_open.return_value = mock_img
        with pytest.raises(HTTPException) as exc:
            await IMAGE_SERVICE.save_image(mock_file)
        assert exc.value.status_code == 400
