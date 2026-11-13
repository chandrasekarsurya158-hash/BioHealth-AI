"""
Plant Pathology Knowledge Base
Contains botanical descriptions, symptoms, organic prevention methods,
and treatment protocols for all supported PlantVillage leaf classes.
"""

PLANT_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

PLANT_DISEASE_DETAILS = {
    "Apple___Apple_scab": {
        "display_name": "Apple Scab",
        "scientific_name": "Venturia inaequalis",
        "plant": "Apple",
        "is_healthy": False,
        "symptoms": "Olive-green to dull brown velvety spots on leaf surfaces. Lesions turn dark brown and crusty with age, causing premature leaf yellowing and drop.",
        "prevention": "Rake and destroy fallen leaves in autumn to reduce overwintering fungal spores. Prune canopy branches annually to improve airflow and rapid leaf drying.",
        "treatment": "Apply preventive copper-based fungicides or sulfur formulations during bud break and early bloom. In wet seasons, apply myclobutanil according to local agricultural extension schedules."
    },
    "Apple___Black_rot": {
        "display_name": "Apple Black Rot (Frogeye Leaf Spot)",
        "scientific_name": "Botryosphaeria obtusa",
        "plant": "Apple",
        "is_healthy": False,
        "symptoms": "Circular purple spots on foliage that enlarge into tan spots with purple margins (frogeye appearance). Causes fruit rot and limb cankers.",
        "prevention": "Prune out dead wood, cankered twigs, and mummified fruits from previous seasons. Burn or discard infected cuttings far away from the orchard.",
        "treatment": "Apply captan or thiophanate-methyl fungicides from silver tip stage through petal fall and summer cover sprays."
    },
    "Apple___Cedar_apple_rust": {
        "display_name": "Cedar Apple Rust",
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "plant": "Apple",
        "is_healthy": False,
        "symptoms": "Bright yellow-orange or reddish spots on the upper leaf surface. Raised tube-like fungal aecia develop on the undersides of leaves during late spring.",
        "prevention": "Remove eastern red cedar (Juniperus virginiana) trees within a 1-2 mile radius of the orchard where possible. Plant rust-resistant cultivars (e.g., Enterprise, Freedom).",
        "treatment": "Apply myclobutanil, fenbuconazole, or mancozeb fungicides as flower buds turn pink through post-bloom petal drop."
    },
    "Apple___healthy": {
        "display_name": "Healthy Apple Leaf",
        "scientific_name": "Malus domestica (Healthy)",
        "plant": "Apple",
        "is_healthy": True,
        "symptoms": "No visible signs of pathogen invasion. Leaves exhibit vibrant green pigmentation, smooth margins, and intact cellular structure.",
        "prevention": "Continue standard preventive orchard hygiene, balanced nitrogen fertilization, and clean drip irrigation.",
        "treatment": "No disease intervention required. Maintain seasonal scouting for early foliar irregularities."
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "display_name": "Corn Gray Leaf Spot",
        "scientific_name": "Cercospora zeae-maydis",
        "plant": "Corn (Maize)",
        "is_healthy": False,
        "symptoms": "Rectangular, pale brown to gray necrotic lesions running parallel between leaf veins. Blighting of large leaf areas during grain filling.",
        "prevention": "Practice 2-year crop rotation with non-host crops (soybeans, legumes). Incorporate or till crop residue to accelerate residue decomposition.",
        "treatment": "Apply strobilurin or triazole fungicides (such as azoxystrobin or propiconazole) if lesions reach the ear leaf prior to tasseling."
    },
    "Corn_(maize)___Common_rust_": {
        "display_name": "Corn Common Rust",
        "scientific_name": "Puccinia sorghi",
        "plant": "Corn (Maize)",
        "is_healthy": False,
        "symptoms": "Small, powdery, cinnamon-brown to dark red pustules on both upper and lower leaf surfaces. Severely infected leaves turn yellow and die prematurely.",
        "prevention": "Plant commercial hybrids carrying Rp resistance genes. Avoid late planting which increases exposure to wind-blown fungal spores from warmer regions.",
        "treatment": "Foliar fungicide application is warranted only when susceptible inbred lines or sweet corn show pustules on upper leaves prior to tasseling."
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "display_name": "Northern Corn Leaf Blight",
        "scientific_name": "Exserohilum turcicum",
        "plant": "Corn (Maize)",
        "is_healthy": False,
        "symptoms": "Long, elliptical, grayish-green to tan cigar-shaped lesions (1 to 6 inches long). In humid weather, lesions develop dark olive fungal fuzz.",
        "prevention": "Select resistant hybrids (Ht genes). Rotate crops away from corn for at least 1-2 years to deplete infected surface residue.",
        "treatment": "Apply labeled fungicides (pyraclostrobin + metconazole) at VT to R1 growth stages if weather conditions remain cool and wet."
    },
    "Corn_(maize)___healthy": {
        "display_name": "Healthy Corn Foliage",
        "scientific_name": "Zea mays (Healthy)",
        "plant": "Corn (Maize)",
        "is_healthy": True,
        "symptoms": "Foliage exhibits uniform deep green color with clear vascular striping and no pustules or blighting.",
        "prevention": "Ensure balanced soil nitrogen, phosphorus, and potassium levels; maintain adequate soil drainage.",
        "treatment": "No chemical or biological treatment needed."
    },
    "Potato___Early_blight": {
        "display_name": "Potato Early Blight",
        "scientific_name": "Alternaria solani",
        "plant": "Potato",
        "is_healthy": False,
        "symptoms": "Small brown spots that enlarge into characteristic target-like concentric rings on older bottom leaves. Leaf tissue around lesions often turns chlorotic yellow.",
        "prevention": "Avoid overhead sprinkler irrigation; water at the base of plants. Plant certified pathogen-free seed tubers. Rotate out of Solanaceae crops for 3 years.",
        "treatment": "Apply chlorothalonil, mancozeb, or azoxystrobin fungicides at the first sign of lower leaf spotting."
    },
    "Potato___Late_blight": {
        "display_name": "Potato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "plant": "Potato",
        "is_healthy": False,
        "symptoms": "Water-soaked irregular pale to dark green lesions on leaves that rapidly turn purplish-black. Delicate white mold appears on the underside of leaves during damp conditions.",
        "prevention": "Destroy all volunteer potato plants and cull piles. Eliminate infected vines prior to tuber harvest. Ensure adequate hill coverage with soil.",
        "treatment": "Immediately apply systemic fungicides such as metalaxyl, cymoxanil, or mandipropamid. In severe infestations, destroy top foliage to protect underground tubers."
    },
    "Potato___healthy": {
        "display_name": "Healthy Potato Foliage",
        "scientific_name": "Solanum tuberosum (Healthy)",
        "plant": "Potato",
        "is_healthy": True,
        "symptoms": "Vigorous, dark green composite leaves free of necrotic halos, spots, or water-soaked borders.",
        "prevention": "Ensure hilling around stems, proper irrigation timing, and regular scouting.",
        "treatment": "No fungicide intervention needed."
    },
    "Tomato___Bacterial_spot": {
        "display_name": "Tomato Bacterial Spot",
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "plant": "Tomato",
        "is_healthy": False,
        "symptoms": "Small, dark, water-soaked circular spots (under 3mm) that turn greasy brown with yellow halos. Leaves may drop prematurely, exposing fruit to sunscald.",
        "prevention": "Use certified disease-free seed and transplants. Avoid working in tomato fields when leaves are wet to prevent mechanical transmission of bacteria.",
        "treatment": "Spray fixed copper bactericide mixed with mancozeb to reduce bacterial load. Biological sprays with Bacillus subtilis can suppress early bacterial spread."
    },
    "Tomato___Early_blight": {
        "display_name": "Tomato Early Blight",
        "scientific_name": "Alternaria solani",
        "plant": "Tomato",
        "is_healthy": False,
        "symptoms": "Concentric target-board rings on older foliage starting from the base of the plant. Causes severe lower defoliation, stem cankers, and collar rot.",
        "prevention": "Stake and cage plants to elevate foliage off wet soil. Mulch heavily around bases. Strip lower 12 inches of foliage as plants mature to reduce soil splash.",
        "treatment": "Spray protective copper fungicide, chlorothalonil, or bio-fungicide (Trichoderma harzianum) at 7-10 day intervals during humid weather."
    },
    "Tomato___Late_blight": {
        "display_name": "Tomato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "plant": "Tomato",
        "is_healthy": False,
        "symptoms": "Large, oily-looking olive-green to black lesions on leaves and stems. White cottony downy growth on the underside of foliage during humid mornings.",
        "prevention": "Space tomato plants widely to maximize air penetration. Avoid planting potatoes near tomatoes. Water exclusively at ground level.",
        "treatment": "Apply preventive copper hydroxide or systemic chlorothalonil/fenamidone. Pull out and discard severely blighted plants in sealed trash bags."
    },
    "Tomato___Leaf_Mold": {
        "display_name": "Tomato Leaf Mold",
        "scientific_name": "Passalora fulva",
        "plant": "Tomato",
        "is_healthy": False,
        "symptoms": "Pale greenish-yellow indistinct spots on the upper leaf surface with velvety olive-green to brown fungal growth directly beneath on the lower leaf surface.",
        "prevention": "Common in greenhouses and high tunnels. Maintain relative humidity below 85% by opening greenhouse vents and using exhaust fans.",
        "treatment": "Apply copper octanoate or captan upon first identification of lower leaf discoloration."
    },
    "Tomato___Septoria_leaf_spot": {
        "display_name": "Tomato Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "plant": "Tomato",
        "is_healthy": False,
        "symptoms": "Numerous circular spots (1-3mm) with dark brown borders and distinctly gray or tan centers speckled with tiny black pycnidia fruiting bodies.",
        "prevention": "Keep foliage dry; utilize drip tape rather than overhead sprinklers. Control solanaceous weeds (nightshade, horsenettle) around crop borders.",
        "treatment": "Apply mancozeb, copper sulfate, or chlorothalonil starting at first cluster set and repeating following rainfall events."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "display_name": "Tomato Two-Spotted Spider Mite",
        "scientific_name": "Tetranychus urticae",
        "plant": "Tomato",
        "is_healthy": False,
        "symptoms": "Fine yellow or bronze stippling / speckling across the upper leaf surface. Silken webbing visible on leaf undersides; leaves eventually turn brown and desiccate.",
        "prevention": "Wash plants with periodic water sprays to dislodge dust and mites. Maintain adequate soil moisture to minimize plant drought stress.",
        "treatment": "Introduce predatory mites (Phytoseiulus persimilis). Apply insecticidal soap, neem oil, or horticultural oils covering the entire underside of leaves."
    },
    "Tomato___Target_Spot": {
        "display_name": "Tomato Target Spot",
        "scientific_name": "Corynespora cassiicola",
        "plant": "Tomato",
        "is_healthy": False,
        "symptoms": "Small, pinpoint water-soaked lesions that enlarge into circular brown lesions with faint concentric rings and light brown centers. Causes extensive blossom and leaf drop.",
        "prevention": "Prune suckers and lower leaf canopy to allow light and breeze penetration. Rotate with non-susceptible crops.",
        "treatment": "Apply strobilurin or carboxamide fungicides according to university extension guidelines."
    },
    "Tomato___Tomato_mosaic_virus": {
        "display_name": "Tomato Mosaic Virus (ToMV)",
        "scientific_name": "Tomato Mosaic Tobamovirus",
        "plant": "Tomato",
        "is_healthy": False,
        "symptoms": "Mottled light and dark green mosaic patterns on foliage. Leaves may appear distorted, fern-like ('shoestring' effect), with stunted plant growth.",
        "prevention": "Disinfect tools in 10% bleach solution between plants. Tobacco users must wash hands with soap before touching plants (transmitted mechanically).",
        "treatment": "There is no chemical cure for viral infections. Immediately rogue (uproot and bag) infected plants to prevent transmission to neighboring crops."
    },
    "Tomato___healthy": {
        "display_name": "Healthy Tomato Leaf",
        "scientific_name": "Solanum lycopersicum (Healthy)",
        "plant": "Tomato",
        "is_healthy": True,
        "symptoms": "Leaves exhibit healthy green color, defined serrations, firm turgor pressure, and zero necrotic or chlorotic spotting.",
        "prevention": "Maintain consistent deep watering, adequate calcium in soil to prevent blossom end rot, and seasonal mulching.",
        "treatment": "No disease intervention required."
    }
}

