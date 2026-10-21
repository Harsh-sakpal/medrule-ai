# MedRule AI: AI-Based Medical Diagnosis System Using a Rule-Based Expert System

**Savitribai Phule Pune University (SPPU) — NEP 2024 Pattern**  
**Third Year Computer Engineering (Semester V) &bull; Artificial Intelligence Mini-Project**

---

## Academic Information

- **Institution:** Bharati Vidyapeeth's College of Engineering, Lavale, Pune
- **Department:** Department of Computer Engineering
- **University:** Savitribai Phule Pune University (SPPU)
- **Academic Year:** 2026–2027
- **Candidate Name:** Harsh Rajendra Sakpal
- **Roll Number:** 45
- **Division:** TE-A COMP
- **Project Guide:** Prof. Ajit Patil
- **Subject:** Artificial Intelligence (Mini-Project)

---

## Project Overview

**MedRule AI** is an educational Rule-Based Expert System developed to demonstrate fundamental Artificial Intelligence concepts:
1. **Knowledge Representation:** Structured IF–THEN production rules representing medical symptom patterns.
2. **Forward Chaining (Data-Driven Reasoning):** Deducing conclusions from user-observed symptoms (facts) to matched disease profiles.
3. **Backward Chaining (Goal-Driven Reasoning):** Testing a specific suspected diagnostic goal by verifying whether supporting antecedent facts exist.
4. **Emergency Priority Filter (Red-Flags):** Life-safety priority filter that immediately halts normal rule processing and triggers urgent medical assistance alerts when high-risk symptoms (such as severe chest pain, breathing difficulty, or loss of consciousness) are detected.
5. **Explainable AI (XAI):** Step-by-step reasoning trace indicating which rules were inspected, which antecedent conditions were satisfied vs. missing, and why conclusions were reached.
6. **Audit History Dashboard:** Session-based record of evaluations matching SPPU academic prototype specifications.

> **Academic Disclaimer:** MedRule AI is strictly an educational prototype designed for academic demonstrations under SPPU syllabus guidelines. It is **not** a certified medical device and must **never** be used for clinical diagnosis or replacing licensed healthcare practitioners.

---

## System Architecture

The application implements a clean **Three-Layer Architecture**:

1. **Presentation Layer:**
   - HTML5, modern CSS3 (glassmorphic styling, responsive layout, CSS variables), and Vanilla JavaScript.
   - Interactive checkbox grid categorized into Respiratory, General/Systemic, Head & Eyes, Gastrointestinal, and Emergency Red-Flags.
   - Dynamic mode switch between Forward Chaining and Backward Chaining with live goal selector.
   - In-browser live Automated Test Suite Runner (`/tests`).

2. **Application / Inference Engine Layer:**
   - Python 3 & Flask web controller.
   - `EmergencyFilter`: Priority 0 evaluation for acute danger indicators.
   - `ForwardChainingEngine`: Evaluates working memory facts against rule antecedents.
   - `BackwardChainingEngine`: Depth-verification of required conditions for candidate goals.
   - Explainable trace generation and input validation.

3. **Knowledge Layer:**
   - Declarative production rules ($R_1 \dots R_6$), emergency catalogs, and hypothesis schemas stored in Python data structures.

---

## Project Directory Structure

```text
AI_miniproject/
│
├── app.py                     # Main Flask web application and routing controller
├── inference_engine.py        # Core Forward & Backward Chaining reasoning engines
├── knowledge_base.py          # IF-THEN production rules and symptom definitions
├── vercel.json                # Vercel deployment configuration for Python Serverless
├── requirements.txt           # Python dependencies (Flask, pytest, etc.)
├── README.md                  # Comprehensive setup and run documentation
├── PROJECT_REPORT.md          # 20-page SPPU academic mini-project report
│
├── api/
│   └── index.py               # Vercel Serverless Function entry point
│
├── templates/
│   ├── base.html              # Master layout with navigation and SPPU metadata
│   ├── index.html             # Symptom checker and reasoning mode selector
│   ├── result.html            # Diagnostic result, explainable trace, and emergency alert
│   ├── history.html           # Analysis audit history dashboard
│   ├── about.html             # System design, architecture, and mathematical model
│   └── test_runner.html       # Live in-browser automated unit test runner
│
├── static/
│   ├── css/
│   │   └── style.css          # Modern medical UI styling and design tokens
│   └── js/
│       └── main.js            # Frontend interactivity, mode toggling, and presets
│
└── tests/
    ├── __init__.py
    ├── test_inference.py      # 10 Academic Unit Tests (TC-01 to TC-10)
    └── test_routes.py         # HTTP web endpoint & REST API test suite
```

---

## Local Setup and Running on Windows

### Prerequisites
- Python 3.10+ (Available via `py` or `python` command)
- Git (optional, for version control)
- Visual Studio Code or any code editor

### Step-by-Step Instructions

1. **Open Terminal in the Project Directory:**
   ```powershell
   cd "C:\Users\Harsh Sakpal\Desktop\AI_miniproject"
   ```

