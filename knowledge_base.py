"""
Knowledge Base Module for MedRule AI
Rule-Based Medical Diagnosis Educational Expert System
SPPU TE Computer Engineering - Artificial Intelligence Mini-Project

Contains:
- Predefined symptom catalog with categories
- Emergency symptoms requiring immediate clinical intervention
- Production rules (IF-THEN) for illustrative symptom patterns
- Hypothesis definitions and supporting metadata
"""

# Available symptoms categorized for structured presentation and input validation
SYMPTOM_CATALOG = {
    "respiratory": [
        {"id": "sneezing", "name": "Sneezing", "description": "Frequent or sudden sneezing"},
        {"id": "runny_nose", "name": "Runny Nose", "description": "Excess nasal drainage"},
        {"id": "cough", "name": "Cough", "description": "Dry or productive cough"},
        {"id": "sore_throat", "name": "Sore Throat", "description": "Pain or scratchiness in throat"},
        {"id": "watery_nose", "name": "Watery Nasal Discharge", "description": "Clear watery nasal fluid"},
        {"id": "nasal_congestion", "name": "Nasal Congestion", "description": "Stuffy or blocked nasal passages"}
    ],
    "general": [
        {"id": "fever", "name": "Fever", "description": "Elevated body temperature above 37.8°C / 100°F"},
        {"id": "fatigue", "name": "Fatigue", "description": "Generalized tiredness or lethargy"},
        {"id": "body_ache", "name": "Body Ache / Myalgia", "description": "Muscle aches and generalized body pain"},
        {"id": "chills", "name": "Chills", "description": "Feeling cold with involuntary shivering"}
    ],
    "head_eyes": [
        {"id": "headache", "name": "Headache", "description": "Pain in head or upper neck"},
        {"id": "itchy_eyes", "name": "Itchy Eyes", "description": "Irritated, redness or itching in conjunctiva"},
        {"id": "facial_pressure", "name": "Facial Pain / Pressure", "description": "Tenderness around sinuses and forehead"},
        {"id": "light_sensitivity", "name": "Sensitivity to Light", "description": "Discomfort caused by bright light"}
    ],
    "digestive": [
        {"id": "nausea", "name": "Nausea", "description": "Uneasiness of stomach with urge to vomit"},
        {"id": "vomiting", "name": "Vomiting", "description": "Involuntary ejection of stomach contents"},
        {"id": "diarrhea", "name": "Diarrhea", "description": "Frequent loose or watery bowel movements"},
        {"id": "abdominal_pain", "name": "Abdominal Cramps", "description": "Discomfort or pain in the stomach region"}
    ],
    "emergency": [
        {"id": "difficulty_breathing", "name": "Difficulty Breathing / Dyspnea", "description": "Shortness of breath or struggle to breathe"},
        {"id": "severe_chest_pain", "name": "Severe Chest Pain / Pressure", "description": "Crushing or tight chest discomfort"},
        {"id": "unconsciousness", "name": "Loss of Consciousness / Fainting", "description": "Unresponsive or sudden syncope"}
    ]
}

# Flat list of all valid symptom IDs
ALL_VALID_SYMPTOMS = {
    symptom["id"]
    for category in SYMPTOM_CATALOG.values()
    for symptom in category
}

# Emergency symptoms triggering immediate red-flag response
EMERGENCY_SYMPTOMS = {
    "difficulty_breathing": "Acute breathing difficulty or shortness of breath detected.",
    "severe_chest_pain": "Severe chest pain or intense thoracic pressure detected.",
    "unconsciousness": "Loss of consciousness, extreme unresponsiveness or fainting detected."
}

# Target hypotheses available for backward chaining
HYPOTHESES = [
    {
        "id": "common_cold_pattern",
        "name": "Common Cold-like Symptom Pattern",
        "description": "Upper respiratory viral symptom profile typically presenting with sneezing, runny nose, and sore throat."
    },
    {
        "id": "allergy_pattern",
        "name": "Allergic Rhinitis-like Symptom Pattern",
        "description": "Environmental or seasonal allergic reaction characterized by itchy eyes, repeated sneezing, and clear watery discharge."
    },
    {
        "id": "flu_pattern",
        "name": "Influenza-like Illness (ILI) Pattern",
        "description": "Systemic viral profile characterized by acute onset of fever, cough, body aches, and marked fatigue."
    },
    {
        "id": "sinusitis_pattern",
        "name": "Sinusitis-like Symptom Pattern",
        "description": "Inflammation of nasal sinuses marked by facial pressure, headache, and persistent nasal congestion."
    },
    {
        "id": "gastroenteritis_pattern",
        "name": "Acute Gastroenteritis-like Symptom Pattern",
        "description": "Digestive tract irritation typically marked by nausea, vomiting, abdominal cramps, or diarrhea."
    },
    {
        "id": "migraine_pattern",
        "name": "Migraine-like Symptom Pattern",
        "description": "Neurological headache pattern accompanied by nausea, sensitivity to light, and intense throbbing pain."
    }
]

