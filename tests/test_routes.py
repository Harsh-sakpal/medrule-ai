"""
Flask Route and Web Application Test Suite for MedRule AI
Verifies all HTTP endpoints, session management, and template rendering.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret-key"
        self.client = app.test_client()

    def test_home_page(self):
        """Test GET / renders 200 with symptom checker UI."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MedRule", response.data)
        self.assertIn(b"Rule-Based Medical Diagnosis System", response.data)
        self.assertIn(b"Run Inference Engine", response.data)

    def test_forward_chaining_post(self):
        """Test POST /analyze with forward chaining symptoms."""
        response = self.client.post("/analyze", data={
            "symptoms": ["sneezing", "runny_nose", "sore_throat"],
            "inference_mode": "forward"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Common Cold-like Symptom Pattern", response.data)
        self.assertIn(b"Rule R1", response.data)

    def test_backward_chaining_post(self):
        """Test POST /analyze with backward chaining target goal."""
        response = self.client.post("/analyze", data={
            "symptoms": ["fever", "cough", "body_ache", "fatigue"],
            "inference_mode": "backward",
            "target_goal": "flu_pattern"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"GOAL SATISFIED", response.data)
        self.assertIn(b"Influenza-like", response.data)

    def test_emergency_red_flag_post(self):
        """Test POST /analyze with emergency symptom triggers emergency view."""
        response = self.client.post("/analyze", data={
            "symptoms": ["fever", "severe_chest_pain"],
            "inference_mode": "forward"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"URGENT MEDICAL ATTENTION REQUIRED", response.data)
        self.assertIn(b"Severe chest pain", response.data)

    def test_history_page(self):
        """Test GET /history renders correctly."""
        # Perform an analysis first to populate session
        self.client.post("/analyze", data={
            "symptoms": ["sneezing", "runny_nose", "sore_throat"],
            "inference_mode": "forward"
        })
        response = self.client.get("/history")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Analysis Audit History", response.data)
        self.assertIn(b"Analysis #1", response.data)

    def test_about_page(self):
        """Test GET /about renders architecture and academic metadata."""
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"System Architecture", response.data)
        self.assertIn(b"Harsh Rajendra Sakpal", response.data)

    def test_test_runner_page(self):
        """Test GET /tests runs unit test suite in browser."""
        response = self.client.get("/tests")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Automated Test Suite Verification", response.data)
        self.assertIn(b"Total Test Cases", response.data)

    def test_json_api_analyze(self):
        """Test POST /api/analyze returns valid JSON."""
        response = self.client.post("/api/analyze", json={
            "symptoms": ["itchy_eyes", "sneezing", "watery_nose"],
            "mode": "forward"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["inference_data"]["matched_rules"][0]["rule_id"], "R2")


if __name__ == "__main__":
    unittest.main()
