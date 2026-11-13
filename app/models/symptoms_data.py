"""
Clinical Symptoms Knowledge Base, Emergency Rules & Pharmacopeia (Module 4A)
----------------------------------------------------------------------------
Reviewed medical ontology covering:
- Common and emergency symptoms
- Emergency triage rules (including temperature boundaries, seizures, chest pain)
- Syndromic matching knowledge base with differential causes and matching rationale
- Educational medicine database with contraindications, precautions, and allergy cross-checks
- Sources: WHO Model List, NHS UK, CDC, American Heart Association, FDA
"""

# Supported symptoms categorized by anatomical/clinical domain
SUPPORTED_SYMPTOMS = {
    "fever": {"name": "Fever / Elevated Body Temperature", "icon": "bi-thermometer-half", "category": "General", "is_emergency": False},
    "headache": {"name": "Headache / Head Pressure", "icon": "bi-person-headset", "category": "Neurological", "is_emergency": False},
    "cough": {"name": "Persistent Cough", "icon": "bi-soundwave", "category": "Respiratory", "is_emergency": False},
    "cold": {"name": "Runny / Stuffy Nose (Congestion)", "icon": "bi-snow", "category": "Respiratory", "is_emergency": False},
    "sore_throat": {"name": "Sore Throat / Pharyngeal Pain", "icon": "bi-mic", "category": "Respiratory", "is_emergency": False},
    "shortness_breath": {"name": "Difficulty Breathing / Shortness of Breath", "icon": "bi-wind", "category": "Cardiorespiratory", "is_emergency": True},
    "chest_pain": {"name": "Chest Pain / Tightness / Pressure", "icon": "bi-heartbreak", "category": "Cardiorespiratory", "is_emergency": True},
    "vomiting": {"name": "Nausea / Vomiting", "icon": "bi-emoji-dizzy", "category": "Gastrointestinal", "is_emergency": False},
    "stomach_pain": {"name": "Abdominal / Stomach Pain", "icon": "bi-capsule-pill", "category": "Gastrointestinal", "is_emergency": False},
    "fatigue": {"name": "Profound Fatigue / Weakness", "icon": "bi-battery", "category": "General", "is_emergency": False},
    "joint_pain": {"name": "Joint / Muscle Aches (Myalgia)", "icon": "bi-person-arms-up", "category": "Musculoskeletal", "is_emergency": False},
    "dizziness": {"name": "Dizziness / Vertigo / Lightheadedness", "icon": "bi-arrow-repeat", "category": "Neurological", "is_emergency": False},
    "stiff_neck": {"name": "Stiff Neck (Inability to touch chin to chest)", "icon": "bi-shield-exclamation", "category": "Emergency", "is_emergency": True},
    "confusion": {"name": "Confusion / Disorientation / Altered Mental State", "icon": "bi-exclamation-triangle-fill", "category": "Emergency", "is_emergency": True},
    "seizures": {"name": "Seizures / Involuntary Convulsions / Tremors", "icon": "bi-lightning-charge-fill", "category": "Emergency", "is_emergency": True},
    "blood_vomit": {"name": "Blood in Vomit (Hematemesis) or Black Tarry Stool", "icon": "bi-droplet-fill", "category": "Emergency", "is_emergency": True},
    "loss_consciousness": {"name": "Fainting / Loss of Consciousness (Syncope)", "icon": "bi-person-x-fill", "category": "Emergency", "is_emergency": True}
}

# Standardized Common Preexisting Health Conditions
SUPPORTED_CONDITIONS = {
    "liver_disease": "Liver Disease / Hepatitis / Cirrhosis",
    "kidney_disease": "Kidney Disease / Renal Impairment",
    "peptic_ulcer": "Peptic Ulcer / Gastrointestinal Bleeding",
    "asthma_copd": "Asthma / COPD / Respiratory Disease",
    "heart_disease": "Hypertension / Coronary Heart Disease",
    "diabetes": "Diabetes Mellitus (Type 1 or 2)",
    "none": "No Known Preexisting Chronic Conditions"
}

