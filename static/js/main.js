/**
 * MedRule AI - Client Interaction & UI Script
 * Savitribai Phule Pune University (SPPU) TE Artificial Intelligence Mini-Project
 */

document.addEventListener("DOMContentLoaded", function () {
    initializeCheckboxes();
    updateCounter();
});

// Toggle between Forward and Backward Chaining modes
function toggleInferenceMode(mode) {
    const forwardCard = document.getElementById("forwardCard");
    const backwardCard = document.getElementById("backwardCard");
    const targetGoalWrapper = document.getElementById("targetGoalWrapper");

    if (mode === "forward") {
        forwardCard.classList.add("active");
        backwardCard.classList.remove("active");
        if (targetGoalWrapper) {
            targetGoalWrapper.style.display = "none";
        }
    } else {
        backwardCard.classList.add("active");
        forwardCard.classList.remove("active");
        if (targetGoalWrapper) {
            targetGoalWrapper.style.display = "block";
            targetGoalWrapper.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
    }
}

// Initialize checkbox state and card selection highlights
function initializeCheckboxes() {
    const checkboxes = document.querySelectorAll(".symptom-checkbox");
    checkboxes.forEach(chk => {
        // Initial state
        if (chk.checked) {
            chk.closest(".symptom-card").classList.add("selected");
        }

        chk.addEventListener("change", function () {
            const card = this.closest(".symptom-card");
            if (this.checked) {
                card.classList.add("selected");
            } else {
                card.classList.remove("selected");
            }
            updateCounter();
        });
    });

    // Form submission validation
    const form = document.getElementById("diagnosisForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            const selected = document.querySelectorAll(".symptom-checkbox:checked");
            if (selected.length === 0) {
                e.preventDefault();
                alert("Please select at least one symptom before running the inference engine.");
            }
        });
    }
}

// Update selected symptoms count indicator
function updateCounter() {
    const selected = document.querySelectorAll(".symptom-checkbox:checked");
    const countEl = document.getElementById("selectedCountText");
    if (countEl) {
        countEl.textContent = selected.length;
    }
}

// Quick presets for evaluation and viva demonstration
const PRESETS = {
    cold: ["sneezing", "runny_nose", "sore_throat"],
    flu: ["fever", "cough", "body_ache", "fatigue"],
    allergy: ["itchy_eyes", "sneezing", "watery_nose"],
    sinus: ["headache", "facial_pressure", "nasal_congestion"],
    emergency: ["fever", "cough", "severe_chest_pain", "difficulty_breathing"]
};

function loadPreset(presetName) {
    clearAllSymptoms();
    const symptomsToSelect = PRESETS[presetName] || [];

    symptomsToSelect.forEach(id => {
        const chk = document.getElementById("chk_" + id);
        if (chk) {
            chk.checked = true;
            chk.closest(".symptom-card").classList.add("selected");
        }
    });

    updateCounter();

    // Visual feedback
    const counter = document.getElementById("selectionCounter");
    if (counter) {
        counter.style.transform = "scale(1.08)";
        setTimeout(() => {
            counter.style.transform = "scale(1)";
        }, 200);
    }
}

function clearAllSymptoms() {
    const checkboxes = document.querySelectorAll(".symptom-checkbox");
    checkboxes.forEach(chk => {
        chk.checked = false;
        chk.closest(".symptom-card").classList.remove("selected");
    });
    updateCounter();
}
