"""
Inference Engine Module for MedRule AI
Rule-Based Medical Diagnosis Educational Expert System
SPPU TE Computer Engineering - Artificial Intelligence Mini-Project

Implements:
1. Input Validation & Pre-processing
2. Emergency Red-Flag Warning Filter (Highest Priority)
3. Forward Chaining Engine (Data-Driven Reasoning)
4. Backward Chaining Engine (Goal-Driven Reasoning)
5. Explainable Reasoning Trace Generator
"""

from typing import List, Dict, Any, Optional, Set
from knowledge_base import (
    RULES,
    EMERGENCY_SYMPTOMS,
    ALL_VALID_SYMPTOMS,
    HYPOTHESES,
    get_symptom_name
)

class ValidationError(Exception):
    """Custom exception raised when user input is invalid."""
    pass


class EmergencyFilter:
    """Evaluates whether any critical red-flag emergency symptoms are present."""

    @staticmethod
    def evaluate(symptoms: Set[str]) -> Optional[Dict[str, Any]]:
        detected_emergencies = []
        for symptom_id in symptoms:
            if symptom_id in EMERGENCY_SYMPTOMS:
                detected_emergencies.append({
                    "id": symptom_id,
                    "name": get_symptom_name(symptom_id),
                    "warning": EMERGENCY_SYMPTOMS[symptom_id]
                })

        if detected_emergencies:
            return {
                "is_emergency": True,
                "severity": "CRITICAL",
                "detected": detected_emergencies,
                "alert_title": "URGENT MEDICAL ATTENTION REQUIRED",
                "message": (
                    "One or more acute red-flag symptoms have been indicated. "
                    "Rule-based educational screening cannot handle emergency conditions. "
                    "Please contact emergency services (e.g., dial 112 / 108 / 911) or "
                    "visit the nearest emergency room immediately."
                ),
                "action_items": [
                    "Call for immediate emergency ambulance / medical transport.",
                    "Do not attempt home remedies or wait for online diagnosis.",
                    "Keep patient calm, rested, and monitored until medical assistance arrives."
                ]
            }
        return None


class ForwardChainingEngine:
    """
    Data-driven reasoning engine.
    Begins with user-supplied facts (symptoms) and systematically checks
    which production rules in the knowledge base have their antecedents satisfied.
    """

    @staticmethod
    def run(facts: Set[str]) -> Dict[str, Any]:
        reasoning_trace: List[Dict[str, Any]] = []
        matched_rules: List[Dict[str, Any]] = []
        partial_matches: List[Dict[str, Any]] = []

        step_counter = 1

        for rule in RULES:
            rule_id = rule["id"]
            rule_antecedents = set(rule["antecedents"])
            min_required = rule.get("min_matches", len(rule_antecedents))

            satisfied_conditions = rule_antecedents.intersection(facts)
            missing_conditions = rule_antecedents.difference(facts)

            match_count = len(satisfied_conditions)
            total_conditions = len(rule_antecedents)
            match_percentage = round((match_count / total_conditions) * 100, 1)

            trace_entry = {
                "step": step_counter,
                "rule_id": rule_id,
                "hypothesis": rule["conclusion"],
                "total_conditions": total_conditions,
                "satisfied_count": match_count,
                "satisfied_conditions": [get_symptom_name(s) for s in satisfied_conditions],
                "missing_conditions": [get_symptom_name(s) for s in missing_conditions],
                "match_percentage": match_percentage
            }

            # Check if rule fires
            if match_count >= min_required:
                trace_entry["status"] = "FIRED"
                trace_entry["explanation"] = rule["explanation"]
                matched_rules.append({
                    "rule_id": rule_id,
                    "hypothesis": rule["conclusion"],
                    "hypothesis_id": rule["hypothesis_id"],
                    "category": rule["category"],
                    "matched_symptoms": [get_symptom_name(s) for s in satisfied_conditions],
                    "explanation": rule["explanation"],
                    "recommendation": rule["recommendation"],
                    "confidence_label": "High Compatibility (Educational Rule Match)"
                })
            elif match_count > 0:
                trace_entry["status"] = "PARTIAL_MATCH"
                trace_entry["explanation"] = f"Condition threshold not met ({match_count}/{min_required} required)."
                partial_matches.append({
                    "rule_id": rule_id,
                    "hypothesis": rule["conclusion"],
                    "matched_symptoms": [get_symptom_name(s) for s in satisfied_conditions],
                    "missing_symptoms": [get_symptom_name(s) for s in missing_conditions],
                    "match_percentage": match_percentage
                })
            else:
                trace_entry["status"] = "NOT_MATCHED"
                trace_entry["explanation"] = "No overlapping symptoms observed for this rule."

            reasoning_trace.append(trace_entry)
            step_counter += 1

        is_uncertain = len(matched_rules) == 0

        return {
            "mode": "forward",
            "mode_label": "Forward Chaining (Data-Driven Reasoning)",
            "facts_provided": [get_symptom_name(s) for s in facts],
            "facts_count": len(facts),
            "matched_rules": matched_rules,
            "partial_matches": partial_matches,
            "reasoning_trace": reasoning_trace,
            "is_uncertain": is_uncertain,
            "conclusion_summary": (
                f"{len(matched_rules)} rule(s) satisfied based on provided facts."
                if not is_uncertain
                else "Uncertain Result: The entered facts do not satisfy any predefined rule in the knowledge base."
            ),
            "guidance": (
                "Review the matched patterns and step-by-step reasoning trace below."
                if not is_uncertain
                else "The system cannot determine an illustrative pattern. Different medical conditions share symptoms. Always consult a qualified medical professional for proper diagnostic examination."
            )
        }


