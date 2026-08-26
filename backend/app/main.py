"""
FastAPI Main Application - AI-Based Pothole Detection System
"""
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.config.database import db
from app.routes import auth, reports, zones, repairs

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


async def _seed_test_users():
    """Seed demo login accounts. Development convenience only - never run in production."""
    from app.utils.auth import get_password_hash
    from datetime import datetime

    if not await db.database.users.find_one({"email": settings.TEST_CITIZEN_EMAIL}):
        citizen = {
            "name": "Test Citizen",
            "email": settings.TEST_CITIZEN_EMAIL,
            "hashed_password": get_password_hash(settings.TEST_CITIZEN_PASSWORD),
            "phone": "1234567890",
            "role": "user",
            "created_at": datetime.utcnow()
        }
        await db.database.users.insert_one(citizen)
        logger.info("Created test citizen account: %s", settings.TEST_CITIZEN_EMAIL)

    if not await db.database.users.find_one({"email": settings.TEST_AUTHORITY_EMAIL}):
        authority = {
            "name": "City Admin",
            "email": settings.TEST_AUTHORITY_EMAIL,
            "hashed_password": get_password_hash(settings.TEST_AUTHORITY_PASSWORD),
            "phone": "9876543210",
            "role": "authority",
            "created_at": datetime.utcnow()
        }
        await db.database.users.insert_one(authority)
        logger.info("Created test authority account: %s", settings.TEST_AUTHORITY_EMAIL)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """Application lifespan manager"""
    # Startup
    await db.connect_db()

    # Demo accounts are only ever seeded in development, never in staging/production,
    # since they use fixed, publicly-known credentials.
    if settings.ENVIRONMENT.lower() == "development":
        await _seed_test_users()

    logger.info("Application started successfully")

    yield

    # Shutdown
    await db.close_db()
    logger.info("Application shut down")


# Create FastAPI application
app = FastAPI(
    title="Pothole Detection API",
    description="AI-Based Road Damage & Pothole Detection System Backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - origins are configured via CORS_ORIGINS in settings/.env
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for serving images
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(reports.router, prefix=settings.API_V1_PREFIX)
app.include_router(zones.router, prefix=settings.API_V1_PREFIX)
app.include_router(repairs.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI-Based Pothole Detection System API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if db.database is not None else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
