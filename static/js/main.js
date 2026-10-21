/**
 * MedRule AI — Client Interaction & Motion System
 * Smooth transitions, staggered animations, and micro-interactions
 * SPPU TE Artificial Intelligence Mini-Project
 */

document.addEventListener("DOMContentLoaded", function () {
    initializeCheckboxes();
    updateCounter();
    initStaggerAnimations();
    initScrollReveal();
    initRippleEffects();
});

/* ═══════════════════════════════════════════
   INFERENCE MODE TOGGLE
   ═══════════════════════════════════════════ */
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

/* ═══════════════════════════════════════════
   CHECKBOX INTERACTIONS
   ═══════════════════════════════════════════ */
function initializeCheckboxes() {
    const checkboxes = document.querySelectorAll(".symptom-checkbox");
    checkboxes.forEach(chk => {
        if (chk.checked) {
            chk.closest(".symptom-card").classList.add("selected");
        }

        chk.addEventListener("change", function () {
            const card = this.closest(".symptom-card");
            if (this.checked) {
                card.classList.add("selected");
                // Mini pop animation
                card.style.transform = "scale(1.03)";
                setTimeout(() => {
                    card.style.transform = "";
                }, 200);
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
                showToast("Please select at least one symptom before running the inference engine.");
            }
        });
    }
}

/* ═══════════════════════════════════════════
   COUNTER UPDATE WITH ANIMATION
   ═══════════════════════════════════════════ */
function updateCounter() {
    const selected = document.querySelectorAll(".symptom-checkbox:checked");
    const countEl = document.getElementById("selectedCountText");
    if (countEl) {
        const newCount = selected.length;
        const oldCount = parseInt(countEl.textContent) || 0;

        if (newCount !== oldCount) {
            countEl.style.transform = "scale(1.3)";
            countEl.style.color = "#6366f1";
            setTimeout(() => {
                countEl.textContent = newCount;
                countEl.style.transform = "scale(1)";
            }, 120);
            setTimeout(() => {
                countEl.style.color = "";
            }, 400);
        }
    }
}

/* ═══════════════════════════════════════════
   QUICK PRESETS
   ═══════════════════════════════════════════ */
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

    symptomsToSelect.forEach((id, index) => {
        const chk = document.getElementById("chk_" + id);
        if (chk) {
            // Stagger the check animation
            setTimeout(() => {
                chk.checked = true;
                const card = chk.closest(".symptom-card");
                card.classList.add("selected");
                card.style.transform = "scale(1.04)";
                setTimeout(() => {
                    card.style.transform = "";
                }, 180);
            }, index * 80);
        }
    });

    // Update counter after all are checked
    setTimeout(() => {
        updateCounter();
    }, symptomsToSelect.length * 80 + 100);

    // Bounce the counter
    const counter = document.getElementById("selectionCounter");
    if (counter) {
        setTimeout(() => {
            counter.style.transform = "scale(1.06)";
            setTimeout(() => {
                counter.style.transform = "scale(1)";
            }, 250);
        }, symptomsToSelect.length * 80 + 50);
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

/* ═══════════════════════════════════════════
   STAGGER ANIMATIONS — ON LOAD
   ═══════════════════════════════════════════ */
function initStaggerAnimations() {
    // Stagger symptom category blocks
    const categories = document.querySelectorAll(".category-block");
    categories.forEach((el, i) => {
        el.style.opacity = "0";
        el.style.transform = "translateY(14px)";
        el.style.transition = `opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1), transform 0.45s cubic-bezier(0.16, 1, 0.3, 1)`;
        el.style.transitionDelay = `${0.1 + i * 0.08}s`;
        requestAnimationFrame(() => {
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
        });
    });

    // Stagger history cards
    const historyCards = document.querySelectorAll(".history-card");
    historyCards.forEach((el, i) => {
        el.style.opacity = "0";
        el.style.transform = "translateX(-12px)";
        el.style.transition = `opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)`;
        el.style.transitionDelay = `${i * 0.06}s`;
        requestAnimationFrame(() => {
            el.style.opacity = "1";
            el.style.transform = "translateX(0)";
        });
    });

    // Stagger metric cards
    const metrics = document.querySelectorAll(".metric-card");
    metrics.forEach((el, i) => {
        el.style.opacity = "0";
        el.style.transform = "translateY(16px) scale(0.95)";
        el.style.transition = `opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)`;
        el.style.transitionDelay = `${0.15 + i * 0.1}s`;
        requestAnimationFrame(() => {
            el.style.opacity = "1";
            el.style.transform = "translateY(0) scale(1)";
        });
    });
}

/* ═══════════════════════════════════════════
   SCROLL REVEAL — INTERSECTION OBSERVER
   ═══════════════════════════════════════════ */
function initScrollReveal() {
    const revealElements = document.querySelectorAll(
        ".card, .arch-tier-card, .content-card, .rule-match-card, .evaluation-item"
    );

    if (!("IntersectionObserver" in window)) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -40px 0px"
    });

    revealElements.forEach(el => {
        // Only observe elements below the fold
        const rect = el.getBoundingClientRect();
        if (rect.top > window.innerHeight * 0.8) {
            el.style.opacity = "0";
            el.style.transform = "translateY(16px)";
            el.style.transition = "opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)";
            observer.observe(el);
        }
    });
}

/* ═══════════════════════════════════════════
   RIPPLE EFFECT ON BUTTONS
   ═══════════════════════════════════════════ */
function initRippleEffects() {
    document.querySelectorAll(".btn").forEach(btn => {
        btn.addEventListener("mousedown", function (e) {
            const rect = this.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            this.style.setProperty("--ripple-x", x + "%");
            this.style.setProperty("--ripple-y", y + "%");
        });
    });
}

/* ═══════════════════════════════════════════
   TOAST NOTIFICATION
   ═══════════════════════════════════════════ */
function showToast(message) {
    // Remove existing toast
    const existing = document.querySelector(".toast-notification");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.className = "toast-notification";
    toast.innerHTML = `<i class="fa-solid fa-circle-info"></i> ${message}`;
    toast.style.cssText = `
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%) translateY(20px);
        background: #0f172a;
        color: #e2e8f0;
        padding: 0.85rem 1.4rem;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 600;
        font-family: inherit;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        box-shadow: 0 12px 32px rgba(0,0,0,0.2);
        opacity: 0;
        transition: opacity 0.3s, transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    `;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateX(-50%) translateY(0)";
    });

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(-50%) translateY(10px)";
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}
