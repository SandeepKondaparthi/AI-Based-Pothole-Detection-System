"""
Geographic clustering service for risk zone detection
Using Uber's H3 Hexagonal Indexing System
"""
from datetime import datetime
from collections import defaultdict
from typing import List, Dict

import h3
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.report import LocationModel
from app.models.risk_zone import RiskZoneInDB


# pylint: disable=no-member

class ClusteringService:
    """
    Service for geographic clustering and risk zone calculation
    Using Uber's H3 Hexagonal Indexing System
    """

    # H3 Resolution for City-level pothole clustering (~0.1 km2 hexagons)
    H3_RESOLUTION = 9

    # Risk level thresholds
    HIGH_RISK_THRESHOLD = 5  # 5+ potholes
    MEDIUM_RISK_THRESHOLD = 3  # 3-4 potholes

    def determine_risk_level(self, pothole_count: int) -> str:
        """Determine risk level based on pothole count"""
        if pothole_count >= self.HIGH_RISK_THRESHOLD:
            return "high"
        elif pothole_count >= self.MEDIUM_RISK_THRESHOLD:
            return "medium"
        else:
            return "low"

    def calculate_center(self, locations: List[LocationModel]) -> LocationModel:
        """Calculate geographic center of multiple locations"""
        if not locations:
            return LocationModel(latitude=0, longitude=0)

        avg_lat = sum(loc.latitude for loc in locations) / len(locations)
        avg_lon = sum(loc.longitude for loc in locations) / len(locations)

        return LocationModel(latitude=avg_lat, longitude=avg_lon)

    async def recalculate_risk_zones(self, db: AsyncIOMotorDatabase) -> List[Dict]:
        """
        Recalculate all risk zones based on verified pothole reports
        Using H3 Hexagonal Aggregation

        Args:
            db: Database instance

        Returns:
            List of created/updated risk zones
        """
        # Get all verified pothole reports
        reports_cursor = db.pothole_reports.find({"status": "verified"})
        reports = await reports_cursor.to_list(length=None)

        if not reports:
            return []

        # Clear existing risk zones
        await db.risk_zones.delete_many({})

        # Group reports by H3 index
        h3_clusters = defaultdict(list)

        for report in reports:
            # Use stored h3_index or calculate if missing (legacy data)
            h3_index = report.get("h3_index")
            if not h3_index:
                loc = report["location"]
                h3_index = h3.latlng_to_cell(loc["latitude"], loc["longitude"], self.H3_RESOLUTION)

            h3_clusters[h3_index].append(report)

        # Create risk zones for each H3 cell
        created_zones = []
        for h3_index, cluster in h3_clusters.items():
            # Calculate center location
            locations = [LocationModel(**r["location"]) for r in cluster]
            center = self.calculate_center(locations)

            # Determine risk level
            pothole_count = len(cluster)
            risk_level = self.determine_risk_level(pothole_count)

            # Create risk zone
            zone = RiskZoneInDB(
                center_location=center,
                h3_index=h3_index,
                pothole_count=pothole_count,
                risk_level=risk_level,
                report_ids=[r["_id"] for r in cluster],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Insert into database
            result = await db.risk_zones.insert_one(zone.dict(by_alias=True, exclude={"id"}))
            zone.id = result.inserted_id

            created_zones.append(zone.dict(by_alias=True))

        return created_zones


# Global clustering service instance
clustering_service = ClusteringService()
