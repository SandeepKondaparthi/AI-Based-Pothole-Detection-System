"""
Configuration settings for the application
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "pothole_detection"

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10

    # API Configuration
    API_V1_PREFIX: str = "/api"
    # NOTE: "*" is not valid alongside allow_credentials=True in the CORS middleware
    # (browsers reject it). Set explicit origins here or via CORS_ORIGINS in .env.
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Environment
    ENVIRONMENT: str = "development"

    # Testing Credentials
    TEST_AUTHORITY_EMAIL: str = "admin@city.gov"
    TEST_AUTHORITY_PASSWORD: str = "admin123"
    TEST_CITIZEN_EMAIL: str = "citizen@test.com"
    TEST_CITIZEN_PASSWORD: str = "password123"

    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra environment variables
        case_sensitive = True


settings = Settings()
