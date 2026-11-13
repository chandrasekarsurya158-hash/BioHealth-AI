"""
Symptoms Triage & Clinical Assessment Analyzer (Module 4A)
-----------------------------------------------------------
Executes:
1. Emergency Triage (evaluated BEFORE symptom matching)
2. Temperature verification (°C / °F) and implausibility detection
3. Clinical Syndromic Matching with differentials and rationale
4. Medication Safety, Allergy Cross-Checking, and Contraindication Screening
5. Recommended Next Steps (Self-care, Hydration, and When to Seek Care)
"""

from app.models.symptoms_data import (
    SUPPORTED_SYMPTOMS,
    SUPPORTED_CONDITIONS,
    SUPPORTED_ALLERGIES,
    EMERGENCY_RULES,
    SYNDROMES_KNOWLEDGE_BASE,
    MEDICINES_DATABASE
)

# In-memory store for complete rich clinical assessments
# Prevents client-side cookie overflow (>4KB) while preserving detailed medical metadata
GLOBAL_ASSESSMENT_CACHE = {}

class SymptomsAnalyzer:
    """Clinical triage engine ensuring safety-first medical assessment."""

    @staticmethod
    def parse_and_validate_temperature(temp_val, temp_unit):
        """
        Validates body temperature in Celsius or Fahrenheit.
        Detects physiologically implausible readings and normalizes both units.
        Returns: (is_valid, temp_f, temp_c, implausible_message)
        """
        if not temp_val:
            return True, None, None, None

        try:
            val = float(temp_val)
        except (ValueError, TypeError):
            return False, None, None, "Temperature must be a valid numeric value."

        unit = str(temp_unit).upper().strip()
        if "C" in unit:
            # Celsius validation
            if val < 30.0 or val > 45.0:
                return False, None, None, f"Entered temperature ({val:.1f}°C) is physiologically implausible for human life. Please recheck your thermometer and measurement technique."
            temp_c = val
            temp_f = (val * 9.0 / 5.0) + 32.0
        else:
            # Default to Fahrenheit
            if val < 85.0 or val > 115.0:
                return False, None, None, f"Entered temperature ({val:.1f}°F) is outside the physiological range for human survival. Please recheck your thermometer reading."
            temp_f = val
            temp_c = (val - 32.0) * 5.0 / 9.0

        return True, round(temp_f, 1), round(temp_c, 1), None

    @classmethod
    def evaluate(cls, selected_symptoms, duration, severity, age=None, 
                 temperature_val=None, temperature_unit="F",
                 allergies=None, conditions=None, current_medicines="", 
                 pregnancy_status="none", additional_notes=""):
        """
        Executes clinical rule-based evaluation with strict emergency priority.
        """
        if not selected_symptoms:
            return {
                "status": "error",
                "message": "Please select at least one symptom to evaluate."
            }

        symptom_set = set(selected_symptoms)
        allergies = allergies or []
        conditions = conditions or []

        # ---------------------------------------------------------
        # Step 1: Temperature Validation & Extreme Temperature Check
        # ---------------------------------------------------------
        temp_valid, temp_f, temp_c, temp_error = cls.parse_and_validate_temperature(
            temperature_val, temperature_unit
        )
        
        red_flags_triggered = []
        is_emergency = False

        if temp_error:
            # Non-blocking warning added to report
            temp_display = f"{temperature_val}° {temperature_unit} (Invalid reading: {temp_error})"
        elif temp_f is not None:
            temp_display = f"{temp_f}°F ({temp_c}°C)"
            # Check 108°F / 42.2°C emergency threshold
            if temp_f >= 108.0:
                is_emergency = True
                rule_108 = next(r for r in EMERGENCY_RULES if r["id"] == "extreme_hyperpyrexia")
                red_flags_triggered.append({
                    "title": rule_108["title"],
                    "reason": f"Recorded temperature of {temp_f}°F ({temp_c}°C) is in the extreme hyperpyrexia range. " + rule_108["reason"],
                    "action": rule_108["action"]
                })
            elif temp_f >= 104.0:
                rule_104 = next(r for r in EMERGENCY_RULES if r["id"] == "severe_fever")
                red_flags_triggered.append({
                    "title": rule_104["title"],
                    "reason": f"Recorded temperature of {temp_f}°F ({temp_c}°C) is dangerously elevated. " + rule_104["reason"],
                    "action": rule_104["action"]
                })
        else:
            temp_display = "Not Recorded"

        # ---------------------------------------------------------
        # Step 2: Emergency Triage System (Evaluated BEFORE Disease Matching)
        # ---------------------------------------------------------
        for rule in EMERGENCY_RULES:
            if "trigger" in rule:
                if all(trigger in symptom_set for trigger in rule["trigger"]):
                    is_emergency = True
                    # Avoid duplicate titles
                    if not any(rf["title"] == rule["title"] for rf in red_flags_triggered):
                        red_flags_triggered.append({
                            "title": rule["title"],
                            "reason": rule["reason"],
                            "action": rule["action"]
                        })

        # Determine overall urgency level
        if is_emergency:
            urgency_level = "EMERGENCY"
            urgency_badge = "bg-danger text-white"
            urgency_title = "CRITICAL EMERGENCY: IMMEDIATE MEDICAL ATTENTION REQUIRED"
        elif severity == "severe" or duration in ["more_than_week", "chronic"]:
            urgency_level = "HIGH"
            urgency_badge = "bg-warning text-dark"
            urgency_title = "HIGH URGENCY: SAME-DAY MEDICAL EVALUATION RECOMMENDED"
        elif severity == "moderate" or duration == "4_to_7_days":
            urgency_level = "MODERATE"
            urgency_badge = "bg-primary text-white"
            urgency_title = "MODERATE: CLINICAL CONSULTATION RECOMMENDED"
        else:
            urgency_level = "LOW"
            urgency_badge = "bg-success text-white"
            urgency_title = "ROUTINE SELF-CARE & CLOSE MONITORING"

        # ---------------------------------------------------------
        # Step 3: Possible Health Explanations
        # ---------------------------------------------------------
        if is_emergency:
            # FOR EMERGENCY: STOP ordinary benign disease matching from being the main result
            primary_syndrome = "Critical Medical Warning — Urgent Clinical Triage"
            matching_rationale = "Life-threatening or high-risk red-flag indicators have been detected in your reported evaluation."
            primary_explanation = (
                "EMERGENCY TRIAGE ACTIVE: One or more acute clinical red flags (such as critical fever, acute chest discomfort, respiratory distress, seizure activity, or neurological signs) take precedence over non-urgent diagnostic matching. Ordinary disease categorization is suppressed to prevent dangerous delays in emergency intervention."
            )
            differentials = [
                "Acute Cardiovascular / Thromboembolic Event",
                "Severe Respiratory Failure / Hypoxemia",
                "Central Nervous System Infection (e.g. Meningitis)",
                "Severe Hyperpyrexia / Heat-Induced Cellular Crisis",
                "Systemic Sepsis / Severe Metabolic Disturbance"
            ]
            home_guidance = (
                "DO NOT RELY ON HOME TREATMENT OR ORAL MEDICATIONS AS A SUBSTITUTE FOR EMERGENCY CARE. "
                "Keep the patient calm, sitting upright or in the recovery position if unconscious. "
                "Contact local paramedics (112 / 911) without delay."
            )
            when_to_seek_care = "IMMEDIATELY. Proceed to the nearest hospital emergency department."

        else:
            # NON-EMERGENCY: Match against reviewed medical knowledge base
            scored_syndromes = []
            for item in SYNDROMES_KNOWLEDGE_BASE:
                key_set = set(item["key_symptoms"])
                overlap = len(symptom_set.intersection(key_set))
                scored_syndromes.append((overlap, item))

            scored_syndromes.sort(key=lambda x: x[0], reverse=True)
            best_overlap, best_match = scored_syndromes[0]

            if best_overlap > 0:
                primary_syndrome = best_match["syndrome"]
                matching_rationale = best_match["matching_rationale"]
                primary_explanation = best_match["explanation"]
                differentials = best_match["differentials"]
                home_guidance = best_match["general_guidance"]
                when_to_seek_care = best_match["when_to_seek_care"]
            else:
                primary_syndrome = "Non-Specific Constitutional Symptom Complex"
                matching_rationale = "Your reported symptoms reflect generalized physiological responses rather than a single distinct clinical syndrome."
                primary_explanation = (
                    "Reported signs may be associated with an early incubation-stage viral infection, physical exhaustion, seasonal stress, or mild systemic inflammation. Because many illnesses share overlapping early symptoms, diagnosis requires direct examination by a licensed physician."
                )
                differentials = [
                    "Early Acute Viral Prodrome",
                    "Physical Fatigue / Sleep Deprivation",
                    "Mild Dehydration / Electrolyte Imbalance"
                ]
                home_guidance = (
                    "Prioritize quality sleep, optimize hydration with water and clear fluids, and eat light, easily digestible meals. Maintain a daily log of temperature and symptoms."
                )
                when_to_seek_care = (
                    "Schedule an appointment with your doctor if symptoms persist past 3 to 5 days, if fever develops, or if you feel progressively worse."
                )

        # ---------------------------------------------------------
        # Step 4: Medicine Information, Precautions & Safety Cross-Checks
        # ---------------------------------------------------------
        # Dynamically determine educational medicine profiles based on all evaluated symptoms
        applicable_med_set = set()

        if symptom_set.intersection({"fever", "headache", "joint_pain", "sore_throat"}):
            applicable_med_set.add("paracetamol")
            applicable_med_set.add("ibuprofen")
        if symptom_set.intersection({"cough", "sore_throat"}):
            applicable_med_set.add("honey_lozenges")
        if symptom_set.intersection({"cold", "cough"}):
            applicable_med_set.add("saline_spray")
        if symptom_set.intersection({"vomiting", "stomach_pain", "fatigue", "dizziness", "fever"}):
            applicable_med_set.add("ors_solution")

        # Fallback to standard core medicines if not already included
        if not applicable_med_set:
            applicable_med_set = {"paracetamol", "ors_solution"}

        # Preserve reliable order
        med_order = ["paracetamol", "ibuprofen", "saline_spray", "honey_lozenges", "ors_solution"]
        applicable_med_keys = [k for k in med_order if k in applicable_med_set]

        medicine_cards = []
        is_pregnant = (str(pregnancy_status).lower() == "pregnant")

        for m_key in applicable_med_keys:
            if m_key not in MEDICINES_DATABASE:
                continue

            med_data = MEDICINES_DATABASE[m_key].copy()
            safety_alerts = []
            is_contraindicated = False

            # 1. Allergy check
            if med_data.get("allergy_check_key"):
                if med_data["allergy_check_key"] in allergies:
                    is_contraindicated = True
                    safety_alerts.append(
                        f"CRITICAL ALLERGY WARNING: You reported an allergy to {SUPPORTED_ALLERGIES.get(med_data['allergy_check_key'], 'this medication')}. This medicine is strictly contraindicated."
                    )

            # 2. Existing health condition check
            for cond_key in med_data.get("condition_check_keys", []):
                if cond_key in conditions:
                    if cond_key == "peptic_ulcer" and m_key == "ibuprofen":
                        is_contraindicated = True
                        safety_alerts.append("CONTRAINDICATION: Ibuprofen and other NSAIDs irritate the gastric mucosal lining and are strictly contraindicated in active peptic ulcer disease or gastrointestinal bleeding.")
                    elif cond_key == "liver_disease" and m_key == "paracetamol":
                        is_contraindicated = True
                        safety_alerts.append("HEPATIC CAUTION: Paracetamol is metabolized by the liver. Patients with active liver disease or cirrhosis face elevated risk of hepatotoxicity; consult a doctor before use.")
                    elif cond_key == "kidney_disease" and m_key == "ibuprofen":
                        is_contraindicated = True
                        safety_alerts.append("RENAL WARNING: NSAIDs reduce renal blood flow. Avoid Ibuprofen in chronic kidney disease or renal impairment.")
                    elif cond_key == "asthma_copd" and m_key == "ibuprofen":
                        safety_alerts.append("RESPIRATORY CAUTION: Up to 10% of adults with asthma experience bronchospasm with NSAIDs (Aspirin-Exacerbated Respiratory Disease). Exercise extreme caution.")
                    elif cond_key == "heart_disease" and m_key == "ibuprofen":
                        safety_alerts.append("CARDIOVASCULAR CAUTION: Regular NSAID use may promote sodium retention and exacerbate hypertension or heart failure.")

            # 3. Pregnancy check
            if is_pregnant and med_data.get("pregnancy_contraindicated"):
                is_contraindicated = True
                safety_alerts.append("PREGNANCY WARNING: NSAIDs like Ibuprofen should be avoided during pregnancy (particularly in the third trimester due to risk of premature closure of the fetal ductus arteriosus and low amniotic fluid).")

            # 4. Current medicines interaction alert
            if current_medicines.strip():
                safety_alerts.append(f"MEDICATION INTERACTION CHECK: You reported taking: '{current_medicines}'. Review possible drug-drug interactions with a pharmacist before taking any new OTC medicine.")

            med_data["safety_alerts"] = safety_alerts
            med_data["is_contraindicated"] = is_contraindicated
            medicine_cards.append(med_data)

        # Formatted readable summary lists
        readable_symptoms = [
            SUPPORTED_SYMPTOMS.get(s, {}).get("name", s.replace("_", " ").title())
            for s in selected_symptoms
        ]
        readable_allergies = [
            SUPPORTED_ALLERGIES.get(a, a.replace("_", " ").title())
            for a in allergies
        ] or ["None Reported"]
        
        readable_conditions = [
            SUPPORTED_CONDITIONS.get(c, c.replace("_", " ").title())
            for c in conditions
        ] or ["None Reported"]

        duration_labels = {
            "less_24h": "Less than 24 hours (Acute onset)",
            "1_to_3_days": "1 to 3 days (Short-term)",
            "4_to_7_days": "4 to 7 days (Sub-acute)",
            "more_than_week": "More than 1 week (Prolonged)",
            "chronic": "Over 1 month (Chronic)"
        }

        return {
            "status": "success",
            "urgency_level": urgency_level,
            "urgency_badge": urgency_badge,
            "urgency_title": urgency_title,
            "is_emergency": is_emergency,
            "red_flags": red_flags_triggered,
            "patient_profile": {
                "age": age if age else "Not Specified",
                "temperature": temp_display,
                "allergies": readable_allergies,
                "conditions": readable_conditions,
                "current_medicines": current_medicines if current_medicines.strip() else "None Reported",
                "pregnancy_status": pregnancy_status.replace("_", " ").title() if pregnancy_status != "none" else "Not Applicable"
            },
            "selected_symptoms": readable_symptoms,
            "raw_symptoms": selected_symptoms,
            "duration": duration_labels.get(duration, duration),
            "severity": severity.capitalize(),
            "notes": additional_notes,
            "primary_syndrome": primary_syndrome,
            "matching_rationale": matching_rationale,
            "primary_explanation": primary_explanation,
            "differentials": differentials,
            "home_guidance": home_guidance,
            "when_to_seek_care": when_to_seek_care,
            "medicine_cards": medicine_cards
        }