# Educational Production Rules (Knowledge Base)
# Each rule represents an IF-THEN implication: IF all antecedents are TRUE THEN hypothesis is triggered
RULES = [
    {
        "id": "R1",
        "hypothesis_id": "common_cold_pattern",
        "conclusion": "Common Cold-like Symptom Pattern",
        "antecedents": ["sneezing", "runny_nose", "sore_throat"],
        "min_matches": 3,
        "explanation": "Rule R1 fires: Co-occurrence of sneezing, runny nose, and mild sore throat corresponds logically to an upper respiratory common-cold-like profile.",
        "category": "Upper Respiratory",
        "recommendation": "Maintain hydration, rest adequately, and monitor symptoms. Seek clinical evaluation if symptoms worsen or persist beyond 7-10 days."
    },
    {
        "id": "R2",
        "hypothesis_id": "allergy_pattern",
        "conclusion": "Allergic Rhinitis-like Symptom Pattern",
        "antecedents": ["itchy_eyes", "sneezing", "watery_nose"],
        "min_matches": 3,
        "explanation": "Rule R2 fires: Pruritus of conjunctiva (itchy eyes) combined with repetitive sneezing and watery nasal discharge is characteristic of an allergic reaction pattern.",
        "category": "Immunological / Allergic",
        "recommendation": "Avoid suspected allergens (dust, pollen, pet dander). Consult an allergist or physician if discomfort interferes with daily activities."
    },
    {
        "id": "R3",
        "hypothesis_id": "flu_pattern",
        "conclusion": "Influenza-like Illness (ILI) Pattern",
        "antecedents": ["fever", "cough", "body_ache", "fatigue"],
        "min_matches": 3,
        "explanation": "Rule R3 fires: Acute combination of systemic fever, myalgia (body ache), dry/productive cough, and generalized fatigue aligns with an influenza-like symptom constellation.",
        "category": "Systemic Viral",
        "recommendation": "Ensure bed rest, oral fluids, and isolate to prevent viral transmission. Consult a healthcare provider if fever remains high or persistent."
    },
    {
        "id": "R4",
        "hypothesis_id": "sinusitis_pattern",
        "conclusion": "Sinusitis-like Symptom Pattern",
        "antecedents": ["headache", "facial_pressure", "nasal_congestion"],
        "min_matches": 3,
        "explanation": "Rule R4 fires: Frontal/maxillary facial pain or pressure coupled with headache and nasal congestion indicates potential sinus inflammation.",
        "category": "ENT / Sinus",
        "recommendation": "Warm steam inhalation and saline nasal rinses may provide comfort. Seek medical assessment if pain intensifies or persists."
    },
    {
        "id": "R5",
        "hypothesis_id": "gastroenteritis_pattern",
        "conclusion": "Acute Gastroenteritis-like Symptom Pattern",
        "antecedents": ["nausea", "vomiting", "diarrhea", "abdominal_pain"],
        "min_matches": 3,
        "explanation": "Rule R5 fires: Cluster of acute gastrointestinal disturbances including nausea, vomiting, abdominal cramps, and diarrhea matches an enteric irritation pattern.",
        "category": "Gastrointestinal",
        "recommendation": "Prevent dehydration using oral rehydration solutions (ORS). Consult a doctor promptly if unable to retain fluids or if symptoms exceed 24 hours."
    },
    {
        "id": "R6",
        "hypothesis_id": "migraine_pattern",
        "conclusion": "Migraine-like Symptom Pattern",
        "antecedents": ["headache", "nausea", "light_sensitivity"],
        "min_matches": 3,
        "explanation": "Rule R6 fires: Unilateral or severe headache accompanied by photophobia (light sensitivity) and nausea fits a migraine-like neurological pattern.",
        "category": "Neurological",
        "recommendation": "Rest in a quiet, dark room. A medical practitioner should be consulted for proper diagnosis and tailored migraine management."
    }
]

def get_symptom_name(symptom_id: str) -> str:
    """Helper to resolve human-readable symptom name from ID."""
    for category in SYMPTOM_CATALOG.values():
        for s in category:
            if s["id"] == symptom_id:
                return s["name"]
    return symptom_id.replace("_", " ").title()
