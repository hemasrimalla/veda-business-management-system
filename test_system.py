"""
test_system.py
--------------
Automated test suite verifying all components of the Veda Technology
Business & Service Management System.
"""

import os
import sys
import unittest
from datetime import datetime

# Set module lookup path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

from models import Service, Program, Inquiry
import storage
import validators
import search_filter
import reports


class TestVedaSystem(unittest.TestCase):
    """Test suite covering domain models, persistence, validation, search, and reports."""

    def setUp(self):
        storage.ensure_data_directory()
        storage.initialize_storage()
        self.services = storage.load_services()
        self.programs = storage.load_programs()
        self.inquiries = storage.load_inquiries()

    def test_seed_data_counts(self):
        """Verify pre-population of 8-10 records per file."""
        self.assertGreaterEqual(len(self.services), 8)
        self.assertGreaterEqual(len(self.programs), 8)
        self.assertGreaterEqual(len(self.inquiries), 8)

    def test_service_model_serialization(self):
        """Test Service to_dict and from_dict."""
        srv = Service("SRV-999", "Test AI Service", "AI & ML", "Test Description", 4500.50, "Active")
        d = srv.to_dict()
        self.assertEqual(d["id"], "SRV-999")
        self.assertEqual(d["price"], 4500.50)

        restored = Service.from_dict(d)
        self.assertEqual(restored.id, srv.id)
        self.assertEqual(restored.name, srv.name)
        self.assertEqual(restored.price, srv.price)
        self.assertEqual(restored.status, "Active")

    def test_program_model_serialization(self):
        """Test Program to_dict and from_dict."""
        prg = Program("PRG-999", "Python Mastery", "Training", "8 Weeks", 600.0, 30, "Open")
        d = prg.to_dict()
        self.assertEqual(d["title"], "Python Mastery")
        self.assertEqual(d["fee"], 600.0)

        restored = Program.from_dict(d)
        self.assertEqual(restored.title, prg.title)
        self.assertEqual(restored.type, "Training")
        self.assertEqual(restored.seats, 30)

    def test_inquiry_model_and_audit_history(self):
        """Test Inquiry to_dict, from_dict, and status updates."""
        inq = Inquiry("INQ-999", "John Doe", "john@example.com", "+1-5551234567", "Cloud", "Need cloud help", "2026-11-01", "New")
        self.assertEqual(len(inq.history), 1)
        inq.add_status_update("In Progress", "Called customer")
        self.assertEqual(inq.status, "In Progress")
        self.assertEqual(len(inq.history), 2)
        self.assertEqual(inq.history[-1]["note"], "Called customer")

        d = inq.to_dict()
        restored = Inquiry.from_dict(d)
        self.assertEqual(restored.status, "In Progress")
        self.assertEqual(len(restored.history), 2)

    def test_validators(self):
        """Test email, phone, non-empty, and date format validation."""
        self.assertTrue(validators.validate_email("user@domain.com"))
        self.assertTrue(validators.validate_email("first.last+tag@company.co.in"))
        self.assertFalse(validators.validate_email("invalid-email"))
        self.assertFalse(validators.validate_email("@missinguser.com"))

        self.assertTrue(validators.validate_phone("+91-9876543210"))
        self.assertTrue(validators.validate_phone("9876543210"))
        self.assertTrue(validators.validate_phone("+1 (555) 234-5678"))
        self.assertFalse(validators.validate_phone("123"))  # too short
        self.assertFalse(validators.validate_phone("not-a-number"))

        self.assertTrue(validators.validate_non_empty("Valid String"))
        self.assertFalse(validators.validate_non_empty("   "))

        self.assertTrue(validators.validate_date_format("2026-11-05"))
        self.assertFalse(validators.validate_date_format("2026-13-45"))
        self.assertFalse(validators.validate_date_format("05/11/2026"))

    def test_id_generation(self):
        """Test auto sequential ID generation."""
        next_srv_id = storage.generate_service_id(self.services)
        self.assertTrue(next_srv_id.startswith("SRV-"))
        next_prg_id = storage.generate_program_id(self.programs)
        self.assertTrue(next_prg_id.startswith("PRG-"))
        next_inq_id = storage.generate_inquiry_id(self.inquiries)
        self.assertTrue(next_inq_id.startswith("INQ-"))

    def test_search_and_filter(self):
        """Test search and multi-criteria filtering."""
        # Services search
        web_services = search_filter.search_services(self.services, "web")
        self.assertGreater(len(web_services), 0)

        # Services category filter
        cloud_services = search_filter.filter_services_by_category(self.services, "Cloud")
        self.assertGreater(len(cloud_services), 0)

        # Services price range filter
        mid_priced = search_filter.filter_services_by_price_range(self.services, min_price=3000.0, max_price=4500.0)
        self.assertGreater(len(mid_priced), 0)
        for s in mid_priced:
            self.assertTrue(3000.0 <= s.price <= 4500.0)

        # Programs search
        ml_progs = search_filter.search_programs(self.programs, "Machine Learning")
        self.assertGreater(len(ml_progs), 0)

        # Programs type filter
        internships = search_filter.filter_programs_by_type(self.programs, "Internship")
        self.assertGreater(len(internships), 0)
        for p in internships:
            self.assertEqual(p.type, "Internship")

        # Inquiries status filter
        resolved_inqs = search_filter.filter_inquiries_by_status(self.inquiries, "Resolved")
        self.assertGreater(len(resolved_inqs), 0)
        for i in resolved_inqs:
            self.assertEqual(i.status, "Resolved")

    def test_reports_and_metrics(self):
        """Test report calculations, formatting, and file export."""
        metrics = reports.calculate_metrics(self.services, self.programs, self.inquiries)
        self.assertIn("total_services", metrics)
        self.assertIn("total_programs", metrics)
        self.assertIn("total_inquiries", metrics)
        self.assertGreater(metrics["active_service_catalog_value"], 0)
        self.assertGreater(metrics["resolution_rate"], 0)

        report_txt = reports.generate_report_text(self.services, self.programs, self.inquiries)
        self.assertIn("VEDA TECHNOLOGY", report_txt)
        self.assertIn("EXECUTIVE BUSINESS REPORT", report_txt)
        self.assertIn("REVENUE POTENTIAL", report_txt)

        export_target = os.path.join(PROJECT_DIR, "sample_output", "test_report.txt")
        success = reports.export_report_to_file(report_txt, export_target)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(export_target))
        if os.path.exists(export_target):
            os.remove(export_target)


if __name__ == "__main__":
    unittest.main()