# Standardized Drug Allergies
SUPPORTED_ALLERGIES = {
    "paracetamol": "Paracetamol (Acetaminophen)",
    "nsaids": "NSAIDs (Ibuprofen, Aspirin, Naproxen)",
    "penicillin": "Penicillin / Beta-Lactam Antibiotics",
    "sulfa": "Sulfonamides (Sulfa drugs)",
    "none": "No Known Drug Allergies"
}

# Emergency Triage Evaluation Rules
EMERGENCY_RULES = [
    {
        "id": "extreme_hyperpyrexia",
        "condition": "temperature_extreme",
        "threshold_f": 108.0,
        "threshold_c": 42.2,
        "title": "HYPERPYREXIA / HEAT STROKE EMERGENCY",
        "reason": "Body temperature at or above 108.0°F (42.2°C) is a life-threatening physiological emergency. Extreme hyperthermia can cause rapid cellular denaturation, cerebral edema, permanent neurological injury, and cardiac collapse.",
        "action": "Call local emergency services (112 / 911) IMMEDIATELY. While waiting for paramedics, move the person to a cool environment, remove excess clothing, and apply cool wet cloths to the neck, armpits, and groin. Do not rely on oral medication alone."
    },
    {
        "id": "severe_fever",
        "condition": "temperature_severe",
        "threshold_f": 104.0,
        "threshold_c": 40.0,
        "title": "HIGH FEVER WARNING (Severe Pyrexia)",
        "reason": "Body temperature at or above 104.0°F (40.0°C) indicates acute systemic inflammation or severe infection requiring urgent medical evaluation.",
        "action": "Contact a doctor or urgent care clinic promptly. If accompanied by lethargy, rash, stiff neck, or confusion, proceed to the emergency room immediately."
    },
    {
        "id": "cardiorespiratory_crisis",
        "trigger": ["chest_pain", "shortness_breath"],
        "title": "ACUTE CARDIOPULMONARY EMERGENCY",
        "reason": "The co-occurrence of chest pain/pressure and shortness of breath requires immediate clinical rule-out of Acute Myocardial Infarction (heart attack), Pulmonary Embolism, or Pneumothorax.",
        "action": "CALL EMERGENCY SERVICES (112 / 911) NOW. Have the person sit in a comfortable position and remain calm. Do not drive to the hospital yourself if paramedics can be dispatched."
    },
    {
        "id": "isolated_chest_pain",
        "trigger": ["chest_pain"],
        "title": "CHEST PAIN EMERGENCY WARNING",
        "reason": "Unexplained chest tightness, pressure, or radiating discomfort must be treated as a potential acute cardiovascular event until clinically cleared by an ECG and troponin biomarker testing.",
        "action": "Seek immediate emergency medical evaluation. Do not delay care or assume it is simple acid reflux."
    },
    {
        "id": "isolated_severe_dyspnea",
        "trigger": ["shortness_breath"],
        "title": "RESPIRATORY DISTRESS WARNING",
        "reason": "Acute difficulty breathing can indicate severe asthma exacerbation, anaphylaxis, pulmonary edema, pneumonia, or hypoxemia.",
        "action": "Seek urgent emergency medical care immediately, particularly if lips appear bluish, speech is broken, or breathing is audibly wheezing or labored."
    },
    {
        "id": "neurological_meningitis_triad",
        "trigger": ["headache", "fever", "stiff_neck"],
        "title": "SUSPECTED MENINGITIS / NEUROLOGICAL EMERGENCY",
        "reason": "The classical triad of severe headache, fever, and neck stiffness strongly suggests central nervous system infection (Bacterial or Viral Meningitis) or intracranial pathology.",
        "action": "Immediate emergency room hospital admission required for lumbar puncture and prompt medical evaluation. Time is critical."
    },
    {
        "id": "seizure_disorder",
        "trigger": ["seizures"],
        "title": "SEIZURE / CONVULSION EMERGENCY",
        "reason": "New-onset seizures, prolonged convulsions, or seizure activity with fever warrants immediate paramedic evaluation to manage airway and prevent status epilepticus.",
        "action": "Call emergency services immediately. Ensure the person is on their side in the recovery position, clear dangerous objects away, and do NOT put anything in their mouth."
    },
    {
        "id": "acute_confusion_syncope",
        "trigger": ["confusion"],
        "title": "ALTERED MENTAL STATUS / SEVERE SEPSIS ALERT",
        "reason": "Sudden disorientation, acute confusion, or slurred responsiveness may be signs of stroke, severe hypoglycemia, toxic encephalopathy, or overwhelming systemic sepsis.",
        "action": "Seek immediate emergency medical evaluation."
    },
    {
        "id": "syncope_loss_consciousness",
        "trigger": ["loss_consciousness"],
        "title": "LOSS OF CONSCIOUSNESS (SYNCOPE) ALERT",
        "reason": "Unexplained fainting or loss of consciousness requires diagnostic evaluation to rule out cardiac arrhythmias, transient ischemic attacks, or internal hemorrhage.",
        "action": "Seek urgent medical evaluation. If the person has not regained full consciousness or has sustained head trauma, call emergency services immediately."
    },
    {
        "id": "acute_gi_bleed",
        "trigger": ["blood_vomit"],
        "title": "ACUTE GASTROINTESTINAL HEMORRHAGE",
        "reason": "Blood in vomitus ('coffee-ground' or bright red) or black tarry stools indicates upper or lower gastrointestinal bleeding requiring hemodynamic monitoring and endoscopy.",
        "action": "Proceed to the emergency department immediately. Do not take aspirin, ibuprofen, or eat solid food."
    }
]

