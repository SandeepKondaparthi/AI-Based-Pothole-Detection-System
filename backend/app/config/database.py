"""
MongoDB database connection and management
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from pymongo.errors import PyMongoError
from app.config import settings

logger = logging.getLogger(__name__)


class Database:
    """MongoDB database manager"""

    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

    async def connect_db(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            self.database = self.client[settings.MONGODB_DB_NAME]

            # Test connection
            await self.client.admin.command('ping')
            logger.info("Connected to MongoDB: %s", settings.MONGODB_DB_NAME)

            # Create indexes for better performance
            await self.create_indexes()

        except Exception as e:
            logger.error("Error connecting to MongoDB: %s", e)
            raise

    async def close_db(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    async def create_indexes(self):
        """Create database indexes for better query performance"""
        try:
            # Users collection indexes
            await self.database.users.create_index("email", unique=True)

            # Pothole reports collection indexes
            await self.database.pothole_reports.create_index("status")
            await self.database.pothole_reports.create_index("user_id")
            await self.database.pothole_reports.create_index("h3_index")
            await self.database.pothole_reports.create_index(
                [("location.latitude", 1), ("location.longitude", 1)]
            )

            # Create TTL index for image verification history
            await self.database.image_verification.create_index(
                "request_time",
                expireAfterSeconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )

            # Risk zones collection indexes
            await self.database.risk_zones.create_index("h3_index", unique=True)
            await self.database.risk_zones.create_index(
                [("center_location.latitude", 1), ("center_location.longitude", 1)]
            )

            # Repair actions collection indexes
            await self.database.repair_actions.create_index("zone_id")
            await self.database.repair_actions.create_index("repair_status")

            logger.info("Database indexes created")

        except PyMongoError as e:
            logger.error("Error creating database indexes: %s", e)


# Global database instance
db = Database()


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance for dependency injection"""
    return db.database