2. **Create a Virtual Environment (Recommended):**
   ```powershell
   py -m venv venv
   ```

3. **Activate the Virtual Environment:**
   ```powershell
   .\venv\Scripts\activate
   ```

4. **Install Dependencies:**
   ```powershell
   py -m pip install -r requirements.txt
   ```

5. **Run the Application:**
   ```powershell
   py app.py
   ```

6. **Access in Web Browser:**
   Open your browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

7. **Run the Automated Unit Tests:**
   ```powershell
   py -m unittest discover tests
   ```
   All 18 test cases will execute and verify the inference engine.

---

## Deploying on Vercel

MedRule AI is pre-configured for instant zero-configuration deployment on **Vercel** via Serverless Functions.

### Method 1: Using the Vercel CLI

1. **Install Vercel CLI globally (if not already installed):**
   ```powershell
   npm install -g vercel
   ```

2. **Deploy directly from the project directory:**
   ```powershell
   vercel
   ```
   - Follow the interactive prompts (Accept defaults by pressing Enter).
   - Link to your Vercel account.

3. **Deploy to Production:**
   ```powershell
   vercel --prod
   ```

### Method 2: Deploying via GitHub to Vercel (1-Click Git Integration)

1. **Initialize Git and commit your files:**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit of MedRule AI Expert System"
   ```

2. **Push to GitHub:**
   - Create a new repository on GitHub (e.g., `medrule-ai`).
   ```powershell
   git remote add origin https://github.com/<your-username>/medrule-ai.git
   git branch -M main
   git push -u origin main
   ```

3. **Import into Vercel:**
   - Log in to [vercel.com](https://vercel.com).
   - Click **"Add New..."** &rarr; **"Project"**.
   - Select your `medrule-ai` repository.
   - Vercel automatically detects `vercel.json` and builds the `@vercel/python` serverless function.
   - Click **"Deploy"**.
   - Your live URL (e.g. `https://medrule-ai.vercel.app`) will be ready in under 60 seconds!

---

## Automated Test Cases Matrix

| Test ID | Test Description | Target Logic | Input Vector | Expected Output | Status |
|---|---|---|---|---|---|
| **TC-01** | Forward Chaining Cold Match | ForwardChainingEngine | `[sneezing, runny_nose, sore_throat]` | Fires Rule R1 (Common Cold pattern) | **PASS** |
| **TC-02** | Forward Chaining Allergy Match | ForwardChainingEngine | `[itchy_eyes, sneezing, watery_nose]` | Fires Rule R2 (Allergy pattern) | **PASS** |
| **TC-03** | Forward Chaining Flu Match | ForwardChainingEngine | `[fever, cough, body_ache, fatigue]` | Fires Rule R3 (Influenza pattern) | **PASS** |
| **TC-04** | Backward Chaining Goal Proof | BackwardChainingEngine | Goal: flu_pattern + 4 symptoms | Goal Satisfied = True | **PASS** |
| **TC-05** | Backward Chaining Missing Condition | BackwardChainingEngine | Goal: allergy_pattern + `[fever, cough]` | Goal Satisfied = False | **PASS** |
| **TC-06** | Empty Symptom Selection | Input Validation | `[]` (Empty set) | Raises ValidationError | **PASS** |
| **TC-07** | Unmatched Symptoms Uncertainty | ForwardChainingEngine | `[fatigue]` (Partial non-match) | Returns `is_uncertain = True` | **PASS** |
| **TC-08** | Emergency Priority Filter | EmergencyFilter | `[fever, severe_chest_pain]` | Halts normal rule firing, CRITICAL alert | **PASS** |
| **TC-09** | Invalid Inference Mode | Input Validation | Mode: `unknown_mode` | Raises ValidationError | **PASS** |
| **TC-10** | Forward Chaining Sinusitis Match | ForwardChainingEngine | `[headache, facial_pressure, nasal_congestion]` | Fires Rule R4 (Sinusitis pattern) | **PASS** |

---

## REST API Reference

MedRule AI provides headless REST API endpoints for automated programmatic evaluation:

- **`GET /api/symptoms`**: Returns categorized symptom inventory.
- **`GET /api/rules`**: Returns declarative rule base and hypotheses.
- **`POST /api/analyze`**: Submits symptoms for diagnosis.
  - **Request Body:**
    ```json
    {
      "symptoms": ["sneezing", "runny_nose", "sore_throat"],
      "mode": "forward"
    }
    ```
  - **Response (200 OK):**
    ```json
    {
      "success": true,
      "is_emergency": false,
      "mode": "forward",
      "facts_count": 3,
      "inference_data": {
        "matched_rules": [
          {
            "rule_id": "R1",
            "hypothesis": "Common Cold-like Symptom Pattern",
            "category": "Upper Respiratory"
          }
        ]
      }
    }
    ```

---

## Academic Assessment Reference

This project is prepared in fulfillment of the **Savitribai Phule Pune University (SPPU)** Third Year (TE) Computer Engineering Artificial Intelligence Laboratory Mini-Project requirements under **NEP 2024**.
