# QA Test Suite

Comprehensive backend test suite covering authentication, detection storage,
geospatial indexing, data consistency, ACID behavior, performance, security,
and end-to-end workflows.

## Quick Start

## Prerequisites
```bash
# Ensure MongoDB is running locally (port 27017)
mongod

# Or use Docker
docker run -d -p 27017:27017 mongo:latest
```

## Installation
```bash
cd backend
pip install -r requirements-dev.txt
pip install pytest pytest-asyncio motor h3 passlib[bcrypt]
```

## Run All Tests

### Option 1: Via Pytest
```bash
pytest tests/master_test_executor.py -v -s
```

### Option 2: Direct Python Execution
```bash
cd tests
python master_test_executor.py
```

### Option 3: Run Individual Phases
```bash
# Phases 1-8
pytest tests/comprehensive_qa_suite.py -v -s

# Phases 9-11
pytest tests/test_performance_security_e2e.py -v -s
```

## Output
Test reports are generated in:
- `qa_test_report_YYYYMMDD_HHMMSS.txt` - Formatted text report
- `qa_test_report_YYYYMMDD_HHMMSS.json` - Machine-readable JSON report

## Test Phases Overview

### PHASE 1: TEST USER GENERATION
**What it tests:** User data generation with edge cases
**Edge cases included:**
- Maximum length names (100 chars)
- Minimum length names (2 chars)
- International emails with special TLDs
- Long phone numbers (15 digits)
- Special characters (José, O'Connor)
- Both user and authority roles
- Weak passwords (valid but simple)

**Expected output:** 9+ test users with comprehensive coverage

### PHASE 2: AUTHENTICATION + DB VALIDATION
**What it tests:** User signup, login, and database integrity
**Validations:**
- ✓ User inserted into database
- ✓ All fields stored correctly
- ✓ Password hashed (NOT plain text)
- ✓ Timestamps recorded correctly
- ✓ Unique email constraint enforced
- ✓ Password verification works
- ✓ Wrong passwords rejected
- ✓ No duplicate records created

**Critical checks:**
- Password must be hashed with bcrypt
- Email must be unique (index enforced)
- Timestamps must be recent
- No partial inserts allowed

### PHASE 3: POTHOLE DETECTION + DB STORAGE
**What it tests:** Image upload, detection, and storage
**Test cases:**
1. High confidence detection (95.5%)
2. Low confidence detection (52.3%)
3. No detection (0%)
4. Extreme coordinates (-90°, 180°)
5. Zero coordinates (0°, 0°)

**Validations:**
- ✓ Image record stored
- ✓ File path preserved correctly
- ✓ Detection result stored
- ✓ Confidence score recorded
- ✓ Timestamp present
- ✓ No duplicate entries
- ✓ Correct user-image mapping

### PHASE 4: HEX MAP & GEO DATA STORAGE
**What it tests:** Hexagonal mapping and geographic data
**Validations:**
- ✓ H3 index generated correctly
- ✓ Neighboring cells calculated
- ✓ Coordinates stored accurately
- ✓ No coordinate drift

### PHASE 5: DATA CONSISTENCY CHECKS
**What it tests:** Referential integrity and duplicate detection
**Checks:**
- ✓ User → reports linked correctly
- ✓ No orphan records (reports without users)
- ✓ No orphan zones (zones without reports)
- ✓ No duplicate emails
- ✓ No duplicate image paths

**Failure conditions:**
- Orphan reports (report.user_id doesn't exist)
- Orphan zones (zone.report_ids contain missing reports)
- Duplicate emails
- Duplicate image paths

### PHASE 6-7: ACID PROPERTY TESTING (CRITICAL)
**What it tests:** ACID compliance - the core database guarantee

#### Atomicity
- All-or-nothing operations
- No partial writes
- Complex documents inserted completely or not at all
- Expected: All fields present or nothing

#### Consistency
- Data constraints enforced
- Invalid data rejected
- Out-of-range coordinates rejected
- Invalid enum values rejected
- Expected: Validation errors on bad data

#### Isolation
- Concurrent operations don't interfere
- No dirty reads during transactions
- Expected: Consistent reads across concurrent ops

#### Durability
- Data persists after insert
- Immediate retrieval works
- Multiple retrievals return same data
- Expected: Data remains after system restart

**Failure condition:** If any ACID property fails, DATABASE IS UNRELIABLE

### PHASE 8: RETRIEVAL VALIDATION
**What it tests:** Data retrieval accuracy and efficiency
**Validations:**
- ✓ User fetch successful
- ✓ All user fields present
- ✓ All report fields present
- ✓ Data accuracy verified

### PHASE 9: PERFORMANCE & SCALABILITY
**What it tests:** System performance under load

**Tests:**
1. Bulk Insert (100 users)
   - Insertion time
   - Throughput (users/sec)
   - Index impact

2. Query Performance
   - Indexed query speed (<100ms target)
   - Query efficiency

3. Concurrent Operations (10 concurrent)
   - Operations/sec
   - All ops complete successfully

4. Large Document Handling (1MB documents)
   - 16MB MongoDB limit enforcement
   - Retrieval performance

**Metrics:**
- Bulk insertion time
- Throughput (ops/sec)
- Query response time
- Concurrent operation success rate

### PHASE 10: SECURITY VALIDATION
**What it tests:** Security hardening and data protection

#### Password Security
- ✓ Passwords hashed (not plain text)
- ✓ Bcrypt strength validation
- ✓ Different passwords → different hashes
- ✓ Password verification works
- ✓ Wrong passwords rejected

#### Input Validation
- ✓ NoSQL injection prevented
- ✓ XSS payloads handled safely
- ✓ Invalid data rejected

#### Access Control
- ✓ Users cannot access others' data
- ✓ Role-based access enforced

#### Encryption at Rest
- ✓ Sensitive fields hashed
- ✓ Hashes cannot be reversed
- ✓ Password verification consistent

**Critical findings:**
- If any password is plain text → CRITICAL FAILURE
- If injection attacks succeed → CRITICAL FAILURE

### PHASE 11: END-TO-END FLOW VALIDATION
**What it tests:** Complete user workflows

#### Complete User Workflow
1. Signup → User created
2. Login → Password verified
3. Image Upload → File stored
4. Detection → Results recorded
5. Storage → Data persisted
6. Retrieval → Data accurate
7. Map Display → Zone created
8. Verification → Data integrity maintained

#### Multi-User Collaboration
- Multiple users report same pothole
- Zone aggregation works
- Risk level updated
- All reports linked correctly

## Understanding Test Results

### Pass/Fail Criteria

**Overall Success:** Pass rate ≥ 80%

**Critical Failures (must be 0):**
- Password stored in plain text
- Duplicate emails not prevented
- Orphan records exist
- ACID properties violated
- Data consistency issues

**Warnings (should be 0):**
- Query performance > 100ms
- Concurrent ops < 90% success rate
- Input validation gaps

## Troubleshooting

### MongoDB Connection Failed
```
❌ Failed to connect to MongoDB
Solution: Ensure MongoDB is running on localhost:27017
```

### Import Errors
```
ModuleNotFoundError: No module named 'motor'
Solution: pip install -r requirements-dev.txt
```

### Tests Timeout
```
Timeout: Test didn't complete in 30s
Solution: Increase CONFIG["test_timeout"] in test files
```

## Test Database
- Database name: `roadcare_qa_comprehensive`
- Automatically created and cleaned up
- All test data removed after execution
- Indexes recreated each run

## Performance Benchmarks (Expected)

| Operation | Expected Time | Threshold |
|-----------|---------------|-----------|
| User Insert | < 10ms | 50ms |
| Query (indexed) | < 20ms | 100ms |
| Bulk Insert (100) | < 500ms | 2s |
| Concurrent Ops (10) | < 100ms | 500ms |

## Security Checklist

After running tests, verify:
- [ ] All passwords hashed (never plain text)
- [ ] Email uniqueness enforced
- [ ] No orphan records
- [ ] ACID properties validated
- [ ] Input validation working
- [ ] Query performance acceptable
- [ ] Concurrent operations stable

## Next Steps

1. **Fix any critical failures** before deployment
2. **Optimize performance** if benchmarks exceeded
3. **Harden security** per recommendations
4. **Implement monitoring** for production
5. **Schedule regular testing** (pre-deployment)

## Advanced Usage

### Custom Test Configuration
```python
# In test files, modify CONFIG:
CONFIG = {
    "db_name": "custom_test_db",
    "mongodb_uri": "mongodb://custom-host:27017",
    "test_timeout": 60,
    "concurrent_users": 20,
}
```

### Generate Report Only
```python
from test_report_generator import ComprehensiveQAReportGenerator
generator = ComprehensiveQAReportGenerator()
# Add results...
report_text = generator.generate_text_report()
json_report = generator.to_json()
```

### Run Single Phase
```python
from comprehensive_qa_suite import AuthenticationTestSuite
auth_suite = AuthenticationTestSuite(db)
result = await auth_suite.test_signup_and_db_validation(user)
```

## Test Suite Architecture

```
Master Test Executor
├── Phases 1-8 (Core)
│   ├── Phase 1: User Generation
│   ├── Phase 2: Authentication
│   ├── Phase 3: Detection
│   ├── Phase 4: Hex Mapping
│   ├── Phase 5: Consistency
│   ├── Phase 6: ACID
│   └── Phase 8: Retrieval
├── Phases 9-11 (Extended)
│   ├── Phase 9: Performance
│   ├── Phase 10: Security
│   └── Phase 11: End-to-End
└── Report Generator
    ├── Text Report
    └── JSON Report
```

## Support

For issues or improvements to the test suite:
1. Check test logs for specific errors
2. Review MongoDB connection settings
3. Verify all dependencies installed
4. Check data consistency reports
5. Review security findings


