"""
Staple Crop Pathology Knowledge Base (Module 2)
Dedicated to major staple cereal crops: Rice, Wheat, and Maize.
Distinct from general horticultural plant models.
"""

CROP_CLASSES = [
    # Rice Classes
    "Rice_Bacterial_leaf_blight",
    "Rice_Brown_spot",
    "Rice_Leaf_blast",
    "Rice_healthy",
    # Wheat Classes
    "Wheat_Brown_rust",
    "Wheat_Yellow_rust",
    "Wheat_Septoria",
    "Wheat_healthy",
    # Maize Classes
    "Maize_Cercospora_leaf_spot",
    "Maize_Common_rust",
    "Maize_Northern_Leaf_Blight",
    "Maize_healthy"
]

CROP_DISEASE_DETAILS = {
    # ------------------ Rice ------------------
    "Rice_Bacterial_leaf_blight": {
        "display_name": "Rice Bacterial Leaf Blight",
        "crop_type": "rice",
        "scientific_name": "Xanthomonas oryzae pv. oryzae",
        "is_healthy": False,
        "symptoms": "Water-soaked stripes starting from leaf tips that turn yellowish-white with wavy margins. Entire leaf desiccates into a bleached straw-white appearance.",
        "prevention": "Ensure balanced nitrogen application (excess nitrogen exacerbates blight). Drain floodwaters temporarily during early disease onset. Grow tolerant cultivars (e.g., IR64, Improved Samba Mahsuri).",
        "treatment": "Apply copper hydroxide or validamycin combined with streptocycline during early tillering. Avoid clipping seedling tips during transplanting."
    },
    "Rice_Brown_spot": {
        "display_name": "Rice Brown Spot",
        "crop_type": "rice",
        "scientific_name": "Bipolaris oryzae (Cochliobolus miyabeanus)",
        "is_healthy": False,
        "symptoms": "Small, circular to oval dark brown spots with yellowish-gray halos. Often indicative of soil nutrient deficiencies (silicon, potassium) and drought stress.",
        "prevention": "Treat seeds with hot water or fungicide prior to sowing. Apply balanced potassium and zinc fertilizers. Maintain adequate standing water depth in paddies.",
        "treatment": "Foliar spray of tricyclazole, edifenphos, or mancozeb at the boot-leaf to panicle emergence stage."
    },
    "Rice_Leaf_blast": {
        "display_name": "Rice Blast (Leaf & Neck Blast)",
        "crop_type": "rice",
        "scientific_name": "Magnaporthe oryzae",
        "is_healthy": False,
        "symptoms": "Spindle-shaped (diamond-shaped) lesions with pointed ends, gray/white centers, and dark brown or reddish borders. Rapidly coalesces to destroy the entire canopy.",
        "prevention": "Avoid late-season excessive nitrogen top-dressing. Plant blast-resistant varieties. Eliminate barnyard grass and host weeds on paddy bunds.",
        "treatment": "Spray systemic fungicides like tricyclazole (75% WP), isoprothiolane, or kasugamycin at the first appearance of leaf lesions."
    },
    "Rice_healthy": {
        "display_name": "Healthy Rice Crop",
        "crop_type": "rice",
        "scientific_name": "Oryza sativa (Healthy)",
        "is_healthy": True,
        "symptoms": "Upright, vibrant green tillers with uniform chlorophyl distribution and unblemished vegetative leaf blades.",
        "prevention": "Maintain scheduled alternate wetting and drying (AWD) water management and standard N-P-K nutrient schedules.",
        "treatment": "No disease intervention required."
    },

    # ------------------ Wheat ------------------
    "Wheat_Brown_rust": {
        "display_name": "Wheat Brown Rust (Leaf Rust)",
        "crop_type": "wheat",
        "scientific_name": "Puccinia triticina",
        "is_healthy": False,
        "symptoms": "Small, scattered, circular orange-brown pustules predominantly on the upper leaf surface. Pustules rupture the epidermis to release powdery urediniospores.",
        "prevention": "Eradicate alternate hosts (Thalictrum). Sow recommended rust-resistant varieties with slow-rusting genes. Practice synchronized regional sowing.",
        "treatment": "Apply propiconazole (25% EC), tebuconazole, or mancozeb at 500-750 ml/ha when 1-5% of upper foliage exhibits rust pustules."
    },
    "Wheat_Yellow_rust": {
        "display_name": "Wheat Yellow Rust (Stripe Rust)",
        "crop_type": "wheat",
        "scientific_name": "Puccinia striiformis",
        "is_healthy": False,
        "symptoms": "Bright yellow pustules arranged in narrow, parallel stripes or rows along the leaf veins. Highly damaging in cool, humid climates.",
        "prevention": "Plant resistant cultivars adapted to cooler agro-climatic zones. Avoid dense planting that restricts morning canopy drying.",
        "treatment": "Immediate spraying with propiconazole or azoxystrobin upon detection of the first yellow foci/patches in the field."
    },
    "Wheat_Septoria": {
        "display_name": "Wheat Septoria Tritici Blotch",
        "crop_type": "wheat",
        "scientific_name": "Zymoseptoria tritici",
        "is_healthy": False,
        "symptoms": "Irregular necrotic brown lesions sprinkled with tiny, black specks (pycnidia fruiting bodies) embedded within dead tissue.",
        "prevention": "Rotate with broadleaf crops (canola, pulses). Deeply plow or bury wheat stubble to accelerate residue decomposition.",
        "treatment": "Apply prothioconazole, epoxiconazole, or fluxapyroxad between flag leaf emergence and flowering (GS 39-59)."
    },
    "Wheat_healthy": {
        "display_name": "Healthy Wheat Crop",
        "crop_type": "wheat",
        "scientific_name": "Triticum aestivum (Healthy)",
        "is_healthy": True,
        "symptoms": "Sturdy green culms and clean flag leaves with zero pustules, stripes, or pycnidial blotches.",
        "prevention": "Ensure optimal seed drill depth and balanced basal fertilization.",
        "treatment": "No fungicide intervention needed."
    },

    # ------------------ Maize ------------------
    "Maize_Cercospora_leaf_spot": {
        "display_name": "Maize Gray Leaf Spot",
        "crop_type": "maize",
        "scientific_name": "Cercospora zeae-maydis",
        "is_healthy": False,
        "symptoms": "Rectangular, tan to gray lesions with distinct parallel margins bounded by leaf veins. Severe blighting impairs photosynthetic grain fill.",
        "prevention": "Crop rotation with non-host legumes for 1-2 seasons. Manage surface residue through conservation tillage where appropriate.",
        "treatment": "Apply strobilurin or triazole fungicides (e.g. pyraclostrobin) if disease reaches the third leaf below the ear prior to pollination."
    },
    "Maize_Common_rust": {
        "display_name": "Maize Common Rust",
        "crop_type": "maize",
        "scientific_name": "Puccinia sorghi",
        "is_healthy": False,
        "symptoms": "Oval to elongate powdery cinnamon-brown pustules scattered across both leaf surfaces. Foliage becomes chlorotic and desiccates under heavy infection.",
        "prevention": "Utilize hybrid seed carrying Rp-resistance traits. Avoid late planting which coincides with peak spore flights.",
        "treatment": "Fungicide application (azoxystrobin + propiconazole) is recommended on susceptible inbred lines if symptoms appear before tasseling."
    },
    "Maize_Northern_Leaf_Blight": {
        "display_name": "Maize Northern Corn Leaf Blight",
        "crop_type": "maize",
        "scientific_name": "Exserohilum turcicum",
        "is_healthy": False,
        "symptoms": "Large, elongated, cigar-shaped grayish-green lesions (2.5 to 15 cm long). Lesions turn tan with dark olive fungal sporulation in damp weather.",
        "prevention": "Select resistant hybrids (Ht genes). Rotate fields away from corn. Ensure proper row spacing for light penetration.",
        "treatment": "Apply systemic fungicides (e.g., fluxapyroxad + pyraclostrobin) when weather forecasts predict extended cool, rainy periods during silking."
    },
    "Maize_healthy": {
        "display_name": "Healthy Maize Crop",
        "crop_type": "maize",
        "scientific_name": "Zea mays (Healthy)",
        "is_healthy": True,
        "symptoms": "Broad, vibrant green leaves with sturdy midribs and no chlorotic striping or necrotic lesioning.",
        "prevention": "Maintain soil aeration, weed control, and balanced nitrogen side-dressing.",
        "treatment": "No disease intervention needed."
    }
}

