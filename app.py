"""
MedRule AI - Web Application
Rule-Based Medical Diagnosis Educational Expert System
SPPU TE Computer Engineering - NEP 2024 Pattern

Student: Harsh Rajendra Sakpal (Roll No. 45, Div TE-A COMP)
College: Bharati Vidyapeeth's College of Engineering, Lavale, Pune
Guide: Prof. Ajit Patil
Academic Year: 2026-27
"""

import os
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from knowledge_base import (
    SYMPTOM_CATALOG,
    HYPOTHESES,
    RULES,
    EMERGENCY_SYMPTOMS,
    get_symptom_name
)
from inference_engine import (
    process_diagnosis_request,
    ValidationError
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static",
    template_folder=os.path.join(BASE_DIR, "templates")
)
# Secret key for secure session state management
app.secret_key = os.environ.get("SECRET_KEY", "medrule-ai-sppu-2026-harsh-sakpal-secret-key")

from flask import send_from_directory

@app.route("/static/<path:filename>")
def custom_static(filename):
    """Ensure static files are always served reliably across local and serverless environments."""
    return send_from_directory(app.static_folder, filename)

# Academic Project Context
PROJECT_METADATA = {
    "title": "AI-Based Medical Diagnosis System Using a Rule-Based Expert System",
    "short_name": "MedRule AI",
    "student": "Harsh Rajendra Sakpal",
    "roll_no": "45",
    "division": "TE-A COMP",
    "academic_year": "2026-27",
    "semester": "Semester V",
    "college": "Bharati Vidyapeeth's College of Engineering, Lavale, Pune",
    "department": "Department of Computer Engineering",
    "university": "Savitribai Phule Pune University (SPPU)",
    "pattern": "NEP 2024",
    "guide": "Prof. Ajit Patil",
    "subject": "Artificial Intelligence (Mini-Project)"
}


@app.context_processor
def inject_metadata():
    """Make project metadata globally available across all Jinja2 templates."""
    return {"meta": PROJECT_METADATA}


@app.route("/")
def index():
    """Home page: Interactive Symptom Selection, Inference Mode Toggle, and Safety Notice."""
    return render_template(
        "index.html",
        catalog=SYMPTOM_CATALOG,
        hypotheses=HYPOTHESES,
        rules=RULES,
        emergency_keys=list(EMERGENCY_SYMPTOMS.keys())
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    """Process symptoms via selected inference method and render explanation result."""
    selected_symptoms = request.form.getlist("symptoms")
    inference_mode = request.form.get("inference_mode", "forward")
    target_goal = request.form.get("target_goal", "").strip() or None

    try:
        result = process_diagnosis_request(
            symptoms=selected_symptoms,
            inference_mode=inference_mode,
            target_goal=target_goal
        )

        # Store in session history (capped at latest 15 records)
        if "history" not in session:
            session["history"] = []

        history_entry = {
            "id": len(session["history"]) + 1,
            "timestamp": datetime.datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p"),
            "mode": inference_mode,
            "facts_count": len(selected_symptoms),
            "symptoms": [get_symptom_name(s) for s in selected_symptoms],
            "is_emergency": result.get("is_emergency", False),
            "summary": (
                "CRITICAL EMERGENCY ALERT"
                if result.get("is_emergency")
                else (
                    result["inference_data"]["conclusion_summary"]
                )
            )
        }
        
        # Prepend latest entry
        session["history"].insert(0, history_entry)
        session["history"] = session["history"][:15]
        session.modified = True

        return render_template(
            "result.html",
            result=result,
            symptoms=[get_symptom_name(s) for s in selected_symptoms],
            inference_mode=inference_mode,
            target_goal=target_goal,
            catalog=SYMPTOM_CATALOG
        )

    except ValidationError as ve:
        return render_template(
            "index.html",
            catalog=SYMPTOM_CATALOG,
            hypotheses=HYPOTHESES,
            rules=RULES,
            emergency_keys=list(EMERGENCY_SYMPTOMS.keys()),
            error_message=str(ve)
        ), 400
    except Exception as e:
        return render_template(
            "index.html",
            catalog=SYMPTOM_CATALOG,
            hypotheses=HYPOTHESES,
            rules=RULES,
            emergency_keys=list(EMERGENCY_SYMPTOMS.keys()),
            error_message=f"An unexpected error occurred during inference processing: {str(e)}"
        ), 500


@app.route("/history")
def history():
    """View analysis audit history dashboard (reflecting report Page 16)."""
    user_history = session.get("history", [])
    return render_template("history.html", history=user_history)


@app.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear session-stored analysis logs."""
    session["history"] = []
    session.modified = True
    return redirect(url_for("history"))


@app.route("/about")
def about():
    """Display project background, AI architecture, mathematical model, and SPPU credentials."""
    return render_template(
        "about.html",
        catalog=SYMPTOM_CATALOG,
        rules=RULES,
        hypotheses=HYPOTHESES
    )


@app.route("/tests")
def test_runner():
    """Interactive in-browser automated test runner demonstrating test cases TC-01 to TC-10."""
    import unittest
    from io import StringIO
    from tests import test_inference

    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    suite = unittest.TestLoader().loadTestsFromModule(test_inference)
    test_result = runner.run(suite)

    test_logs = stream.getvalue()
    total_tests = test_result.testsRun
    failures = len(test_result.failures)
    errors = len(test_result.errors)
    passed = total_tests - (failures + errors)

    return render_template(
        "test_runner.html",
        total=total_tests,
        passed=passed,
        failures=failures,
        errors=errors,
        was_successful=test_result.wasSuccessful(),
        logs=test_logs
    )


# REST API Endpoints for external or headless verification
@app.route("/api/symptoms", methods=["GET"])
def api_symptoms():
    """API endpoint providing all symptoms categorized."""
    return jsonify({"success": True, "catalog": SYMPTOM_CATALOG})


@app.route("/api/rules", methods=["GET"])
def api_rules():
    """API endpoint providing the educational rule base."""
    return jsonify({"success": True, "rules": RULES, "hypotheses": HYPOTHESES})


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """JSON API endpoint for headless diagnosis request processing."""
    data = request.get_json(silent=True) or {}
    symptoms = data.get("symptoms", [])
    mode = data.get("mode", "forward")
    target_goal = data.get("target_goal")

    try:
        result = process_diagnosis_request(
            symptoms=symptoms,
            inference_mode=mode,
            target_goal=target_goal
        )
        return jsonify(result), 200
    except ValidationError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Internal inference error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting MedRule AI server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
