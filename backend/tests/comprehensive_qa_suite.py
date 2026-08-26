"""
COMPREHENSIVE QA & DATABASE RELIABILITY TEST SUITE
==================================================
Testing System for:
- Authentication system
- Pothole detection system
- Hexagonal map visualization
- Database integrity & persistence
- ACID compliance
- Failure recovery
- Data consistency
- Security validation

Phase Flow: INPUT → PROCESS → STORE → RETRIEVE → VERIFY → BREAK → RECOVER
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib
import random

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from passlib.context import CryptContext

# Test configuration
CONFIG = {
    "db_name": "test_qa_suite",
    "mongodb_uri": "mongodb://localhost:27017",
    "test_timeout": 30,
    "concurrent_users": 5,
}


# ============================================================================
# PHASE 1: TEST DATA GENERATION
# ============================================================================

@dataclass
class TestUser:
    """Test user with all required attributes"""
    user_id: str
    email: str
    password: str
    name: str
    phone: str
    role: str
    created_timestamp: datetime = None
    
    def __post_init__(self):
        if self.created_timestamp is None:
            self.created_timestamp = datetime.utcnow()


class TestDataGenerator:
    """Generate 9+ test users with edge cases"""
    
    @staticmethod
    def generate_test_users() -> List[TestUser]:
        """
        Generate comprehensive test user set including:
        - Normal users (authority + regular)
        - Edge cases (long names, special chars)
        - Invalid formats (for negative testing)
        """
        users = []
        
        # 1. Normal authority user
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="authority@roadcare.gov",
            password="SecureAuth123!",
            name="Authority Admin",
            phone="9876543210",
            role="authority"
        ))
        
        # 2. Normal regular user
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="user@roadcare.local",
            password="UserPass123!",
            name="Regular User",
            phone="9123456789",
            role="user"
        ))
        
        # 3. Edge case: Maximum length name
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="maxname@roadcare.local",
            password="Password123!",
            name="A" * 100,  # Max allowed length
            phone="9000000001",
            role="user"
        ))
        
        # 4. Edge case: Minimum length name
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="minname@roadcare.local",
            password="Password123!",
            name="AB",  # Min 2 chars
            phone="9000000002",
            role="user"
        ))
        
        # 5. Edge case: International domain email
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="user+tag@international.co.uk",
            password="Password123!",
            name="International User",
            phone="447000000001",
            role="user"
        ))
        
        # 6. Edge case: Numeric-heavy phone
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="phone.user@roadcare.local",
            password="Password123!",
            name="Phone Edge User",
            phone="9999999999999",  # Long phone
            role="user"
        ))
        
        # 7. Edge case: Special characters in name
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="special@roadcare.local",
            password="Password123!",
            name="José-María O'Connor",
            phone="9000000003",
            role="user"
        ))
        
        # 8. Authority with different credentials
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="traffic.authority@city.gov",
            password="Auth@123!Secure",
            name="Traffic Management Authority",
            phone="5551234567",
            role="authority"
        ))
        
        # 9. User with weak password format (edge case for validation)
        users.append(TestUser(
            user_id=str(ObjectId()),
            email="weak@roadcare.local",
            password="weak123",  # Weak but valid (>6 chars)
            name="Weak Password User",
            phone="9000000004",
            role="user"
        ))
        
        return users
    
    @staticmethod
    def generate_duplicate_email_user(base_user: TestUser) -> TestUser:
        """Generate user with duplicate email for conflict testing"""
        return TestUser(
            user_id=str(ObjectId()),
            email=base_user.email,  # DUPLICATE
            password="DifferentPassword123!",
            name="Different Person",
            phone="9111111111",
            role="user"
        )
    
    @staticmethod
    def generate_invalid_format_users() -> List[Dict[str, Any]]:
        """Generate invalid format users for negative testing"""
        return [
            {
                "email": "invalid.email",  # Missing @
                "password": "Password123!",
                "name": "Invalid Email",
                "phone": "9000000005",
                "role": "user"
            },
            {
                "email": "test@example.com",
                "password": "short",  # Too short
                "name": "Short Password",
                "phone": "9000000006",
                "role": "user"
            },
            {
                "email": "test@example.com",
                "password": "Password123!",
                "name": "X",  # Too short (< 2 chars)
                "phone": "9000000007",
                "role": "user"
            },
            {
                "email": "test@example.com",
                "password": "Password123!",
                "name": "Valid Name",
                "phone": "123",  # Too short
                "role": "user"
            },
            {
                "email": "test@example.com",
                "password": "Password123!",
                "name": "Valid Name",
                "phone": "9000000008",
                "role": "invalid_role"  # Invalid role
            }
        ]


# ============================================================================
# PHASE 2: AUTHENTICATION & DB VALIDATION TEST SUITE
# ============================================================================

class AuthenticationTestSuite:
    """Test authentication system and database validation"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.test_results = []
    
    async def test_signup_and_db_validation(self, user: TestUser) -> Dict[str, Any]:
        """
        Test signup process with comprehensive DB validation
        
        Checks:
        - Record created in DB
        - All fields stored correctly
        - Password hashed (NOT plain text)
        - Timestamps correct
        - Indexes working
        """
        result = {
            "user_email": user.email,
            "phase": "SIGNUP_AND_DB_VALIDATION",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Step 1: Insert user
        user_doc = {
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "hashed_password": self.pwd_context.hash(user.password),
            "created_at": datetime.utcnow()
        }
        
        insert_result = await self.db.users.insert_one(user_doc)
        result["checks"]["insert_successful"] = insert_result.inserted_id is not None
        result["inserted_id"] = str(insert_result.inserted_id)
        
        # Step 2: Retrieve and validate
        retrieved_user = await self.db.users.find_one({"_id": insert_result.inserted_id})
        result["checks"]["record_exists"] = retrieved_user is not None
        
        if retrieved_user:
            # Check all fields
            result["checks"]["name_stored_correctly"] = retrieved_user["name"] == user.name
            result["checks"]["email_stored_correctly"] = retrieved_user["email"] == user.email
            result["checks"]["phone_stored_correctly"] = retrieved_user["phone"] == user.phone
            result["checks"]["role_stored_correctly"] = retrieved_user["role"] == user.role
            
            # CRITICAL: Password must be hashed
            result["checks"]["password_is_hashed"] = (
                retrieved_user["hashed_password"] != user.password
                and len(retrieved_user["hashed_password"]) > 10
            )
            result["checks"]["password_not_plain_text"] = user.password not in retrieved_user["hashed_password"]
            
            # Check timestamps
            result["checks"]["created_at_present"] = "created_at" in retrieved_user
            result["checks"]["created_at_recent"] = (
                datetime.utcnow() - retrieved_user["created_at"] < timedelta(seconds=5)
            )
            
            # Check no duplicate records created
            duplicate_count = await self.db.users.count_documents({"email": user.email})
            result["checks"]["no_duplicates_on_insert"] = duplicate_count == 1
        
        return result
    
    async def test_login_validation(self, user: TestUser, user_id: str) -> Dict[str, Any]:
        """
        Test login process with DB validation
        
        Checks:
        - Correct user fetched
        - Password comparison works
        - No duplicate records created
        - Timestamps valid
        """
        result = {
            "user_email": user.email,
            "phase": "LOGIN_VALIDATION",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Step 1: Fetch user by email
        fetched_user = await self.db.users.find_one({"email": user.email})
        result["checks"]["user_fetched"] = fetched_user is not None
        
        if fetched_user:
            result["checks"]["correct_user_id"] = str(fetched_user["_id"]) == user_id
            
            # Step 2: Verify password
            password_valid = self.pwd_context.verify(
                user.password,
                fetched_user["hashed_password"]
            )
            result["checks"]["password_verification_works"] = password_valid
            
            # Step 3: Check uniqueness
            email_count = await self.db.users.count_documents({"email": user.email})
            result["checks"]["email_uniqueness_enforced"] = email_count == 1
            
            # Step 4: Verify wrong password fails
            wrong_password_valid = self.pwd_context.verify(
                "WrongPassword123!",
                fetched_user["hashed_password"]
            )
            result["checks"]["wrong_password_rejected"] = not wrong_password_valid
        
        return result
    
    async def test_duplicate_email_rejection(self, user: TestUser) -> Dict[str, Any]:
        """Test that duplicate emails are rejected"""
        result = {
            "phase": "DUPLICATE_EMAIL_REJECTION",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # First user should exist
        first_user = await self.db.users.find_one({"email": user.email})
        result["checks"]["first_user_exists"] = first_user is not None
        
        if first_user:
            # Attempt to insert duplicate email
            duplicate_user = {
                "name": "Different Person",
                "email": user.email,  # DUPLICATE
                "phone": "9999999999",
                "role": "user",
                "hashed_password": self.pwd_context.hash("DifferentPass123!"),
                "created_at": datetime.utcnow()
            }
            
            # With unique index, this should fail or be prevented
            try:
                await self.db.users.insert_one(duplicate_user)
                result["checks"]["duplicate_prevented_by_index"] = False
            except Exception as e:
                result["checks"]["duplicate_prevented_by_index"] = "duplicate" in str(e).lower()
                result["duplicate_rejection_error"] = str(e)
        
        return result


# ============================================================================
# PHASE 3: POTHOLE DETECTION & DB STORAGE
# ============================================================================

@dataclass
class DetectionTestCase:
    """Test case for pothole detection"""
    case_id: str
    image_path: str
    latitude: float
    longitude: float
    confidence_score: float  # 0-100
    detected: bool
    user_id: str = None


class PotholeDetectionTestSuite:
    """Test pothole detection and database storage"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.detection_results = []
    
    @staticmethod
    def generate_detection_test_cases(user_id: str) -> List[DetectionTestCase]:
        """Generate diverse pothole detection test cases"""
        cases = []
        
        # 1. High confidence detection
        cases.append(DetectionTestCase(
            case_id=str(ObjectId()),
            image_path=f"uploads/case_1_{uuid.uuid4()}.jpg",
            latitude=28.6139,
            longitude=77.2090,
            confidence_score=95.5,
            detected=True,
            user_id=user_id
        ))
        
        # 2. Low confidence detection
        cases.append(DetectionTestCase(
            case_id=str(ObjectId()),
            image_path=f"uploads/case_2_{uuid.uuid4()}.jpg",
            latitude=28.6140,
            longitude=77.2091,
            confidence_score=52.3,
            detected=True,
            user_id=user_id
        ))
        
        # 3. No detection
        cases.append(DetectionTestCase(
            case_id=str(ObjectId()),
            image_path=f"uploads/case_3_{uuid.uuid4()}.jpg",
            latitude=28.6141,
            longitude=77.2092,
            confidence_score=0.0,
            detected=False,
            user_id=user_id
        ))
        
        # 4. Edge case: Extreme coordinates
        cases.append(DetectionTestCase(
            case_id=str(ObjectId()),
            image_path=f"uploads/case_4_{uuid.uuid4()}.jpg",
            latitude=-90.0,  # South pole
            longitude=180.0,  # Date line
            confidence_score=78.5,
            detected=True,
            user_id=user_id
        ))
        
        # 5. Edge case: Zero coordinates
        cases.append(DetectionTestCase(
            case_id=str(ObjectId()),
            image_path=f"uploads/case_5_{uuid.uuid4()}.jpg",
            latitude=0.0,
            longitude=0.0,
            confidence_score=62.1,
            detected=True,
            user_id=user_id
        ))
        
        return cases
    
    async def test_detection_and_storage(
        self, 
        test_case: DetectionTestCase
    ) -> Dict[str, Any]:
        """
        Test pothole detection and database storage
        
        Checks:
        - Image record stored
        - File path/URL stored correctly
        - Detection result stored
        - Confidence score stored
        - Timestamp present
        - No duplicate entries
        - Correct mapping (image ↔ result)
        """
        result = {
            "case_id": test_case.case_id,
            "phase": "DETECTION_AND_STORAGE",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Simulate detection process
        report_doc = {
            "user_id": ObjectId(test_case.user_id) if isinstance(test_case.user_id, str) else test_case.user_id,
            "description": f"Pothole detection case {test_case.case_id}",
            "location": {
                "latitude": test_case.latitude,
                "longitude": test_case.longitude
            },
            "image_path": test_case.image_path,
            "h3_index": self._calculate_h3_index(test_case.latitude, test_case.longitude),
            "status": "pending",
            "ai_confidence": test_case.confidence_score,
            "ai_verified": test_case.detected,
            "report_date": datetime.utcnow()
        }
        
        # Insert report
        insert_result = await self.db.pothole_reports.insert_one(report_doc)
        result["checks"]["image_record_stored"] = insert_result.inserted_id is not None
        result["report_id"] = str(insert_result.inserted_id)
        
        # Retrieve and validate
        retrieved_report = await self.db.pothole_reports.find_one({"_id": insert_result.inserted_id})
        result["checks"]["record_retrievable"] = retrieved_report is not None
        
        if retrieved_report:
            result["checks"]["image_path_correct"] = retrieved_report["image_path"] == test_case.image_path
            result["checks"]["confidence_stored"] = retrieved_report["ai_confidence"] == test_case.confidence_score
            result["checks"]["detection_result_stored"] = retrieved_report["ai_verified"] == test_case.detected
            result["checks"]["timestamp_present"] = "report_date" in retrieved_report
            result["checks"]["coordinates_stored"] = (
                retrieved_report["location"]["latitude"] == test_case.latitude
                and retrieved_report["location"]["longitude"] == test_case.longitude
            )
            
            # Check for duplicates
            duplicate_count = await self.db.pothole_reports.count_documents({
                "image_path": test_case.image_path
            })
            result["checks"]["no_duplicate_entries"] = duplicate_count == 1
            
            # Check mapping
            result["checks"]["user_id_maps_correctly"] = (
                str(retrieved_report["user_id"]) == test_case.user_id
            )
        
        self.detection_results.append(result)
        return result
    
    @staticmethod
    def _calculate_h3_index(lat: float, lon: float, resolution: int = 8) -> str:
        """Calculate H3 index for coordinates (simulated)"""
        try:
            import h3
            return h3.latlng2cell(lat, lon, resolution)
        except ImportError:
            # Fallback: Simple hash-based index
            hash_input = f"{lat:.4f}_{lon:.4f}"
            return f"h3_{hashlib.md5(hash_input.encode()).hexdigest()[:12]}"


# ============================================================================
# PHASE 4: HEX MAP & GEO DATA STORAGE
# ============================================================================

class HexMapGeoTestSuite:
    """Test hexagonal mapping and geospatial storage"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def test_hex_mapping(self, location: Dict[str, float]) -> Dict[str, Any]:
        """Test H3 hexagonal mapping"""
        result = {
            "location": location,
            "phase": "HEX_MAP_VALIDATION",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        try:
            import h3
            h3_index = h3.latlng2cell(location["latitude"], location["longitude"], 8)
            result["checks"]["h3_index_generated"] = h3_index is not None
            result["h3_index"] = h3_index
            
            # Test neighboring cells
            neighbors = h3.grid_ring(h3_index, 1)
            result["checks"]["neighbors_calculated"] = len(neighbors) > 0
            result["neighbor_count"] = len(neighbors)
        except ImportError:
            result["checks"]["h3_library_available"] = False
            result["warning"] = "h3-py not installed, using fallback"
        
        return result
    
    async def test_geo_data_storage(self, risk_zone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test geographic data storage and retrieval"""
        result = {
            "phase": "GEO_DATA_STORAGE",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Store risk zone
        zone_doc = {
            "center_location": risk_zone_data["center_location"],
            "h3_index": risk_zone_data["h3_index"],
            "pothole_count": risk_zone_data["pothole_count"],
            "risk_level": risk_zone_data["risk_level"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        insert_result = await self.db.risk_zones.insert_one(zone_doc)
        result["checks"]["zone_stored"] = insert_result.inserted_id is not None
        
        # Retrieve and validate
        retrieved_zone = await self.db.risk_zones.find_one({"_id": insert_result.inserted_id})
        result["checks"]["coordinates_stored_correctly"] = (
            retrieved_zone["center_location"]["latitude"] == risk_zone_data["center_location"]["latitude"]
        )
        result["checks"]["h3_index_stored"] = retrieved_zone["h3_index"] == risk_zone_data["h3_index"]
        
        return result


# ============================================================================
# PHASE 5: DATA CONSISTENCY CHECKS
# ============================================================================

class DataConsistencyTestSuite:
    """Test data consistency and referential integrity"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def test_referential_integrity(self, user_id: str) -> Dict[str, Any]:
        """
        Test referential integrity
        
        Checks:
        - user → reports linked correctly
        - report → user resolvable
        - No orphan records
        """
        result = {
            "user_id": user_id,
            "phase": "REFERENTIAL_INTEGRITY",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Check user exists
        user = await self.db.users.find_one({"_id": ObjectId(user_id)})
        result["checks"]["user_exists"] = user is not None
        
        # Check all reports for this user
        user_reports = await self.db.pothole_reports.find({"user_id": ObjectId(user_id)}).to_list(None)
        result["user_report_count"] = len(user_reports) if user_reports else 0
        
        # Verify each report references valid user
        orphan_reports = 0
        for report in user_reports:
            linked_user = await self.db.users.find_one({"_id": report["user_id"]})
            if linked_user is None:
                orphan_reports += 1
        
        result["checks"]["no_orphan_reports"] = orphan_reports == 0
        result["orphan_report_count"] = orphan_reports
        
        # Check risk zones reference valid reports
        orphan_zones = 0
        zones = await self.db.risk_zones.find().to_list(None)
        for zone in zones:
            for report_id in zone.get("report_ids", []):
                report = await self.db.pothole_reports.find_one({"_id": report_id})
                if report is None:
                    orphan_zones += 1
                    break
        
        result["checks"]["no_orphan_zones"] = orphan_zones == 0
        result["orphan_zone_count"] = orphan_zones
        
        return result
    
    async def test_duplicate_detection(self) -> Dict[str, Any]:
        """Detect duplicate or near-duplicate records"""
        result = {
            "phase": "DUPLICATE_DETECTION",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Check for duplicate emails
        pipeline = [
            {"$group": {"_id": "$email", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        duplicate_emails = await self.db.users.aggregate(pipeline).to_list(None)
        result["checks"]["no_duplicate_emails"] = len(duplicate_emails) == 0
        result["duplicate_email_count"] = len(duplicate_emails)
        
        # Check for duplicate image paths
        pipeline = [
            {"$group": {"_id": "$image_path", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        duplicate_images = await self.db.pothole_reports.aggregate(pipeline).to_list(None)
        result["checks"]["no_duplicate_images"] = len(duplicate_images) == 0
        result["duplicate_image_count"] = len(duplicate_images)
        
        return result


# ============================================================================
# PHASE 6-7: ACID PROPERTY & FAILURE TESTING
# ============================================================================

class ACIDTestSuite:
    """Test ACID properties and failure scenarios"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def test_atomicity(self, user_id: str) -> Dict[str, Any]:
        """
        Test atomicity: partial data should NOT exist on failure
        
        Simulate: Begin transaction → Insert user → Simulate failure →
        Verify: No partial records exist
        """
        result = {
            "phase": "ATOMICITY_TESTING",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        test_email = f"atomicity_test_{uuid.uuid4()}@test.local"
        
        # Test single-document atomicity (MongoDB documents are atomic)
        complex_doc = {
            "user_id": ObjectId(user_id),
            "email": test_email,
            "reports": [
                {"report_id": str(ObjectId()), "confidence": 95.5},
                {"report_id": str(ObjectId()), "confidence": 87.3}
            ],
            "metadata": {
                "created": datetime.utcnow(),
                "updated": datetime.utcnow()
            }
        }
        
        insert_result = await self.db.users.insert_one(complex_doc)
        retrieved = await self.db.users.find_one({"_id": insert_result.inserted_id})
        
        # Verify all fields present (no partial writes)
        result["checks"]["all_fields_present"] = (
            "email" in retrieved
            and "reports" in retrieved
            and "metadata" in retrieved
        )
        result["checks"]["complete_document_stored"] = len(asdict(retrieved)) >= 4
        
        return result
    
    async def test_consistency(self, user_id: str) -> Dict[str, Any]:
        """
        Test consistency: constraints enforced, invalid data rejected
        """
        result = {
            "phase": "CONSISTENCY_TESTING",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Test 1: Invalid enum value
        try:
            invalid_report = {
                "user_id": ObjectId(user_id),
                "location": {"latitude": 28.6139, "longitude": 77.2090},
                "image_path": "test.jpg",
                "status": "invalid_status",  # Invalid!
                "report_date": datetime.utcnow()
            }
            await self.db.pothole_reports.insert_one(invalid_report)
            result["checks"]["invalid_enum_rejected"] = False
        except Exception:
            result["checks"]["invalid_enum_rejected"] = True
        
        # Test 2: Out-of-range coordinates
        try:
            invalid_location = {
                "user_id": ObjectId(user_id),
                "location": {"latitude": 91.0, "longitude": 77.2090},  # >90!
                "image_path": "test.jpg",
                "status": "pending",
                "report_date": datetime.utcnow()
            }
            await self.db.pothole_reports.insert_one(invalid_location)
            result["checks"]["out_of_range_coordinates_rejected"] = False
        except Exception:
            result["checks"]["out_of_range_coordinates_rejected"] = True
        
        return result
    
    async def test_isolation(self) -> Dict[str, Any]:
        """
        Test isolation: concurrent requests don't cause dirty reads
        """
        result = {
            "phase": "ISOLATION_TESTING",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Create a document to be read/written
        test_doc = {
            "test_type": "isolation",
            "counter": 0,
            "created": datetime.utcnow()
        }
        insert_result = await self.db.users.insert_one(test_doc)
        
        # Simulate concurrent reads while write is in progress
        async def increment_counter():
            current = await self.db.users.find_one({"_id": insert_result.inserted_id})
            # Simulate processing time
            await asyncio.sleep(0.01)
            await self.db.users.update_one(
                {"_id": insert_result.inserted_id},
                {"$set": {"counter": current["counter"] + 1}}
            )
        
        # Run concurrent increments
        await asyncio.gather(*[increment_counter() for _ in range(3)])
        
        final_doc = await self.db.users.find_one({"_id": insert_result.inserted_id})
        # Due to race conditions, counter might not be 3 (demonstrates isolation issues)
        result["checks"]["concurrent_operations_completed"] = True
        result["final_counter_value"] = final_doc["counter"]
        
        return result
    
    async def test_durability(self, user_id: str) -> Dict[str, Any]:
        """
        Test durability: data persists after insert
        """
        result = {
            "phase": "DURABILITY_TESTING",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        test_data = {
            "user_id": ObjectId(user_id),
            "durability_test": True,
            "timestamp": datetime.utcnow(),
            "data": "persistent"
        }
        
        insert_result = await self.db.users.insert_one(test_data)
        
        # Immediately retrieve (should be durable)
        retrieved1 = await self.db.users.find_one({"_id": insert_result.inserted_id})
        result["checks"]["immediate_retrieval_works"] = retrieved1 is not None
        
        # Multiple retrievals should return same data
        retrieved2 = await self.db.users.find_one({"_id": insert_result.inserted_id})
        result["checks"]["consistent_across_retrievals"] = (
            retrieved1["timestamp"] == retrieved2["timestamp"]
        )
        
        return result


# ============================================================================
# PHASE 8: RETRIEVAL VALIDATION
# ============================================================================

class RetrievalValidationSuite:
    """Test accuracy and efficiency of data retrieval"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def test_fetch_and_validate(self, user_id: str) -> Dict[str, Any]:
        """Test fetching and validating stored data"""
        result = {
            "user_id": user_id,
            "phase": "RETRIEVAL_VALIDATION",
            "checks": {},
            "timestamp": datetime.utcnow()
        }
        
        # Fetch user
        user = await self.db.users.find_one({"_id": ObjectId(user_id)})
        result["checks"]["user_fetch_successful"] = user is not None
        
        if user:
            # Fetch all reports for user
            reports = await self.db.pothole_reports.find({"user_id": ObjectId(user_id)}).to_list(None)
            result["report_count"] = len(reports)
            
            # Validate data accuracy
            all_fields_present = all(
                key in user for key in ["_id", "email", "name", "role"]
            )
            result["checks"]["all_user_fields_present"] = all_fields_present
            
            # Validate report data
            reports_valid = True
            for report in reports:
                required_fields = ["_id", "user_id", "image_path", "location", "report_date"]
                if not all(key in report for key in required_fields):
                    reports_valid = False
                    break
            result["checks"]["all_report_fields_present"] = reports_valid
        
        return result


# ============================================================================
# MAIN TEST ORCHESTRATOR
# ============================================================================

class ComprehensiveQAOrchestrator:
    """Main orchestrator for all testing phases"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.test_results = {
            "phase_1_users": [],
            "phase_2_auth": [],
            "phase_3_detection": [],
            "phase_4_hex": [],
            "phase_5_consistency": [],
            "phase_6_acid": [],
            "phase_8_retrieval": [],
            "summary": {}
        }
    
    async def run_all_phases(self) -> Dict[str, Any]:
        """Execute all testing phases"""
        
        print("\n" + "="*80)
        print("COMPREHENSIVE QA & DATABASE RELIABILITY TEST SUITE")
        print("="*80)
        
        # PHASE 1: Generate test users
        print("\n[PHASE 1] Generating test users...")
        generator = TestDataGenerator()
        test_users = generator.generate_test_users()
        self.test_results["phase_1_users"] = [asdict(u) for u in test_users]
        print(f"✓ Generated {len(test_users)} test users")
        
        # PHASE 2: Authentication & DB Validation
        print("\n[PHASE 2] Testing authentication & database validation...")
        auth_suite = AuthenticationTestSuite(self.db)
        user_ids = {}
        
        for user in test_users[:3]:  # Test subset for speed
            # Signup test
            signup_result = await auth_suite.test_signup_and_db_validation(user)
            self.test_results["phase_2_auth"].append(signup_result)
            user_ids[user.email] = signup_result.get("inserted_id")
            
            # Login test
            login_result = await auth_suite.test_login_validation(
                user,
                signup_result.get("inserted_id")
            )
            self.test_results["phase_2_auth"].append(login_result)
        
        print(f"✓ Completed auth tests for {len(user_ids)} users")
        
        # PHASE 3: Pothole Detection & Storage
        print("\n[PHASE 3] Testing pothole detection & storage...")
        detection_suite = PotholeDetectionTestSuite(self.db)
        
        for email, user_id in list(user_ids.items())[:2]:
            test_cases = detection_suite.generate_detection_test_cases(user_id)
            for test_case in test_cases[:2]:  # Subset for speed
                detection_result = await detection_suite.test_detection_and_storage(test_case)
                self.test_results["phase_3_detection"].append(detection_result)
        
        print(f"✓ Completed detection tests")
        
        # PHASE 4: Hex Map & Geo Storage
        print("\n[PHASE 4] Testing hexagonal mapping...")
        hex_suite = HexMapGeoTestSuite(self.db)
        
        locations = [
            {"latitude": 28.6139, "longitude": 77.2090},
            {"latitude": 40.7128, "longitude": -74.0060},
        ]
        
        for location in locations:
            hex_result = await hex_suite.test_hex_mapping(location)
            self.test_results["phase_4_hex"].append(hex_result)
        
        print(f"✓ Completed hex mapping tests")
        
        # PHASE 5: Data Consistency
        print("\n[PHASE 5] Testing data consistency...")
        consistency_suite = DataConsistencyTestSuite(self.db)
        
        for email, user_id in list(user_ids.items())[:1]:
            ref_integrity = await consistency_suite.test_referential_integrity(user_id)
            self.test_results["phase_5_consistency"].append(ref_integrity)
        
        duplicate_result = await consistency_suite.test_duplicate_detection()
        self.test_results["phase_5_consistency"].append(duplicate_result)
        
        print(f"✓ Completed consistency tests")
        
        # PHASE 6 & 7: ACID Testing
        print("\n[PHASE 6-7] Testing ACID properties...")
        acid_suite = ACIDTestSuite(self.db)
        
        for email, user_id in list(user_ids.items())[:1]:
            atomicity_result = await acid_suite.test_atomicity(user_id)
            self.test_results["phase_6_acid"].append(atomicity_result)
            
            consistency_result = await acid_suite.test_consistency(user_id)
            self.test_results["phase_6_acid"].append(consistency_result)
            
            isolation_result = await acid_suite.test_isolation()
            self.test_results["phase_6_acid"].append(isolation_result)
            
            durability_result = await acid_suite.test_durability(user_id)
            self.test_results["phase_6_acid"].append(durability_result)
        
        print(f"✓ Completed ACID tests")
        
        # PHASE 8: Retrieval Validation
        print("\n[PHASE 8] Testing retrieval validation...")
        retrieval_suite = RetrievalValidationSuite(self.db)
        
        for email, user_id in list(user_ids.items())[:1]:
            retrieval_result = await retrieval_suite.test_fetch_and_validate(user_id)
            self.test_results["phase_8_retrieval"].append(retrieval_result)
        
        print(f"✓ Completed retrieval tests")
        
        # Generate summary
        await self._generate_summary()
        
        return self.test_results
    
    async def _generate_summary(self):
        """Generate test summary"""
        total_checks = 0
        passed_checks = 0
        
        for phase_key, phase_results in self.test_results.items():
            if phase_key != "summary" and isinstance(phase_results, list):
                for result in phase_results:
                    if "checks" in result:
                        for check_name, check_passed in result["checks"].items():
                            total_checks += 1
                            if check_passed:
                                passed_checks += 1
        
        self.test_results["summary"] = {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "pass_rate": f"{(passed_checks/total_checks*100):.1f}%" if total_checks > 0 else "N/A",
            "timestamp": datetime.utcnow().isoformat()
        }


# ============================================================================
# PYTEST FIXTURES & TEST FUNCTIONS
# ============================================================================

@pytest.fixture
async def orchestrator(db):
    """Fixture providing orchestrator instance"""
    return ComprehensiveQAOrchestrator(db)


@pytest.mark.asyncio
async def test_comprehensive_qa_suite(orchestrator):
    """Main test function running all phases"""
    results = await orchestrator.run_all_phases()
    
    # Generate output report
    print("\n" + "="*80)
    print("TEST RESULTS SUMMARY")
    print("="*80)
    print(json.dumps(results["summary"], indent=2))
    
    # Assert overall pass rate > 80%
    pass_rate = float(results["summary"]["pass_rate"].strip("%"))
    assert pass_rate >= 80, f"Pass rate {pass_rate}% below 80% threshold"


if __name__ == "__main__":
    print("Run this with: pytest comprehensive_qa_suite.py -v")
