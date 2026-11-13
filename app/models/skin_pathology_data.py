"""
Dermatological Pathology Knowledge Base (Module 3)
Based on the HAM10000 Benchmark Research Dataset (Tschandl et al., Nature 2018).
Provides clinical descriptions, urgency ratings, and physician evaluation advisories.
"""

SKIN_CLASSES = [
    "nv",     # Melanocytic Nevus (Benign Mole)
    "mel",    # Melanoma (High Urgency)
    "bkl",    # Benign Keratosis (Seborrheic Keratosis)
    "bcc",    # Basal Cell Carcinoma
    "akiec",  # Actinic Keratosis / Bowen's Disease (Precancerous)
    "vasc",   # Vascular Lesion (Angioma)
    "df"      # Dermatofibroma (Benign)
]

SKIN_DISEASE_DETAILS = {
    "nv": {
        "display_name": "Melanocytic Nevus (Common Mole)",
        "code": "nv",
        "category_type": "Benign Pigmented Lesion",
        "urgency": "Low (Routine Observation)",
        "urgency_badge": "bg-success",
        "is_benign": True,
        "description": "A benign proliferation of melanocytes (pigment-producing cells). Characterized by uniform pigment, symmetric circular or oval contours, and well-demarcated smooth borders.",
        "risk_notes": "Very low malignant potential. Most adults possess 10 to 40 benign nevi. Routine self-examination recommended.",
        "abcde_assessment": "Generally passes ABCDE criteria: symmetric, even border, uniform tan/brown color, stable diameter.",
        "recommendation": "Self-monitor monthly using a mirror. Schedule standard annual full-body skin examination with a dermatologist. Seek immediate evaluation if changes in size, shape, or color occur."
    },
    "mel": {
        "display_name": "Melanoma (Malignant Melanocytic Lesion)",
        "code": "mel",
        "category_type": "Malignant Neoplasm (High Urgency)",
        "urgency": "High (Urgent Dermatologist Referral)",
        "urgency_badge": "bg-danger",
        "is_benign": False,
        "description": "A serious, invasive malignancy arising from cutaneous melanocytes. Often presents as an asymmetrical lesion with irregular notched borders, multiple color variations (black, brown, blue, red), and progressive enlargement.",
        "risk_notes": "Early surgical excision significantly improves prognosis. Can metastasize via lymphatic and hematogenous routes if neglected.",
        "abcde_assessment": "High suspicion across ABCDE: Asymmetrical axis, scalloped/notched borders, variegated pigment, diameter often >6mm, actively evolving.",
        "recommendation": "URGENT MEDICAL EVALUATION MANDATORY. Immediately consult a certified dermatologist or surgical oncologist for dermoscopy and excisional biopsy. Do NOT delay or attempt home treatments."
    },
    "bkl": {
        "display_name": "Benign Keratosis-like Lesions",
        "code": "bkl",
        "category_type": "Benign Keratinocytic Growth",
        "urgency": "Low (Benign)",
        "urgency_badge": "bg-success",
        "is_benign": True,
        "description": "Encompasses seborrheic keratoses, solar lentigines ('age/sun spots'), and lichen planus-like keratoses. Commonly presents as waxy, 'pasted-on' brown or tan plaques with horn cysts.",
        "risk_notes": "Completely benign non-cancerous skin growths common in older adults. Harmless, though occasionally irritated by clothing friction.",
        "abcde_assessment": "Often irregular or raised, but exhibits characteristic keratosic surface features, dull waxy texture, and lack of deep pigment migration.",
        "recommendation": "No medical intervention required unless the lesion causes chronic itching, bleeding, or cosmetic distress. A dermatologist can confirm through dermoscopy or remove via cryotherapy."
    },
    "bcc": {
        "display_name": "Basal Cell Carcinoma (BCC)",
        "code": "bcc",
        "category_type": "Non-Melanoma Cutaneous Carcinoma",
        "urgency": "Moderate-High (Medical Evaluation Required)",
        "urgency_badge": "bg-warning text-dark",
        "is_benign": False,
        "description": "The most common form of skin cancer, originating in basal cells of the epidermis. Classically appears as a pearly, translucent pink bump with prominent telangiectasias (spider veins) and rolled borders.",
        "risk_notes": "Slow-growing with extremely low metastatic potential, but can cause substantial local tissue destruction and ulceration ('rodent ulcer') if untreated.",
        "abcde_assessment": "Often displays central ulceration, pearly translucence, and delicate arborizing telangiectasias under magnification.",
        "recommendation": "Consult a dermatologist or Mohs micrographic surgeon for confirmation and complete surgical excision, curettage, or topical therapy."
    },
    "akiec": {
        "display_name": "Actinic Keratosis / Bowen's Disease",
        "code": "akiec",
        "category_type": "Pre-cancerous / Intraepithelial Carcinoma",
        "urgency": "Moderate (Clinical Evaluation Recommended)",
        "urgency_badge": "bg-warning text-dark",
        "is_benign": False,
        "description": "Rough, scaly, sandpaper-like patches caused by cumulative ultraviolet radiation exposure. Represents dysplasia of epidermal keratinocytes (carcinoma in situ).",
        "risk_notes": "Precursor lesion: 5% to 10% can progress into invasive Squamous Cell Carcinoma (SCC) over several years.",
        "abcde_assessment": "Persistent rough, erythematous (red), scaly plaque that fails to heal. Often more palpable than visible.",
        "recommendation": "Schedule evaluation with a dermatologist for destructive treatment (liquid nitrogen cryotherapy, photodynamic therapy, or topical 5-fluorouracil)."
    },
    "vasc": {
        "display_name": "Vascular Skin Lesion",
        "code": "vasc",
        "category_type": "Benign Vascular Proliferation",
        "urgency": "Low (Routine Observation)",
        "urgency_badge": "bg-info text-dark",
        "is_benign": True,
        "description": "Includes cherry angiomas, pyogenic granulomas, angiokeratomas, and subungual hematomas. Arises from dilated blood vessels or localized vascular malformations, appearing bright red, purple, or dark violet.",
        "risk_notes": "Predominantly benign. Pyogenic granulomas may bleed easily upon minor trauma.",
        "abcde_assessment": "Exhibits distinct red, purple, or violaceous lacunae (blood-filled spaces) under dermoscopy without melanocytic pigment networks.",
        "recommendation": "Routine clinical observation. If a vascular lesion bleeds profusely, ulcerates, or changes rapidly, consult a physician for laser treatment or electrocautery."
    },
    "df": {
        "display_name": "Dermatofibroma",
        "code": "df",
        "category_type": "Benign Fibrohistiocytic Lesion",
        "urgency": "Low (Benign)",
        "urgency_badge": "bg-success",
        "is_benign": True,
        "description": "A common firm, solitary dermal nodule, typically located on lower legs of young to middle-aged adults. Displays the classic 'dimple sign' (pinching causes inward dimpling).",
        "risk_notes": "Completely benign. Believed to represent a reactive response to minor trauma, such as an insect bite or folliculitis.",
        "abcde_assessment": "Central white scar-like patch surrounded by a faint, delicate pigment network on dermoscopy.",
        "recommendation": "No treatment required. If painful or symptomatic, excision can be performed by a medical professional."
    }
}

