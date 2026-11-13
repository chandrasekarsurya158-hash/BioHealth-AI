"""
Clinical Biomarker Reference Database & Diagnostic Range Knowledge Base (Module 4B)
-----------------------------------------------------------------------------------
Peer-reviewed clinical ranges for routine hematology, biochemistry, lipid profile,
glycemic control, liver function, and renal function markers.
Sources: WHO, American Association for Clinical Chemistry (AACC), Mayo Clinic Labs,
British National Health Service (NHS).
"""

BIOMARKER_DATABASE = {
    "hemoglobin": {
        "display_name": "Hemoglobin (Hb)",
        "category": "Complete Blood Count (CBC)",
        "default_unit": "g/dL",
        "aliases": [
            "hemoglobin", "haemoglobin", "hb", "hgb", "total hemoglobin"
        ],
        "ref_min": 12.0,
        "ref_max": 17.5,
        "critical_low": 7.0,
        "critical_high": 20.0,
        "interpretations": {
            "NORMAL": "Hemoglobin level is within optimal physiological range for oxygen transport.",
            "LOW": "Microcytic/normocytic anemia indicated. Common etiologies include iron deficiency, chronic blood loss, nutritional insufficiency (B12/folate), or chronic systemic disease. May cause fatigue, pallor, and lightheadedness.",
            "HIGH": "Elevated hemoglobin (polycythemia / erythrocytosis). Potential causes include chronic dehydration, cigarette smoking, chronic hypoxemia (COPD/high altitude), or myeloproliferative disorders. Increases blood viscosity.",
            "CRITICAL_LOW": "SEVERE LIFE-THREATENING ANEMIA. Significant risk of myocardial ischemia and tissue hypoxia. Immediate emergency evaluation and potential transfusion required.",
            "CRITICAL_HIGH": "CRITICAL HYPERVISCOSITY RISK. Extreme erythrocytosis with severe thrombosis and stroke hazard."
        }
    },
    "fasting_glucose": {
        "display_name": "Fasting Blood Glucose (FBG)",
        "category": "Metabolic & Glycemic Profile",
        "default_unit": "mg/dL",
        "aliases": [
            "fasting blood sugar", "fbs", "fasting glucose", "fbg", "plasma glucose, fasting", "glucose - fasting"
        ],
        "ref_min": 70.0,
        "ref_max": 99.0,
        "critical_low": 50.0,
        "critical_high": 300.0,
        "interpretations": {
            "NORMAL": "Normal fasting plasma glucose indicating healthy carbohydrate homeostasis.",
            "LOW": "Hypoglycemia detected. May result from excessive insulin/diabetic medication, skipped meals, intense exertion, or adrenal insufficiency. Symptoms include sweating, tremors, palpitations, and confusion.",
            "HIGH": "Hyperglycemia detected. Fasting levels between 100-125 mg/dL suggest Impaired Fasting Glucose (Prediabetes); levels >= 126 mg/dL on repeated testing indicate Diabetes Mellitus. Confirmatory HbA1c is strongly advised.",
            "CRITICAL_LOW": "CRITICAL SEVERE HYPOGLYCEMIA. Acute neuroglycopenic emergency. Ingestion of fast-acting carbohydrates or emergency glucagon/IV dextrose required immediately.",
            "CRITICAL_HIGH": "CRITICAL SEVERE HYPERGLYCEMIA. Severe risk of Diabetic Ketoacidosis (DKA) or Hyperosmolar Hyperglycemic State (HHS). Immediate hospital triage needed."
        }
    },
    "hba1c": {
        "display_name": "Glycated Hemoglobin (HbA1c)",
        "category": "Metabolic & Glycemic Profile",
        "default_unit": "%",
        "aliases": [
            "hba1c", "glycated hemoglobin", "glycosylated hemoglobin", "a1c", "glycohemoglobin"
        ],
        "ref_min": 4.0,
        "ref_max": 5.6,
        "critical_low": 3.0,
        "critical_high": 12.0,
        "interpretations": {
            "NORMAL": "Normal long-term glycemic control over preceding 8-12 weeks.",
            "LOW": "Subnormal HbA1c may occur with shortened erythrocyte lifespan, hemolytic anemia, chronic liver disease, or frequent severe hypoglycemic episodes.",
            "HIGH": "Elevated HbA1c. Range 5.7% - 6.4% indicates Prediabetes (elevated metabolic risk). Value >= 6.5% satisfies the diagnostic threshold for Diabetes Mellitus.",
            "CRITICAL_LOW": "Markedly low HbA1c requiring investigation of RBC hemolysis or recurrent hypoglycemia.",
            "CRITICAL_HIGH": "Extremely poorly controlled diabetes mellitus with significant risk of microvascular and macrovascular end-organ damage."
        }
    },
    "wbc": {
        "display_name": "Total Leukocyte Count (WBC)",
        "category": "Complete Blood Count (CBC)",
        "default_unit": "/mcL",
        "aliases": [
            "wbc", "total leukocyte count", "tlc", "white blood cells", "total wbc", "leukocytes"
        ],
        "ref_min": 4000.0,
        "ref_max": 11000.0,
        "critical_low": 2000.0,
        "critical_high": 30000.0,
        "interpretations": {
            "NORMAL": "Leukocyte count is within normal immune defense baseline.",
            "LOW": "Leukopenia detected. Indicates increased vulnerability to bacterial/fungal infections. Common causes include acute viral infections, autoimmune conditions, bone marrow suppression, or drug-induced myelosuppression.",
            "HIGH": "Leukocytosis detected. Strongly suggests acute bacterial infection, systemic inflammatory response, tissue necrosis, severe physiological stress, or hematological proliferation.",
            "CRITICAL_LOW": "CRITICAL NEUTROPENIA / AGRANULOCYTOSIS. Severe immunocompromise with acute vulnerability to life-threatening sepsis.",
            "CRITICAL_HIGH": "CRITICAL LEUKOCYTOSIS / LEUKEMOID REACTION. Requires immediate urgent hematological evaluation to rule out acute leukemia or catastrophic infection."
        }
    },
    "rbc": {
        "display_name": "Red Blood Cell Count (RBC)",
        "category": "Complete Blood Count (CBC)",
        "default_unit": "million/mcL",
        "aliases": [
            "rbc", "red blood cell count", "erythrocytes", "total rbc", "erythrocyte count"
        ],
        "ref_min": 4.2,
        "ref_max": 5.9,
        "critical_low": 2.5,
        "critical_high": 7.5,
        "interpretations": {
            "NORMAL": "Erythrocyte mass is physiologically adequate for systemic tissue oxygen delivery.",
            "LOW": "Erythrocytopenia correlates with anemia, chronic nutritional deficiency, renal failure (reduced erythropoietin), or bone marrow disorders.",
            "HIGH": "Erythrocytosis indicates secondary compensation to hypoxemia, hemoconcentration, or primary marrow disorder.",
            "CRITICAL_LOW": "Critical anemia with marked oxygen-carrying deficit.",
            "CRITICAL_HIGH": "Severe erythrocytosis presenting microvascular occlusion and hyperviscosity hazards."
        }
    },
    "platelets": {
        "display_name": "Platelet Count",
        "category": "Complete Blood Count (CBC)",
        "default_unit": "/mcL",
        "aliases": [
            "platelet count", "platelets", "thrombocytes", "plt", "total platelets"
        ],
        "ref_min": 150000.0,
        "ref_max": 450000.0,
        "critical_low": 30000.0,
        "critical_high": 1000000.0,
        "interpretations": {
            "NORMAL": "Normal thrombocyte count supporting intact primary hemostasis and clotting.",
            "LOW": "Thrombocytopenia detected. Elevation in spontaneous bruising, petechiae, or mucosal bleeding risks. Causes include viral infections (e.g. Dengue), autoimmune destruction (ITP), splenic sequestration, or marrow suppression.",
            "HIGH": "Thrombocytosis detected. May represent reactive response to iron deficiency, acute infection/inflammation, or essential thrombocythemia. Potential risk for thrombotic events.",
            "CRITICAL_LOW": "CRITICAL THROMBOCYTOPENIA (<30,000/mcL). High risk of spontaneous internal, gastrointestinal, or intracranial hemorrhage. Immediate hospital admission required.",
            "CRITICAL_HIGH": "EXTREME THROMBOCYTOSIS. High paradox of microvascular thrombosis and acquired bleeding diathesis."
        }
    },
    "total_cholesterol": {
        "display_name": "Total Cholesterol",
        "category": "Lipid Profile",
        "default_unit": "mg/dL",
        "aliases": [
            "total cholesterol", "cholesterol, total", "serum cholesterol", "cholesterol"
        ],
        "ref_min": 125.0,
        "ref_max": 200.0,
        "critical_low": 80.0,
        "critical_high": 350.0,
        "interpretations": {
            "NORMAL": "Desirable circulating cholesterol level associated with lower baseline cardiovascular risk.",
            "LOW": "Hypocholesterolemia may reflect severe malnutrition, hyperthyroidism, malabsorption, or advanced chronic liver disease.",
            "HIGH": "Hypercholesterolemia detected (>=200 mg/dL). Elevated atherosclerotic cardiovascular disease (ASCVD) risk. Dietary modification, exercise, and clinical risk scoring recommended.",
            "CRITICAL_LOW": "Markedly low cholesterol indicating metabolic compromise.",
            "CRITICAL_HIGH": "Severely elevated cholesterol suggesting familial hypercholesterolemia or major vascular event risk."
        }
    },
    "triglycerides": {
        "display_name": "Triglycerides",
        "category": "Lipid Profile",
        "default_unit": "mg/dL",
        "aliases": [
            "triglycerides", "serum triglycerides", "tg", "triglyceride"
        ],
        "ref_min": 50.0,
        "ref_max": 150.0,
        "critical_low": 30.0,
        "critical_high": 500.0,
        "interpretations": {
            "NORMAL": "Optimal fasting serum triglyceride concentration.",
            "LOW": "Rarely clinically significant; seen with very low-fat dietary intake or hyperthyroidism.",
            "HIGH": "Hypertriglyceridemia (>=150 mg/dL). Strongly linked to metabolic syndrome, insulin resistance, physical inactivity, and excessive refined carbohydrate intake.",
            "CRITICAL_LOW": "Subnormal triglyceride level.",
            "CRITICAL_HIGH": "CRITICAL SEVERE HYPERTRIGLYCERIDEMIA (>=500 mg/dL). Substantial risk for acute necrotic pancreatitis. Immediate medical therapy required."
        }
    },
    "creatinine": {
        "display_name": "Serum Creatinine",
        "category": "Renal Function Panel",
        "default_unit": "mg/dL",
        "aliases": [
            "serum creatinine", "creatinine", "creat", "s. creatinine"
        ],
        "ref_min": 0.6,
        "ref_max": 1.2,
        "critical_low": 0.3,
        "critical_high": 4.0,
        "interpretations": {
            "NORMAL": "Normal glomerular filtration indicator reflecting healthy renal clearance.",
            "LOW": "Low creatinine is typically benign and reflects low skeletal muscle mass or advanced sarcopenia.",
            "HIGH": "Elevated creatinine indicates impaired renal excretory capacity (Acute Kidney Injury or Chronic Kidney Disease). Nephrology evaluation, hydration assessment, and medication dosage review indicated.",
            "CRITICAL_LOW": "Marked reduction in muscle mass index.",
            "CRITICAL_HIGH": "CRITICAL RENAL DYSFUNCTION / AZOTEMIA. Severe risk of uremia, metabolic acidosis, and fluid overload. Immediate urgent nephrology consultation needed."
        }
    },
    "blood_urea": {
        "display_name": "Blood Urea Nitrogen (BUN)",
        "category": "Renal Function Panel",
        "default_unit": "mg/dL",
        "aliases": [
            "blood urea nitrogen", "bun", "urea", "blood urea", "serum urea"
        ],
        "ref_min": 7.0,
        "ref_max": 20.0,
        "critical_low": 3.0,
        "critical_high": 80.0,
        "interpretations": {
            "NORMAL": "Normal urea concentration and nitrogenous waste processing.",
            "LOW": "Low BUN may occur with severe protein malnutrition, overhydration, or severe liver disease.",
            "HIGH": "Prerenal azotemia (dehydration, congestive heart failure, gastrointestinal hemorrhage) or intrinsic renal impairment.",
            "CRITICAL_LOW": "Subnormal nitrogenous turnover.",
            "CRITICAL_HIGH": "Severe uremic toxicity risk requiring prompt inpatient medical evaluation."
        }
    },
    "bilirubin": {
        "display_name": "Total Bilirubin",
        "category": "Liver Function Panel (LFT)",
        "default_unit": "mg/dL",
        "aliases": [
            "total bilirubin", "bilirubin, total", "t. bilirubin", "serum bilirubin"
        ],
        "ref_min": 0.2,
        "ref_max": 1.2,
        "critical_low": 0.1,
        "critical_high": 12.0,
        "interpretations": {
            "NORMAL": "Normal hepatic breakdown and biliary excretion of heme pigments.",
            "LOW": "No clinical pathology associated with subnormal bilirubin levels.",
            "HIGH": "Hyperbilirubinemia detected. Visual jaundice/scleral icterus typically occurs at >2.5 mg/dL. Etiologies include biliary obstruction, hepatitis, cirrhosis, or accelerated hemolysis.",
            "CRITICAL_LOW": "Physiologically benign.",
            "CRITICAL_HIGH": "CRITICAL HYPERBILIRUBINEMIA. Marked hepatic decompensation or high-grade biliary tree obstruction."
        }
    },
    "sgpt_alt": {
        "display_name": "Alanine Aminotransferase (ALT / SGPT)",
        "category": "Liver Function Panel (LFT)",
        "default_unit": "U/L",
        "aliases": [
            "sgpt", "alt", "alanine aminotransferase", "alanine transaminase", "sgpt/alt"
        ],
        "ref_min": 7.0,
        "ref_max": 56.0,
        "critical_low": 0.0,
        "critical_high": 500.0,
        "interpretations": {
            "NORMAL": "Normal intracellular enzyme levels confirming hepatocyte integrity.",
            "LOW": "Clinically unremarkable; reflects normal baseline.",
            "HIGH": "Hepatocellular injury or inflammation. Causes include metabolic dysfunction-associated steatotic liver disease (NAFLD), viral hepatitis, alcohol use, or hepatotoxic medications (e.g. Paracetamol overdose).",
            "CRITICAL_LOW": "Normal baseline.",
            "CRITICAL_HIGH": "ACUTE HEPATOCELLULAR NECROSIS. Severe ischemic, toxic, or viral liver insult requiring emergency hepatology admission."
        }
    }
}

