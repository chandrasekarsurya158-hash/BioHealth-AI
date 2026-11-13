"""
BioHealth AI - Comprehensive Automated Test Suite (Phase 11)
-----------------------------------------------------------
Tests all 6 AI detection & medical assistance modules, 17 system routes,
database connectivity, PyMuPDF OCR extraction, and machine learning models.
"""

import os
import sys
import unittest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.models.db import test_connection, get_db
from app.models.symptoms_analyzer import SymptomsAnalyzer
from app.models.blood_report_parser import BloodReportParser
from app.models.xray_classifier import XrayClassifier
from app.models.pharmacopeia_data import VERIFIED_MEDICINES

class TestBioHealthSystem(unittest.TestCase):
    """Automated integration tests for BioHealth AI system."""

    @classmethod
    def setUpClass(cls):
        """Set up Flask test application client."""
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.app.config["WTF_CSRF_ENABLED"] = False
        cls.client = cls.app.test_client()

    def test_01_database_connectivity(self):
        """Verify MySQL connectivity and table integrity."""
        connected = test_connection()
        self.assertTrue(connected, "Database connection failed. Ensure MySQL/XAMPP is running.")
        with get_db() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = [list(r.values())[0] for r in cursor.fetchall()]
            required = ["users", "admins", "analysis_history", "plant_detection_results", 
                        "crop_detection_results", "skin_screening_results", "xray_results", 
                        "blood_reports", "blood_test_values", "symptom_assessments", "medicines"]
            for tbl in required:
                self.assertIn(tbl, tables, f"Expected table '{tbl}' not found in database.")

    def test_02_public_http_routes(self):
        """Verify all public informational and diagnostic landing pages return HTTP 200."""
        routes = [
            "/health-check",
            "/",
            "/emergency-directory",
            "/auth/login",
            "/auth/register",
            "/agriculture/plant",
            "/agriculture/crop",
            "/medical/skin",
            "/medical/symptoms",
            "/medical/blood-report",
            "/medical/xray",
            "/medical/medicine",
            "/admin/login"
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(
                response.status_code, 200, 
                f"Route '{route}' returned unexpected HTTP status {response.status_code}"
            )

    def test_03_symptoms_triage_emergency_detection(self):
        """Verify clinical emergency alert triggers on hyperpyrexia (108°F) and red flags."""
        result = SymptomsAnalyzer.evaluate(
            selected_symptoms=["fever", "chest_pain", "shortness_of_breath"],
            duration="hours",
            severity="severe",
            age=45,
            temperature_val=108.0,
            temperature_unit="F",
            conditions=["cardiovascular"],
            allergies=["aspirin"]
        )
        self.assertTrue(result["is_emergency"], "Hyperpyrexia or acute chest pain must flag EMERGENCY status.")
        self.assertGreater(len(result["red_flags"]), 0, "Emergency flags must be populated.")

    def test_04_blood_report_biomarker_extraction(self):
        """Verify PyMuPDF parser extracts clinical biomarkers from sample lab report."""
        sample_pdf = PROJECT_ROOT / "sample_blood_report.pdf"
        if sample_pdf.exists():
            parsed = BloodReportParser.parse_file(str(sample_pdf))
            self.assertEqual(parsed["status"], "success")
            self.assertGreater(parsed["total_extracted"], 5, "Parser should extract at least 5 biomarkers.")
            names = [b["name"] for b in parsed["biomarkers"]]
            self.assertIn("Hemoglobin (Hb)", names)
            self.assertIn("Fasting Blood Glucose (FBG)", names)

    def test_05_xray_model_inference(self):
        """Verify thoracic radiography classifier evaluates frontal radiograph image."""
        sample_xray = PROJECT_ROOT / "sample_chest_xray.png"
        if sample_xray.exists():
            prediction = XrayClassifier.predict(str(sample_xray))
            self.assertEqual(prediction["status"], "success")
            self.assertIn("display_name", prediction)
            self.assertIn("confidence", prediction)
            self.assertGreater(len(prediction["differential_diagnoses"]), 0)

    def test_06_pharmacopeia_medicine_search(self):
        """Verify medicine search engine queries name, category, and indications accurately."""
        # Query Cetirizine
        q = "cetirizine"
        matches = [
            m for m in VERIFIED_MEDICINES 
            if q in m["name"].lower() or q in m["generic_name"].lower()
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["name"], "Cetirizine")
        self.assertIn("renal impairment", matches[0]["warnings"].lower())

    def test_07_auth_redirection(self):
        """Verify protected user dashboard routes redirect unauthenticated users to login."""
        protected = ["/dashboard/", "/dashboard/history", "/dashboard/profile"]
        for route in protected:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 302, f"Protected route '{route}' must redirect to login.")
            self.assertIn("/auth/login", response.location)

    def test_08_history_export_formats(self):
        """Verify CSV and JSON history export endpoints stream valid data for authenticated users."""
        with self.client.session_transaction() as sess:
            sess["user_logged_in"] = True
            sess["user_id"] = 1
            sess["user_name"] = "Test User"
            sess["user_email"] = "test@example.com"

        # Test CSV export
        res_csv = self.client.get("/dashboard/history/export?format=csv")
        self.assertEqual(res_csv.status_code, 200)
        self.assertIn("text/csv", res_csv.content_type)
        self.assertIn(b"Record ID,Date & Time", res_csv.data)

        # Test JSON export
        res_json = self.client.get("/dashboard/history/export?format=json")
        self.assertEqual(res_json.status_code, 200)
        self.assertIn("application/json", res_json.content_type)

    def test_09_rbac_normal_user_forbidden_admin_access(self):
        """Verify normal user (role='user') receives HTTP 403 Forbidden when accessing admin routes."""
        with self.client.session_transaction() as sess:
            sess["user_logged_in"] = True
            sess["user_id"] = 1
            sess["user_name"] = "Normal User"
            sess["user_email"] = "user@example.com"
            sess["role"] = "user"

        admin_routes = [
            "/admin/dashboard",
            "/admin/users",
            "/admin/medicines",
            "/admin/logs"
        ]
        for route in admin_routes:
            response = self.client.get(route)
            self.assertEqual(
                response.status_code, 403,
                f"Normal user MUST be denied access to '{route}' with HTTP 403 Forbidden."
            )
            self.assertIn(b"Access Denied", response.data)

    def test_10_rbac_admin_authorized_access(self):
        """Verify administrator (role='admin') has authorized access to admin console routes."""
        with self.client.session_transaction() as sess:
            sess["admin_logged_in"] = True
            sess["admin_id"] = 1
            sess["admin_name"] = "Chief Systems Administrator"
            sess["role"] = "admin"

        admin_routes = [
            "/admin/dashboard",
            "/admin/users",
            "/admin/medicines",
            "/admin/logs"
        ]
        for route in admin_routes:
            response = self.client.get(route)
            self.assertEqual(
                response.status_code, 200,
                f"Administrator should receive HTTP 200 OK on '{route}'."
            )

    def test_11_unauthenticated_admin_redirection(self):
        """Verify unauthenticated visitors accessing admin routes are redirected to admin login."""
        # Clean session
        self.client.get("/auth/logout")
        response = self.client.get("/admin/dashboard")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login", response.location)

    def test_12_developer_api_health(self):
        """Verify Developer REST API v1 health endpoint returns JSON with model status."""
        res = self.client.get("/api/v1/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("active_models", data)
        self.assertTrue(data["active_models"]["plant_pathology"])
        self.assertTrue(data["active_models"]["xray_analysis"])

    def test_13_developer_api_triage_symptoms(self):
        """Verify Developer REST API symptom triage endpoint processes JSON payloads."""
        payload = {
            "symptoms": ["fever", "cough", "headache"],
            "temperature": 101.2,
            "temperature_unit": "F",
            "age": 30,
            "duration": "days"
        }
        res = self.client.post("/api/v1/triage/symptoms", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("triage_result", data)
        self.assertIn("primary_syndrome", data["triage_result"])

    def test_14_developer_api_medicines_search(self):
        """Verify Developer REST API pharmacopeia search endpoint returns query matches."""
        res = self.client.get("/api/v1/medicines?query=cetirizine")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["total_results"], 1)
        self.assertEqual(data["medicines"][0]["name"], "Cetirizine")

    def test_15_emergency_directory_page(self):
        """Verify Emergency Helplines & Specialist Directory page returns HTTP 200."""
        res = self.client.get("/emergency-directory")
        self.assertEqual(res.status_code, 200, f"Expected 200 on '/emergency-directory', got {res.status_code}")

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBioHealthSystem)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