# Reviewed Medical Knowledge Base of Common Syndromes with Differential Diagnoses
SYNDROMES_KNOWLEDGE_BASE = [
    {
        "id": "urti",
        "syndrome": "Upper Respiratory Tract Infection (Common Cold / Acute Pharyngitis)",
        "key_symptoms": ["cough", "cold", "sore_throat", "headache", "fever", "fatigue"],
        "matching_rationale": "Your reported constellation of cough, nasal congestion, and sore throat is classic for viral proliferation in the upper respiratory mucosa.",
        "explanation": "Upper respiratory infections are self-limiting viral illnesses provoked by over 200 viral strains, most commonly Rhinoviruses, Respiratory Syncytial Virus (RSV), or seasonal Coronaviruses. Infection produces localized inflammation of the pharynx and nasal turbinates.",
        "differentials": [
            "Allergic Rhinitis (typically lacks fever; accompanied by itchy watery eyes)",
            "Influenza (more sudden onset with profound full-body muscle aches)",
            "Streptococcal Pharyngitis (severe throat pain without cough; requires rapid swab test)",
            "Acute Viral Bronchitis (cough predominates and may persist 2-3 weeks)"
        ],
        "general_guidance": "Prioritize abundant rest to support immune function. Maintain consistent hydration with warm water, herbal teas, or clear broths. Use saline nasal sprays or steam inhalation to relieve congestion naturally. Gargling with warm salt water can soothe throat irritation.",
        "when_to_seek_care": "Consult a healthcare professional if fever persists beyond 3 days, throat pain prevents swallowing liquids, or if symptoms improve and then suddenly worsen with high fever.",
        "applicable_medicines": ["paracetamol", "saline_spray", "honey_lozenges"]
    },
    {
        "id": "flu_syndrome",
        "syndrome": "Influenza-Like Illness / Viral Syndrome",
        "key_symptoms": ["fever", "fatigue", "joint_pain", "headache", "cough", "cold"],
        "matching_rationale": "High fever combined with intense body aches (myalgia), headache, and profound exhaustion is the clinical hallmark of influenza and systemic viral syndromes.",
        "explanation": "Influenza virus infection causes widespread release of pro-inflammatory cytokines, producing constitutional symptoms including high fever, severe muscle aches, chills, and prostration.",
        "differentials": [
            "COVID-19 (may involve loss of taste/smell or gastrointestinal upset)",
            "Dengue or Mosquito-Borne Arbovirus (in endemic regions; severe retro-orbital eye pain)",
            "Bacterial Sepsis / Early Pyelonephritis (look for urinary symptoms or flank pain)"
        ],
        "general_guidance": "Strict bed rest is essential. Drink plenty of electrolyte-rich fluids (ORS, coconut water, soups). Isolate at home to prevent transmission to vulnerable infants, elderly, or immunocompromised individuals.",
        "when_to_seek_care": "Seek emergency care if breathing becomes rapid or difficult, if chest pressure occurs, or if confusion develops. High-risk patients (pregnant women, elderly, asthmatics) should contact a doctor within 48 hours for antiviral assessment.",
        "applicable_medicines": ["paracetamol", "ibuprofen", "ors_solution"]
    },
    {
        "id": "gastroenteritis",
        "syndrome": "Acute Gastroenteritis (Stomach Flu / Foodborne Illness)",
        "key_symptoms": ["vomiting", "stomach_pain", "fatigue", "fever", "dizziness"],
        "matching_rationale": "Nausea, vomiting, and abdominal cramping indicate acute inflammation of the stomach and intestinal lining.",
        "explanation": "Acute gastroenteritis is most commonly caused by viral agents (Norovirus, Rotavirus) or bacterial food contamination (Salmonella, Campylobacter). The primary physiological danger is rapid fluid and electrolyte depletion.",
        "differentials": [
            "Food Poisoning (rapid onset within 1-6 hours of contaminated food ingestion)",
            "Acute Appendicitis (pain migrating to the right lower abdomen; requires urgent surgical evaluation)",
            "Peptic Ulcer Disease / Gastritis (burning mid-epigastric pain related to meals)"
        ],
        "general_guidance": "Do not attempt to eat heavy meals immediately. Sip Oral Rehydration Salts (ORS) or electrolyte solutions in small amounts every 5-10 minutes. When vomiting subsides, restart bland foods (BRAT diet: bananas, white rice, applesauce, toast).",
        "when_to_seek_care": "Seek medical evaluation if unable to retain fluids for >24 hours, if signs of dehydration appear (extreme thirst, dry mouth, little or dark urine, dizziness upon standing), or if severe abdominal pain persists.",
        "applicable_medicines": ["ors_solution"]
    },
    {
        "id": "headache_syndrome",
        "syndrome": "Tension-Type Headache or Primary Migraine Episode",
        "key_symptoms": ["headache", "fatigue", "dizziness"],
        "matching_rationale": "Reported head pain without acute fever or meningismus points toward common primary headache disorders.",
        "explanation": "Tension headaches involve pericranial muscle tenderness, stress, screen eye fatigue, and dehydration. Migraines involve neurovascular trigeminovascular activation, often with pulsating pain, light/sound sensitivity, or nausea.",
        "differentials": [
            "Dehydration / Caffeine Withdrawal Headache",
            "Sinusitis (accompanied by facial pressure and nasal congestion)",
            "Cervicogenic Headache (neck muscle strain radiating to the temple)"
        ],
        "general_guidance": "Rest in a quiet, dark room. Apply a cool compress to the forehead or warm compress to the back of the neck. Ensure adequate water intake. Practice slow, deep breathing exercises to relieve muscular tension.",
        "when_to_seek_care": "Seek urgent care if headache is sudden and explosive ('worst headache of life'), follows head trauma, or is accompanied by weakness, numbness, or visual field loss.",
        "applicable_medicines": ["paracetamol"]
    },
    {
        "id": "gastritis",
        "syndrome": "Acute Gastritis / Acid Peptic Discomfort",
        "key_symptoms": ["stomach_pain", "vomiting", "fatigue"],
        "matching_rationale": "Epigastric pain with nausea suggests irritation or hyperacidity of the gastric mucosal barrier.",
        "explanation": "Acute gastritis involves inflammation of the stomach lining triggered by NSAID painkillers, alcohol, spicy foods, stress, or Helicobacter pylori infection.",
        "differentials": [
            "Gastroesophageal Reflux Disease (GERD / heartburn)",
            "Biliary Colic / Gallbladder Disease (pain under the right rib cage after fatty meals)",
            "Irritable Bowel Syndrome (IBS)"
        ],
        "general_guidance": "Avoid trigger foods (acidic, fried, spicy, caffeinated, and alcoholic items). Eat small, regular meals rather than large feasts. Remain upright for at least 2 hours after eating.",
        "when_to_seek_care": "Consult a physician if pain is unremitting, radiates to the back, causes unintentional weight loss, or if vomited material resembles dark coffee grounds.",
        "applicable_medicines": ["antacid_otc"]
    }
]

