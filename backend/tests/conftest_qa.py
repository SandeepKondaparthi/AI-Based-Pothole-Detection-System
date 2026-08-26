"""
Pytest configuration and MongoDB test database setup
"""

import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError
import os


# Test database configuration
TEST_MONGODB_URI = os.getenv("TEST_MONGODB_URI", "mongodb://localhost:27017")
TEST_DB_NAME = "roadcare_qa_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def mongodb_client():
    """Connect to MongoDB for testing"""
    try:
        client = AsyncIOMotorClient(TEST_MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Verify connection
        await client.admin.command('ping')
        print(f"\n✅ Connected to MongoDB at {TEST_MONGODB_URI}")
        yield client
        client.close()
    except ServerSelectionTimeoutError:
        pytest.skip("MongoDB not available")


@pytest.fixture(scope="session")
async def db(mongodb_client):
    """Get test database"""
    database = mongodb_client[TEST_DB_NAME]
    
    # Clear database before tests
    await database.command("dropDatabase")
    print(f"\n✅ Using test database: {TEST_DB_NAME}")
    
    # Create indexes
    await database.users.create_index("email", unique=True)
    await database.pothole_reports.create_index("user_id")
    await database.pothole_reports.create_index("h3_index")
    await database.risk_zones.create_index("h3_index")
    
    yield database
    
    # Cleanup after tests
    await database.command("dropDatabase")


@pytest.fixture
async def clean_db(db):
    """Clean database before each test"""
    for collection_name in await db.list_collection_names():
        await db[collection_name].delete_many({})
    yield db


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as async"
    )


# Optional: Configure logging
import logging
logging.basicConfig(level=logging.INFO)
