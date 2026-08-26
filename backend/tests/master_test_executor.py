"""
MASTER TEST EXECUTOR
====================

Orchestrates all testing phases (1-11) and generates comprehensive reports
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# Import all test suites
from comprehensive_qa_suite import ComprehensiveQAOrchestrator
from test_performance_security_e2e import PerformanceSecurityE2EAggregator
from test_report_generator import ComprehensiveQAReportGenerator, generate_final_report


class MasterTestExecutor:
    """Execute all testing phases and generate reports"""
    
    def __init__(self, mongodb_uri: str = "mongodb://localhost:27017"):
        self.mongodb_uri = mongodb_uri
        self.db_name = "roadcare_qa_comprehensive"
        self.client = None
        self.db = None
        self.all_results = {}
    
    async def connect_to_db(self) -> bool:
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(self.mongodb_uri, serverSelectionTimeoutMS=5000)
            await self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print(f"✅ Connected to MongoDB: {self.mongodb_uri}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            print("   Ensure MongoDB is running locally or set TEST_MONGODB_URI environment variable")
            return False
    
    async def cleanup_db(self):
        """Clean up test database"""
        try:
            await self.db.command("dropDatabase")
            print("✅ Cleaned up test database")
        except Exception as e:
            print(f"⚠️ Could not cleanup database: {e}")
    
    async def run_phases_1_8(self):
        """Run phases 1-8 (Auth, Detection, Consistency, ACID, Retrieval)"""
        print("\n" + "="*100)
        print("EXECUTING PHASES 1-8: CORE TESTING")
        print("="*100)
        
        orchestrator = ComprehensiveQAOrchestrator(self.db)
        self.all_results = await orchestrator.run_all_phases()
        
        # Add summary
        print("\n[PHASES 1-8 SUMMARY]")
        summary = self.all_results.get("summary", {})
        print(f"Total Checks: {summary.get('total_checks', 'N/A')}")
        print(f"Passed: {summary.get('passed_checks', 'N/A')}")
        print(f"Failed: {summary.get('failed_checks', 'N/A')}")
        print(f"Pass Rate: {summary.get('pass_rate', 'N/A')}")
    
    async def run_phases_9_11(self):
        """Run phases 9-11 (Performance, Security, E2E)"""
        print("\n" + "="*100)
        print("EXECUTING PHASES 9-11: PERFORMANCE, SECURITY, END-TO-END")
        print("="*100)
        
        aggregator = PerformanceSecurityE2EAggregator(self.db)
        extended_results = await aggregator.run_all_phases()
        
        # Merge results
        self.all_results.update(extended_results)
        
        # Add summary
        print("\n[PHASES 9-11 SUMMARY]")
        summary = extended_results.get("summary", {})
        print(f"Total Checks: {summary.get('total_checks', 'N/A')}")
        print(f"Passed: {summary.get('passed_checks', 'N/A')}")
        print(f"Failed: {summary.get('failed_checks', 'N/A')}")
        print(f"Pass Rate: {summary.get('pass_rate', 'N/A')}")
    
    async def execute_all(self):
        """Execute all testing phases"""
        try:
            # Connect to database
            if not await self.connect_to_db():
                return False
            
            # Clean up before tests
            await self.cleanup_db()
            
            # Create indexes
            await self._create_indexes()
            
            # Run phases 1-8
            await self.run_phases_1_8()
            
            # Run phases 9-11
            await self.run_phases_9_11()
            
            # Generate reports
            await self.generate_reports()
            
            print("\n" + "="*100)
            print("✅ ALL TESTING PHASES COMPLETED SUCCESSFULLY")
            print("="*100)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Test execution failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            await self.cleanup_db()
            if self.client:
                self.client.close()
    
    async def _create_indexes(self):
        """Create database indexes for testing"""
        try:
            await self.db.users.create_index("email", unique=True)
            await self.db.pothole_reports.create_index("user_id")
            await self.db.pothole_reports.create_index("h3_index")
            await self.db.risk_zones.create_index("h3_index")
            print("✅ Database indexes created")
        except Exception as e:
            print(f"⚠️ Could not create indexes: {e}")
    
    async def generate_reports(self):
        """Generate comprehensive reports"""
        print("\n" + "="*100)
        print("GENERATING COMPREHENSIVE REPORTS")
        print("="*100)
        
        # Generate final report
        final_report = generate_final_report(self.all_results)
        
        # Save reports
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        # Text report
        text_filename = f"qa_test_report_{timestamp}.txt"
        with open(text_filename, "w") as f:
            f.write(final_report)
        print(f"✅ Text report saved: {text_filename}")
        
        # JSON report
        json_filename = f"qa_test_report_{timestamp}.json"
        with open(json_filename, "w") as f:
            json.dump(self.all_results, f, indent=2, default=str)
        print(f"✅ JSON report saved: {json_filename}")
        
        # Print summary to console
        print("\n" + final_report[:2000])
        print("\n... (see full report in files)")


# ============================================================================
# PYTEST INTEGRATION
# ============================================================================

import pytest


@pytest.mark.asyncio
async def test_master_qa_suite():
    """Main pytest entry point"""
    executor = MasterTestExecutor()
    success = await executor.execute_all()
    assert success, "Test suite failed"


# ============================================================================
# STANDALONE EXECUTION
# ============================================================================

async def main():
    """Standalone execution"""
    print("""
    ╔════════════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                        ║
    ║        COMPREHENSIVE QA & DATABASE RELIABILITY TEST SUITE                            ║
    ║                                                                                        ║
    ║   Testing System for:                                                                  ║
    ║   • Authentication system & user management                                            ║
    ║   • Pothole detection & image storage                                                  ║
    ║   • Hexagonal map visualization & geo data                                             ║
    ║   • Database integrity & persistence                                                   ║
    ║   • ACID compliance & transaction handling                                             ║
    ║   • Failure recovery & resilience                                                      ║
    ║   • Data consistency & referential integrity                                           ║
    ║   • Performance & scalability                                                          ║
    ║   • Security validation & encryption                                                   ║
    ║   • End-to-end workflows                                                               ║
    ║                                                                                        ║
    ║   11 Testing Phases | Full ACID Validation | Security Hardening | Performance         ║
    ║                                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    executor = MasterTestExecutor()
    success = await executor.execute_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # Check if running via pytest or standalone
    if "pytest" in sys.modules:
        print("Running via pytest...")
    else:
        # Standalone execution
        asyncio.run(main())