# Educational Medicine Information & Safety Precautions Database
MEDICINES_DATABASE = {
    "paracetamol": {
        "generic_name": "Paracetamol (Acetaminophen)",
        "brand_examples": "Tylenol, Panadol, Calpol, Crocin",
        "purpose": "Mild-to-moderate analgesic (pain reliever) and antipyretic (fever reducer).",
        "symptoms_relieved": "Fever, headache, sore throat pain, and generalized muscle aches.",
        "side_effects": "Generally well tolerated at therapeutic doses. Rare: cutaneous allergic rash, nausea, elevated hepatic transaminases in chronic high doses.",
        "precautions": "Strictly do NOT exceed the maximum adult limit of 4,000 mg (4 grams) in any 24-hour period. In elderly or low-body-weight adults, a lower limit (2,000 to 3,000 mg) is recommended. Avoid alcohol consumption during therapy.",
        "contraindications": [
            "Known hypersensitivity or allergy to Paracetamol/Acetaminophen.",
            "Active severe hepatic impairment, acute hepatitis, or end-stage liver failure."
        ],
        "allergy_check_key": "paracetamol",
        "condition_check_keys": ["liver_disease"],
        "duplicate_warning": "CRITICAL SAFETY WARNING: Hundreds of combination over-the-counter cold, flu, and cough syrups already contain Paracetamol. Always check medicine ingredient labels carefully to avoid accidental double-dosing and toxic liver injury.",
        "interactions": "Warfarin and oral anticoagulants (prolonged regular use may enhance bleeding risk; occasional single doses are safe). Alcohol increases hepatotoxicity risk.",
        "when_to_consult": "Consult a doctor if fever lasts more than 3 days or pain persists beyond 5 days despite treatment. Never give Paracetamol drops intended for infants to older children without measuring.",
        "sources": "WHO Model List of Essential Medicines (2024); British National Formulary (BNF 87); FDA Consumer Health Reference.",
        "reviewed_date": "2026-03-15"
    },
    "ibuprofen": {
        "generic_name": "Ibuprofen",
        "brand_examples": "Advil, Motrin, Nurofen, Brufen",
        "purpose": "Non-Steroidal Anti-Inflammatory Drug (NSAID) providing anti-inflammatory, analgesic, and antipyretic relief.",
        "symptoms_relieved": "Inflammatory pain, headache, dental pain, menstrual cramps, and joint swelling.",
        "side_effects": "Dyspepsia, heartburn, stomach irritation, nausea, fluid retention, mild elevation of blood pressure.",
        "precautions": "Always take with or immediately after food or milk to protect the gastric mucosal barrier. Use the lowest effective dose for the shortest possible duration.",
        "contraindications": [
            "Known allergy or hypersensitivity to Aspirin or other NSAIDs (risk of severe bronchospasm).",
            "Active peptic ulcer, history of recurrent gastrointestinal bleeding or perforation.",
            "Severe renal failure or advanced chronic kidney disease.",
            "Severe heart failure or uncontrolled hypertension.",
            "Third trimester of pregnancy (causes premature closure of fetal ductus arteriosus and oligohydramnios)."
        ],
        "allergy_check_key": "nsaids",
        "condition_check_keys": ["peptic_ulcer", "kidney_disease", "heart_disease", "asthma_copd"],
        "pregnancy_contraindicated": True,
        "duplicate_warning": "Do NOT take Ibuprofen simultaneously with Aspirin, Naproxen, Diclofenac, or other prescription NSAIDs.",
        "interactions": "Anticoagulants (warfarin, apixaban - severe bleeding hazard), ACE inhibitors, diuretics, lithium, methotrexate.",
        "when_to_consult": "Stop immediately and consult a doctor if you experience black stools, vomiting blood, sudden fluid swelling in the ankles, or persistent stomach pain.",
        "sources": "NHS Medicines A-Z (2025); FDA Drug Safety Communication; American College of Gastroenterology.",
        "reviewed_date": "2026-02-20"
    },
    "ors_solution": {
        "generic_name": "Oral Rehydration Salts (ORS)",
        "brand_examples": "WHO-ORS, Pedialyte, Electral, Hydralyte",
        "purpose": "Restores fluid and essential electrolytes (sodium, potassium, chloride, glucose) lost through vomiting, diarrhea, or fever.",
        "symptoms_relieved": "Dehydration, dry mouth, thirst, lightheadedness caused by fluid loss.",
        "side_effects": "None when prepared according to packet dilution instructions. Overly concentrated solutions can cause hypernatremia.",
        "precautions": "Dissolve in the exact volume of clean drinking water specified on the packet. Do not boil prepared solution or mix with sugary fruit juices, milk, or soda.",
        "contraindications": [
            "Intractable vomiting where patient cannot retain any oral fluid (requires IV fluids).",
            "Severe intestinal obstruction or paralytic ileus.",
            "Severe hemodynamic shock or unconsciousness."
        ],
        "allergy_check_key": None,
        "condition_check_keys": ["kidney_disease"],
        "duplicate_warning": "Safe rehydration therapy with no active drug interaction risks.",
        "interactions": "Patients with severe chronic kidney disease should consult a doctor regarding potassium content.",
        "when_to_consult": "Seek medical attention if diarrhea lasts longer than 48 hours or if vomiting prevents oral fluid intake for more than 12-24 hours.",
        "sources": "WHO / UNICEF Guidelines on the Management of Diarrhoea (2024); CDC Yellow Book.",
        "reviewed_date": "2026-01-10"
    },
    "saline_spray": {
        "generic_name": "Isotonic / Hypertonic Saline Nasal Spray",
        "brand_examples": "Ocean, Sterimar, NeilMed, Otrivin Natural",
        "purpose": "Moisturizes dry nasal mucosa, thins tenacious mucus, and clears particulate matter without chemical vasoconstrictors.",
        "symptoms_relieved": "Nasal stuffiness, dry crusting, sinus pressure, post-nasal drip.",
        "side_effects": "Mild transient nasal tingling or sneezing upon first application.",
        "precautions": "Clean the spray nozzle after each use. Do not share the bottle with family members to prevent cross-contamination.",
        "contraindications": ["None for pure sodium chloride saline."],
        "allergy_check_key": None,
        "condition_check_keys": [],
        "duplicate_warning": "Safe alternative to medicated decongestant sprays (such as oxymetazoline), which cause rebound congestion (rhinitis medicamentosa) if used for >3-5 days.",
        "interactions": "None.",
        "when_to_consult": "Consult a doctor if nasal congestion is accompanied by severe facial swelling or vision changes.",
        "sources": "American Academy of Otolaryngology; Cochrane Reviews on Nasal Irrigation.",
        "reviewed_date": "2026-02-12"
    },
    "honey_lozenges": {
        "generic_name": "Demulcent Lozenges / Pure Honey (Ages 1+ only)",
        "brand_examples": "Strepsils, Halls, Fishermans Friend, Natural Honey",
        "purpose": "Coats the irritated pharyngeal lining to reduce sensory nerve stimulation and suppress tickly dry coughing.",
        "symptoms_relieved": "Sore throat scratching, dry non-productive cough, pharyngeal dryness.",
        "side_effects": "None for standard lozenges. Sugar content may be relevant for diabetic patients.",
        "precautions": "INFANT BOTULISM WARNING: Never give natural honey in any form to infants under 1 year of age due to the risk of Clostridium botulinum spores.",
        "contraindications": [
            "Children under 12 months of age (for natural honey products).",
            "Choking hazard: Lozenges should not be given to young children under 5 years."
        ],
        "allergy_check_key": None,
        "condition_check_keys": ["diabetes"],
        "duplicate_warning": "Check if lozenge contains local anesthetic (e.g. benzocaine) or antiseptics if taking other medications.",
        "interactions": "None.",
        "when_to_consult": "Seek medical review if severe throat pain prevents swallowing saliva.",
        "sources": "WHO Cough and Cold Guidelines; American Academy of Pediatrics.",
        "reviewed_date": "2026-01-25"
    }
}
