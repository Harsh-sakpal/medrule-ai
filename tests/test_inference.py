"""
Automated Test Suite for MedRule AI
Rule-Based Medical Diagnosis Educational Expert System
SPPU TE Computer Engineering - Artificial Intelligence Mini-Project

Test Cases:
TC-01: Forward Chaining - Common Cold Pattern Match
TC-02: Forward Chaining - Allergy Pattern Match
TC-03: Forward Chaining - Flu Pattern Match
TC-04: Backward Chaining - Goal Satisfied
TC-05: Backward Chaining - Goal Not Satisfied
TC-06: Input Validation - Empty Symptom Set
TC-07: Uncertainty Handling - Unmatched Symptoms
TC-08: Emergency Red-Flag Warning Detection Priority
TC-09: Input Validation - Invalid Inference Method
TC-10: Forward Chaining - Sinusitis Pattern Match
"""

import unittest
import sys
import os

# Ensure parent directory is in path for module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from inference_engine import (
    process_diagnosis_request,
    ValidationError,
    EmergencyFilter,
    ForwardChainingEngine,
    BackwardChainingEngine
)

class TestMedRuleAI(unittest.TestCase):

    def test_tc01_forward_common_cold_match(self):
        """TC-01: Verify forward chaining correctly fires Common Cold rule (R1)."""
        symptoms = ["sneezing", "runny_nose", "sore_throat"]
        response = process_diagnosis_request(symptoms, inference_mode="forward")
        
        self.assertTrue(response["success"])
        self.assertFalse(response["is_emergency"])
        inf_data = response["inference_data"]
        self.assertFalse(inf_data["is_uncertain"])
        self.assertGreater(len(inf_data["matched_rules"]), 0)
        self.assertEqual(inf_data["matched_rules"][0]["rule_id"], "R1")
        self.assertEqual(inf_data["matched_rules"][0]["hypothesis_id"], "common_cold_pattern")

    def test_tc02_forward_allergy_match(self):
        """TC-02: Verify forward chaining correctly fires Allergy rule (R2)."""
        symptoms = ["itchy_eyes", "sneezing", "watery_nose"]
        response = process_diagnosis_request(symptoms, inference_mode="forward")
        
        self.assertTrue(response["success"])
        inf_data = response["inference_data"]
        matched_rule_ids = [r["rule_id"] for r in inf_data["matched_rules"]]
        self.assertIn("R2", matched_rule_ids)

    def test_tc03_forward_flu_match(self):
        """TC-03: Verify forward chaining correctly fires Flu-like Illness rule (R3)."""
        symptoms = ["fever", "cough", "body_ache", "fatigue"]
        response = process_diagnosis_request(symptoms, inference_mode="forward")
        
        self.assertTrue(response["success"])
        inf_data = response["inference_data"]
        matched_rule_ids = [r["rule_id"] for r in inf_data["matched_rules"]]
        self.assertIn("R3", matched_rule_ids)

    def test_tc04_backward_goal_satisfied(self):
        """TC-04: Verify backward chaining succeeds when target goal conditions are met."""
        symptoms = ["fever", "cough", "body_ache", "fatigue"]
        response = process_diagnosis_request(
            symptoms,
            inference_mode="backward",
            target_goal="flu_pattern"
        )
        
        self.assertTrue(response["success"])
        inf_data = response["inference_data"]
        self.assertTrue(inf_data["is_goal_satisfied"])
        self.assertEqual(inf_data["target_hypothesis_id"], "flu_pattern")

    def test_tc05_backward_goal_not_satisfied(self):
        """TC-05: Verify backward chaining reports goal unsatisfied when required conditions missing."""
        symptoms = ["fever", "cough"]  # Missing body_ache, fatigue for flu
        response = process_diagnosis_request(
            symptoms,
            inference_mode="backward",
            target_goal="allergy_pattern"
        )
        
        self.assertTrue(response["success"])
        inf_data = response["inference_data"]
        self.assertFalse(inf_data["is_goal_satisfied"])
        self.assertGreater(len(inf_data["rule_evaluations"][0]["missing_conditions"]), 0)

    def test_tc06_empty_symptoms_validation(self):
        """TC-06: Verify proper exception handling when symptom selection is empty."""
        with self.assertRaises(ValidationError):
            process_diagnosis_request([], inference_mode="forward")

    def test_tc07_unmatched_symptoms_uncertainty(self):
        """TC-07: Verify proper uncertainty reporting when input facts do not satisfy any rule."""
        symptoms = ["fatigue"]  # Single symptom insufficient for any rule
        response = process_diagnosis_request(symptoms, inference_mode="forward")
        
        self.assertTrue(response["success"])
        inf_data = response["inference_data"]
        self.assertTrue(inf_data["is_uncertain"])
        self.assertEqual(len(inf_data["matched_rules"]), 0)

    def test_tc08_emergency_detection_priority(self):
        """TC-08: Verify emergency symptoms take absolute priority and halt ordinary evaluation."""
        symptoms = ["fever", "cough", "severe_chest_pain"]
        response = process_diagnosis_request(symptoms, inference_mode="forward")
        
        self.assertTrue(response["success"])
        self.assertTrue(response["is_emergency"])
        emergency = response["emergency_data"]
        self.assertEqual(emergency["severity"], "CRITICAL")
        detected_ids = [d["id"] for d in emergency["detected"]]
        self.assertIn("severe_chest_pain", detected_ids)

    def test_tc09_invalid_inference_mode(self):
        """TC-09: Verify ValidationError is raised when inference mode is unrecognized."""
        with self.assertRaises(ValidationError):
            process_diagnosis_request(["fever"], inference_mode="random_mode")

    def test_tc10_sinusitis_match(self):
        """TC-10: Verify forward chaining matches Sinusitis rule (R4)."""
        symptoms = ["headache", "facial_pressure", "nasal_congestion"]
        response = process_diagnosis_request(symptoms, inference_mode="forward")
        
        self.assertTrue(response["success"])
        inf_data = response["inference_data"]
        matched_rule_ids = [r["rule_id"] for r in inf_data["matched_rules"]]
        self.assertIn("R4", matched_rule_ids)


if __name__ == "__main__":
    unittest.main()
