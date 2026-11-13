"""
Comprehensive Verified Pharmacopeia Knowledge Base (Module 4E)
--------------------------------------------------------------
Authoritative clinical pharmacopeia data referencing WHO Essential Medicines,
British National Formulary (BNF), and FDA Drug Safety Communications.
Provides verified uses, precautions, warnings, side effects, contraindications,
and clinical references for search queries.
"""

VERIFIED_MEDICINES = [
    {
        "name": "Cetirizine",
        "generic_name": "Cetirizine Hydrochloride",
        "brand_examples": "Zyrtec, Cetzine, Alerid, Reactine",
        "category": "Second-Generation Antihistamine",
        "prescription_type": "OTC",
        "uses": "Provides rapid, non-drowsy symptomatic relief for allergic rhinitis (hay fever), sneezing, runny/itchy nose, itchy watery red eyes, and chronic idiopathic urticaria (allergic hives and skin itching).",
        "precautions": "Caution should be exercised when operating heavy machinery, driving, or performing hazardous tasks until your individual response to the medication is determined. Avoid concurrent consumption of alcohol or central nervous system sedatives as additive drowsiness may occur. Elderly patients may experience increased anticholinergic sensitivity.",
        "warnings": "Dose reduction (5 mg daily instead of 10 mg) is clinically mandatory in individuals with moderate to severe renal impairment (creatinine clearance < 50 mL/min). Stop taking cetirizine at least 48 to 72 hours before diagnostic skin prick allergy testing to prevent false-negative test results.",
        "side_effects": "Generally well-tolerated. Low-incidence side effects include mild transient drowsiness, dry mouth, mild headache, fatigue, pharyngitis, and gastrointestinal discomfort.",
        "contraindications": "Known hypersensitivity or severe allergic reaction to cetirizine, hydroxyzine, or any piperazine derivatives. End-stage renal disease (creatinine clearance < 10 mL/min) undergoing hemodialysis.",
        "interactions": "Central nervous system depressants (benzodiazepines, opioids, sleeping aids) and alcohol amplify sedative effects. Theophylline slightly decreases cetirizine clearance.",
        "last_reviewed_date": "2026-03-01",
        "references": [
            {"source_name": "British National Formulary (BNF 87)", "publisher": "BMJ Group & Royal Pharmaceutical Society", "year": 2025},
            {"source_name": "FDA Drug Safety Communication", "publisher": "US Food and Drug Administration", "year": 2025}
        ]
    },
    {
        "name": "Paracetamol",
        "generic_name": "Paracetamol / Acetaminophen",
        "brand_examples": "Crocin, Tylenol, Panadol, Calpol, Dolo 650",
        "category": "Analgesic & Antipyretic",
        "prescription_type": "OTC",
        "uses": "First-line therapy for mild to moderate pain (tension headache, toothache, musculoskeletal ache, menstrual cramping) and reduction of elevated body temperature (fever) in viral or bacterial illness.",
        "precautions": "Strictly do NOT exceed 4,000 mg (4 grams) in any 24-hour window for adults (maximum 2,000–3,000 mg in chronic liver disease or frail elderly). Always verify ingredient labels of combination cold, sinus, and cough remedies to avoid inadvertent fatal overdose.",
        "warnings": "BLACK BOX / HEPATOTOXICITY WARNING: Acute acetaminophen overdose is a leading cause of acute liver failure. Concurrent consumption of 3 or more alcoholic beverages daily significantly increases hepatotoxicity hazards.",
        "side_effects": "Rare at standard therapeutic doses. Hypersensitivity skin rash, nausea. Toxic overdose causes acute hepatic transaminase elevation, jaundice, and hepatic encephalopathy.",
        "contraindications": "Severe active liver failure, acute hepatitis, decompensated cirrhosis, or known hypersensitivity to paracetamol.",
        "interactions": "Prolonged daily regular use may enhance the anticoagulant effect of Warfarin (monitoring INR advised). Concomitant enzyme-inducing anti-epileptic drugs (carbamazepine, phenytoin) increase toxic metabolite generation.",
        "last_reviewed_date": "2026-03-15",
        "references": [
            {"source_name": "WHO Model List of Essential Medicines", "publisher": "World Health Organization", "year": 2024},
            {"source_name": "British National Formulary (BNF 87)", "publisher": "BMJ Group", "year": 2025}
        ]
    },
    {
        "name": "Ibuprofen",
        "generic_name": "Ibuprofen",
        "brand_examples": "Advil, Motrin, Nurofen, Brufen, Combiflam (combination)",
        "category": "Non-Steroidal Anti-Inflammatory Drug (NSAID)",
        "prescription_type": "OTC",
        "uses": "Relieves acute inflammatory pain, headache, dental pain, primary dysmenorrhea (menstrual cramps), osteoarthritis, rheumatoid joint inflammation, and fever.",
        "precautions": "Always administer with or immediately following meals, milk, or food to shield the gastric mucosal barrier. Employ the lowest effective dose for the briefest possible clinical duration. Maintain robust hydration to protect renal perfusion.",
        "warnings": "BLACK BOX CARDIOVASCULAR & GI WARNING: Chronic NSAID therapy increases the risk of serious gastrointestinal ulceration, bleeding, and perforation. NSAIDs elevate the relative risk of myocardial infarction and stroke, and should be avoided immediately prior to or following coronary artery bypass graft (CABG) surgery.",
        "side_effects": "Dyspepsia, heartburn, epigastric discomfort, nausea, fluid retention, mild hypertension elevation, peripheral edema.",
        "contraindications": "Active peptic ulcer or history of recurrent GI bleeding; third trimester of pregnancy (premature closure of fetal ductus arteriosus); severe heart failure (NYHA Class IV); advanced chronic kidney disease; history of asthma or anaphylaxis triggered by Aspirin/NSAIDs.",
        "interactions": "Anticoagulants (warfarin, apixaban, rivaroxaban) produce severe hemorrhage hazard. Decreases antihypertensive efficacy of ACE inhibitors and diuretics. Increases serum lithium and methotrexate levels.",
        "last_reviewed_date": "2026-02-20",
        "references": [
            {"source_name": "NHS Medicines A-Z", "publisher": "UK National Health Service", "year": 2025},
            {"source_name": "American College of Gastroenterology NSAID Guidelines", "publisher": "ACG", "year": 2024}
        ]
    },
    {
        "name": "Amoxicillin",
        "generic_name": "Amoxicillin Trihydrate",
        "brand_examples": "Amoxil, Augmentin (with Clavulanate), Mox",
        "category": "Broad-Spectrum Beta-Lactam Antibiotic",
        "prescription_type": "Prescription Only",
        "uses": "Treats susceptible bacterial infections including acute bacterial otitis media, streptococcal pharyngitis, sinusitis, community-acquired bacterial pneumonia, skin infections, and urinary tract infections. COMPLETELY INEFFECTIVE against viral colds, flu, and COVID-19.",
        "precautions": "Complete the full prescribed duration of therapy even if symptoms resolve early, to prevent antibiotic resistance and disease relapse. Diarrhea is common; contact a clinician if watery diarrhea persists (rule out Clostridioides difficile colitis).",
        "warnings": "ANAPHYLAXIS ALERT: Serious and occasionally fatal anaphylactic allergic reactions occur in individuals with a history of penicillin or beta-lactam hypersensitivity. In patients with infectious mononucleosis (Epstein-Barr virus), amoxicillin provokes a generalized erythematous maculopapular rash.",
        "side_effects": "Diarrhea, nausea, vomiting, abdominal cramping, transient oral candidiasis (thrush), skin rash.",
        "contraindications": "Confirmed hypersensitivity to amoxicillin, ampicillin, or any beta-lactam penicillin antibiotics.",
        "interactions": "May decrease efficacy of combined oral hormonal contraceptives (barrier protection advised). Concomitant allopurinol increases skin rash incidence. Probenecid decreases renal clearance.",
        "last_reviewed_date": "2026-02-15",
        "references": [
            {"source_name": "Infectious Diseases Society of America (IDSA)", "publisher": "IDSA Guidelines", "year": 2025},
            {"source_name": "WHO AWaRe Antibiotic Classification", "publisher": "World Health Organization", "year": 2024}
        ]
    },
    {
        "name": "Metformin",
        "generic_name": "Metformin Hydrochloride",
        "brand_examples": "Glucophage, Glycomet, Fortamet, Riomet",
        "category": "Biguanide Oral Antidiabetic Agent",
        "prescription_type": "Prescription Only",
        "uses": "First-line pharmacological management for Type 2 Diabetes Mellitus; diminishes hepatic gluconeogenesis, lowers intestinal glucose absorption, and boosts peripheral insulin sensitivity without provoking hypoglycemia.",
        "precautions": "Take with or immediately after meals to minimize gastrointestinal disturbances. Schedule routine annual serum creatinine, eGFR, and Vitamin B12 monitoring (chronic therapy decreases ileal B12 uptake). Withhold temporarily prior to radiological studies involving iodinated intravascular radiocontrast.",
        "warnings": "BLACK BOX LACTIC ACIDOSIS WARNING: Rare but life-threatening accumulation of lactic acid occurs predominantly in patients with acute renal impairment, hypoperfusion, severe congestive heart failure, severe sepsis, or acute alcoholism.",
        "side_effects": "Transient diarrhea, nausea, abdominal fullness, flatulence, metallic taste in mouth, subclinical Vitamin B12 deficiency.",
        "contraindications": "Severe renal impairment (eGFR < 30 mL/min/1.73m²); acute or chronic metabolic acidosis (including diabetic ketoacidosis); acute heart failure or cardiogenic shock; severe hepatic dysfunction.",
        "interactions": "Iodinated radiocontrast agents (withhold metformin 48 hours prior and post-procedure). Alcohol potentiates the effect of metformin on lactate metabolism.",
        "last_reviewed_date": "2026-01-20",
        "references": [
            {"source_name": "ADA Standards of Medical Care in Diabetes", "publisher": "American Diabetes Association", "year": 2025},
            {"source_name": "EASD Clinical Diabetes Compendium", "publisher": "European Association for Study of Diabetes", "year": 2024}
        ]
    },
    {
        "name": "Omeprazole",
        "generic_name": "Omeprazole Magnesium",
        "brand_examples": "Prilosec, Omez, Losec, Zegerid",
        "category": "Proton Pump Inhibitor (PPI)",
        "prescription_type": "OTC / Prescription",
        "uses": "Suppresses gastric acid secretion for Gastroesophageal Reflux Disease (GERD), erosive esophagitis, active peptic and duodenal ulcers, and eradication of Helicobacter pylori (combined with antibiotics).",
        "precautions": "Administer once daily in the morning, 30 to 60 minutes prior to the first meal of the day. Avoid long-term continuous use (>12 weeks) without medical oversight due to risks of hypomagnesemia, impaired calcium absorption, and bone fracture.",
        "warnings": "Long-term profound acid suppression is associated with increased risk of Clostridioides difficile-associated diarrhea, community-acquired pneumonia, subacute cutaneous lupus erythematosus, and Vitamin B12 malabsorption.",
        "side_effects": "Headache, abdominal pain, constipation, flatulence, nausea, diarrhea.",
        "contraindications": "Hypersensitivity to omeprazole or any substituted benzimidazoles (e.g. pantoprazole, esomeprazole).",
        "interactions": "Significantly decreases antiplatelet activation of Clopidogrel (CYP2C19 inhibition). Decreases absorption of drugs requiring acidic gastric pH (ketoconazole, iron salts, atazanavir). Increases serum methotrexate levels.",
        "last_reviewed_date": "2026-02-10",
        "references": [
            {"source_name": "American Gastroenterological Association (AGA) Clinical Practice Updates", "publisher": "AGA", "year": 2025},
            {"source_name": "British National Formulary (BNF 87)", "publisher": "BMJ Group", "year": 2025}
        ]
    },
    {
        "name": "Azithromycin",
        "generic_name": "Azithromycin Dihydrate",
        "brand_examples": "Zithromax, Z-Pak, Azithral",
        "category": "Macrolide Antibiotic",
        "prescription_type": "Prescription Only",
        "uses": "Treats atypical bacterial respiratory infections (chlamydial, mycoplasmal pneumonia, acute bacterial exacerbations of COPD, pertussis), skin infections, and certain sexually transmitted infections.",
        "precautions": "Take once daily. Can be taken with or without food, though food improves tolerability. Complete the full prescribed course. Do not take with aluminum or magnesium-containing antacids simultaneously.",
        "warnings": "CARDIOVASCULAR QT PROLONGATION WARNING: Can cause abnormal changes in the electrical activity of the heart (QT interval prolongation, Torsades de Pointes), which can be fatal in patients with pre-existing heart disease or electrolyte imbalances.",
        "side_effects": "Diarrhea, abdominal cramps, nausea, transient taste alterations, headache.",
        "contraindications": "Known hypersensitivity to azithromycin, erythromycin, or any macrolide/ketolide antibiotics. History of cholestatic jaundice or hepatic dysfunction associated with prior azithromycin use.",
        "interactions": "Avoid concurrent use with other QT-prolonging medications (amiodarone, sotalol, citalopram). Antacids reduce peak serum concentration.",
        "last_reviewed_date": "2026-01-25",
        "references": [
            {"source_name": "FDA Drug Safety Communication on Azithromycin QT Risk", "publisher": "US FDA", "year": 2024},
            {"source_name": "WHO AWaRe Classification", "publisher": "WHO", "year": 2024}
        ]
    },
    {
        "name": "Oral Rehydration Salts (ORS)",
        "generic_name": "Oral Rehydration Salts (WHO Formula)",
        "brand_examples": "Electral, Pedialyte, Hydralyte, WHO-ORS",
        "category": "Electrolyte & Fluid Replenishment",
        "prescription_type": "OTC",
        "uses": "Restores water and essential electrolytes (sodium, potassium, chloride, citrate, glucose) lost due to acute diarrhea, vomiting, excessive sweating, or heat exhaustion.",
        "precautions": "Dissolve packet contents in the exact volume of clean drinking water specified on packaging (standard packet dissolves in 1 liter). Do not boil prepared solution and do not mix with sweetened juices, milk, or soda.",
        "warnings": "Do not rely exclusively on oral rehydration if patient exhibits signs of severe dehydration, hemodynamic shock, intractable persistent vomiting, or inability to swallow.",
        "side_effects": "None when diluted according to instructions. Overly concentrated solution can provoke hypernatremia.",
        "contraindications": "Paralytic ileus, severe intestinal obstruction, intractable continuous vomiting, and acute renal failure with anuria.",
        "interactions": "Patients with severe chronic kidney disease or taking potassium-sparing diuretics should monitor potassium intake.",
        "last_reviewed_date": "2026-01-10",
        "references": [
            {"source_name": "WHO / UNICEF Diarrhoea Management Guidelines", "publisher": "WHO / UNICEF", "year": 2024}
        ]
    }
]