class BackwardChainingEngine:
    """
    Goal-driven reasoning engine.
    Begins with a target hypothesis chosen by the user or system,
    identifies rules establishing that hypothesis, and inspects whether
    the required supporting facts are present.
    """

    @staticmethod
    def run(target_hypothesis_id: str, facts: Set[str]) -> Dict[str, Any]:
        # Locate target hypothesis metadata
        target_meta = next(
            (h for h in HYPOTHESES if h["id"] == target_hypothesis_id),
            None
        )

        if not target_meta:
            raise ValidationError(f"Invalid target hypothesis ID '{target_hypothesis_id}'.")

        # Find all rules that can prove this hypothesis
        candidate_rules = [
            r for r in RULES if r["hypothesis_id"] == target_hypothesis_id
        ]

        if not candidate_rules:
            return {
                "mode": "backward",
                "mode_label": "Backward Chaining (Goal-Driven Reasoning)",
                "target_hypothesis": target_meta["name"],
                "target_description": target_meta["description"],
                "status": "UNSUPPORTED_GOAL",
                "is_goal_satisfied": False,
                "message": f"No production rules found in knowledge base to establish hypothesis '{target_meta['name']}'."
            }

        rule_evaluations: List[Dict[str, Any]] = []
        overall_goal_satisfied = False

        for rule in candidate_rules:
            rule_antecedents = set(rule["antecedents"])
            min_required = rule.get("min_matches", len(rule_antecedents))

            satisfied_conditions = rule_antecedents.intersection(facts)
            missing_conditions = rule_antecedents.difference(facts)

            is_rule_satisfied = len(satisfied_conditions) >= min_required
            if is_rule_satisfied:
                overall_goal_satisfied = True

            rule_evaluations.append({
                "rule_id": rule["id"],
                "conclusion": rule["conclusion"],
                "required_conditions": [get_symptom_name(s) for s in rule_antecedents],
                "satisfied_conditions": [get_symptom_name(s) for s in satisfied_conditions],
                "missing_conditions": [get_symptom_name(s) for s in missing_conditions],
                "is_satisfied": is_rule_satisfied,
                "explanation": rule["explanation"],
                "recommendation": rule["recommendation"]
            })

        explanation_narrative = (
            f"Goal '{target_meta['name']}' is SATISFIED by the current facts. "
            f"All necessary antecedent conditions for rule {candidate_rules[0]['id']} were validated in the input facts."
            if overall_goal_satisfied
            else (
                f"Goal '{target_meta['name']}' is NOT SATISFIED. "
                f"The available facts do not fulfill all necessary conditions required by the rule(s). "
                "Important Note: Failure to satisfy the rule does NOT clinically rule out the condition."
            )
        )

        return {
            "mode": "backward",
            "mode_label": "Backward Chaining (Goal-Driven Reasoning)",
            "target_hypothesis_id": target_hypothesis_id,
            "target_hypothesis": target_meta["name"],
            "target_description": target_meta["description"],
            "facts_provided": [get_symptom_name(s) for s in facts],
            "is_goal_satisfied": overall_goal_satisfied,
            "rule_evaluations": rule_evaluations,
            "explanation_narrative": explanation_narrative,
            "conclusion_summary": "Hypothesis Supported" if overall_goal_satisfied else "Hypothesis Not Supported"
        }


def process_diagnosis_request(
    symptoms: List[str],
    inference_mode: str,
    target_goal: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main orchestrator for user diagnosis inquiries.
    1. Validates input
    2. Runs emergency check (P0)
    3. Executes chosen inference engine
    4. Formats standardized output structure
    """
    # Normalize input
    cleaned_symptoms: Set[str] = {
        s.strip().lower() for s in symptoms if s and isinstance(s, str)
    }

    # Validate symptom IDs against known catalog
    invalid_symptoms = cleaned_symptoms.difference(ALL_VALID_SYMPTOMS)
    if invalid_symptoms:
        raise ValidationError(f"Unrecognized symptom identifier(s): {', '.join(invalid_symptoms)}")

    if not cleaned_symptoms:
        raise ValidationError("Empty input: Please select at least one symptom to begin analysis.")

    # Validate inference mode
    mode = inference_mode.strip().lower()
    if mode not in {"forward", "backward"}:
        raise ValidationError(f"Invalid inference method '{inference_mode}'. Must be 'forward' or 'backward'.")

    # Step 1: Emergency Check (Red-Flag Priority Filter)
    emergency_result = EmergencyFilter.evaluate(cleaned_symptoms)
    if emergency_result:
        return {
            "success": True,
            "is_emergency": True,
            "emergency_data": emergency_result,
            "mode": mode,
            "facts_count": len(cleaned_symptoms),
            "disclaimer": "EDUCATIONAL PROTOTYPE ONLY - NOT A MEDICAL DIAGNOSTIC SERVICE."
        }

    # Step 2: Inference Engine execution
    if mode == "forward":
        inference_result = ForwardChainingEngine.run(cleaned_symptoms)
    else:
        if not target_goal:
            raise ValidationError("Target hypothesis must be selected for Backward Chaining mode.")
        inference_result = BackwardChainingEngine.run(target_goal, cleaned_symptoms)

    return {
        "success": True,
        "is_emergency": False,
        "inference_data": inference_result,
        "mode": mode,
        "facts_count": len(cleaned_symptoms),
        "disclaimer": (
            "Educational Demonstration Only: MedRule AI is an academic prototype developed "
            "for demonstration of Rule-Based AI Expert Systems under Savitribai Phule Pune University (SPPU). "
            "It does not provide medical diagnoses, treatment recommendations, or clinical advice."
        )
    }
