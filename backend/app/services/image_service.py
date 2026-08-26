"""
Image upload and storage service
"""
import os
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from PIL import Image, UnidentifiedImageError
from app.config import settings
from app.utils.validators import validate_image_file


class ImageService:
    """Service for handling image uploads and storage"""

    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_image(self, file: UploadFile) -> str:
        """
        Save uploaded image to disk

        Args:
            file: Uploaded file object

        Returns:
            str: Relative path to saved image
        """
        # Validate file
        validate_image_file(file)

        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1].lower()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        new_filename = f"pothole_{timestamp}_{unique_id}{file_ext}"

        # Full path to save file
        file_path = os.path.join(self.upload_dir, new_filename)

        try:
            # Read and save file
            contents = await file.read()

            # Verify it's a valid image using PIL
            try:
                img = Image.open(file.file)
                img.verify()
            except (UnidentifiedImageError, ValueError) as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or corrupted image file"
                ) from e

            # Reset file pointer and save
            await file.seek(0)
            with open(file_path, "wb") as f:
                f.write(contents)

            # Return relative path
            return os.path.join(settings.UPLOAD_DIR, new_filename)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving image: {str(e)}"
            ) from e

    def delete_image(self, image_path: str) -> bool:
        """Delete image from disk"""
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                return True
            return False
        except OSError:
            return False


# Global image service instance
IMAGE_SERVICE = ImageService()
