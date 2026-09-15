"""
Plant Disease Knowledge Base
Covers 38 PlantVillage classes (10 crops, 26 diseases + 12 healthy states)
"""

# ──────────────────────────────────────────────────────────────────────────────
# Class label list (PlantVillage 38-class mapping used by the AI model)
# ──────────────────────────────────────────────────────────────────────────────
CLASS_LABELS = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

# ──────────────────────────────────────────────────────────────────────────────
# Helper to parse class label
# ──────────────────────────────────────────────────────────────────────────────
def parse_class_label(label: str) -> tuple[str, str]:
    """Return (plant_name, disease_name) from a PlantVillage label."""
    parts = label.split("___", 1)
    plant = parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
    disease = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Unknown"
    if disease.lower() == "healthy":
        disease = "Healthy"
    return plant, disease


# ──────────────────────────────────────────────────────────────────────────────
# Full disease encyclopaedia
# ──────────────────────────────────────────────────────────────────────────────
DISEASE_KB: dict[str, dict] = {
    # ── APPLE ─────────────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "common_name": "Apple Scab",
        "scientific_name": "Venturia inaequalis",
        "type": "Fungal",
        "summary": "Apple scab is one of the most economically important diseases of apple worldwide, causing significant fruit and foliage damage.",
        "symptoms": [
            "Olive-green to brown velvety spots on leaves",
            "Lesions become dark, corky, and scabby on fruit",
            "Severe defoliation in wet seasons",
            "Cracking and deformation of fruit",
        ],
        "cause": "Fungus Venturia inaequalis overwinters in infected leaf litter; ascospores released in spring during wet weather.",
        "effects": "Reduces fruit quality and marketability; severe infections can cause premature defoliation and weaken trees.",
        "severity_factors": ["Wet spring weather", "Dense canopy", "Susceptible cultivars"],
        "prevention": [
            "Plant resistant varieties (Redfree, Liberty, Freedom)",
            "Rake and destroy fallen leaves",
            "Ensure good air circulation through pruning",
            "Apply dormant oil sprays",
        ],
        "immediate_actions": [
            "Remove and destroy infected leaves and fruit",
            "Begin fungicide programme at green tip growth stage",
            "Avoid overhead irrigation",
        ],
        "cultural_biological": [
            "Urea applications to leaf litter accelerate decomposition",
            "Trichoderma-based biocontrol agents can suppress overwintering inoculum",
            "Copper sprays at delayed dormant stage (organic option)",
        ],
        "references": ["Cornell University Extension", "RHS UK", "Penn State Extension"],
    },

    "Apple___Black_rot": {
        "common_name": "Apple Black Rot",
        "scientific_name": "Botryosphaeria obtusa",
        "type": "Fungal",
        "summary": "Black rot causes fruit rot, leaf spots (frogeye), and limb cankers on apple.",
        "symptoms": [
            "Frogeye leaf spots: purple-bordered, tan to brown centres",
            "Fruit rot starting as small purple specks, enlarging to black, mummified rot",
            "Bark cankers on limbs; reddish-brown sunken areas",
        ],
        "cause": "Fungus Botryosphaeria obtusa; spreads via rain splash from mummified fruit and cankered wood.",
        "effects": "Fruit becomes unmarketable; cankers girdle limbs causing dieback.",
        "severity_factors": ["Warm, humid weather", "Poor sanitation", "Injured bark"],
        "prevention": [
            "Remove mummified fruit from trees and ground",
            "Prune out cankered limbs during dry weather",
            "Avoid mechanical injury to bark",
        ],
        "immediate_actions": [
            "Prune infected limbs 15 cm below visible canker margin",
            "Apply fungicide cover sprays during petal fall to summer",
        ],
        "cultural_biological": [
            "Keep trees vigorous with balanced fertilisation",
            "Improve canopy air circulation",
        ],
        "references": ["University of Maine Extension", "MSU Extension"],
    },

    "Apple___Cedar_apple_rust": {
        "common_name": "Cedar–Apple Rust",
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "type": "Fungal (Rust)",
        "summary": "A fungal disease requiring two hosts (apple and eastern red cedar/juniper) to complete its life cycle.",
        "symptoms": [
            "Bright orange-yellow spots on upper leaf surfaces",
            "Spore tubes (aecia) on lower leaf surface",
            "Fruit and twig infections cause distortion",
        ],
        "cause": "Basidiomycete rust fungus alternating between Malus (apple) and Juniperus (cedar) hosts.",
        "effects": "Premature defoliation reduces photosynthesis and fruit set; repeated infections weaken trees.",
        "severity_factors": ["Nearby juniper/cedar trees", "Wet spring conditions", "Susceptible cultivars"],
        "prevention": [
            "Plant resistant apple cultivars",
            "Remove nearby ornamental junipers if possible",
            "Apply protective fungicide from tight cluster through cover sprays",
        ],
        "immediate_actions": [
            "Apply myclobutanil or mancozeb at first infection period",
            "Remove galls from cedar hosts in late winter",
        ],
        "cultural_biological": [
            "Sulfur-based fungicides (organic option)",
        ],
        "references": ["Virginia Cooperative Extension", "Cornell Fruit"],
    },

    "Apple___healthy": {
        "common_name": "Healthy Apple",
        "scientific_name": "Malus domestica",
        "type": "Healthy",
        "summary": "The plant appears healthy with no signs of disease.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": [
            "Continue regular monitoring",
            "Maintain balanced nutrition",
            "Practice good orchard sanitation",
        ],
        "immediate_actions": ["No immediate action required"],
        "cultural_biological": ["Regular pruning for air circulation and light penetration"],
        "references": [],
    },

    # ── CORN / MAIZE ──────────────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "common_name": "Gray Leaf Spot (Cercospora Leaf Spot)",
        "scientific_name": "Cercospora zeae-maydis",
        "type": "Fungal",
        "summary": "One of the most yield-limiting foliar diseases of maize globally, particularly severe in humid conditions.",
        "symptoms": [
            "Small, tan to brown rectangular lesions with yellow halos",
            "Lesions expand and turn gray with parallel sides bounded by leaf veins",
            "Premature senescence of lower leaves spreading upward",
        ],
        "cause": "Fungus Cercospora zeae-maydis; overwinters in infected crop residue; spread by wind and rain.",
        "effects": "Severe epidemics can reduce grain yield by 50% or more by destroying photosynthetic area.",
        "severity_factors": ["High humidity", "Minimum tillage", "Susceptible hybrids", "Continuous corn"],
        "prevention": [
            "Plant resistant/tolerant hybrids",
            "Rotate crops (soybean or small grains)",
            "Till crop residue to reduce inoculum",
            "Apply foliar fungicides at VT/R1 if canopy humidity is high",
        ],
        "immediate_actions": [
            "Scout fields weekly from V8 onwards",
            "Apply strobilurin + triazole fungicide if disease reaches upper canopy before silking",
        ],
        "cultural_biological": [
            "Biocontrol research ongoing; no commercially available biological fully established for GLS",
            "Promote canopy airflow by optimising plant populations",
        ],
        "references": ["University of Illinois Extension", "Purdue Extension", "CIMMYT"],
    },

    "Corn_(maize)___Common_rust_": {
        "common_name": "Common Rust of Corn",
        "scientific_name": "Puccinia sorghi",
        "type": "Fungal (Rust)",
        "summary": "Common rust is widespread on maize; economic losses in field corn are rare but sweet corn can be severely affected.",
        "symptoms": [
            "Cinnamon-brown, powdery pustules on both leaf surfaces",
            "Pustules later turn black (teliospores)",
            "Heavy infection yellows and kills leaves",
        ],
        "cause": "Obligate rust fungus Puccinia sorghi; alternate host is Oxalis spp.; urediospores spread by wind long distances.",
        "effects": "Severe epidemics on susceptible sweet corn can cause significant yield loss and stalk quality reduction.",
        "severity_factors": ["Cool nights (16–23 °C)", "Dew and high humidity", "Susceptible hybrid"],
        "prevention": [
            "Use rust-resistant hybrids (Rp genes)",
            "Avoid planting sweet corn near heavily infected fields",
        ],
        "immediate_actions": [
            "Apply triazole or strobilurin fungicide if infection appears before silking on susceptible hybrids",
        ],
        "cultural_biological": [
            "Biocontrol agents for rust not well established commercially",
        ],
        "references": ["Iowa State Extension", "University of Wisconsin Extension"],
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "common_name": "Northern Leaf Blight (NLB)",
        "scientific_name": "Exserohilum turcicum",
        "type": "Fungal",
        "summary": "NLB causes characteristic cigar-shaped lesions on maize leaves and is one of the most economically important maize diseases.",
        "symptoms": [
            "Long (2.5–15 cm), elliptical, gray-green to tan cigar-shaped lesions",
            "Lesions may coalesce, destroying large sections of leaf tissue",
            "Dark olive-gray sporulation visible on lesion surface",
        ],
        "cause": "Fungus Exserohilum turcicum; survives on crop debris; dispersed by wind and rain splash.",
        "effects": "Significant yield loss when infection occurs before or during grain fill; 30–50% losses reported in severe epidemics.",
        "severity_factors": ["Moderate temperatures (18–27 °C)", "High humidity", "Susceptible hybrids", "Continuous corn"],
        "prevention": [
            "Plant hybrids with NLB resistance (Ht genes or quantitative resistance)",
            "Crop rotation and residue management",
        ],
        "immediate_actions": [
            "Apply foliar fungicide (azoxystrobin, propiconazole) at VT/R1 when disease is present on the ear leaf or above",
        ],
        "cultural_biological": [
            "Trichoderma seed treatments may reduce early infections",
            "Deep tillage buries infected residue",
        ],
        "references": ["University of Nebraska-Lincoln Extension", "Iowa State University Plant & Insect Diagnostic Lab"],
    },

    "Corn_(maize)___healthy": {
        "common_name": "Healthy Corn (Maize)",
        "scientific_name": "Zea mays",
        "type": "Healthy",
        "summary": "The plant appears healthy. Continue regular monitoring.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Monitor weekly for early disease signs", "Maintain balanced soil fertility"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── GRAPE ─────────────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "common_name": "Grape Black Rot",
        "scientific_name": "Guignardia bidwellii",
        "type": "Fungal",
        "summary": "Black rot is the most destructive disease of cultivated grapes in eastern North America and other humid regions.",
        "symptoms": [
            "Reddish-brown circular leaf spots with dark borders",
            "White pycnidia visible in leaf lesions",
            "Berries shrivel and become hard black mummies",
        ],
        "cause": "Ascomycete fungus Guignardia bidwellii; overwinters in mummified berries and infected canes.",
        "effects": "Complete crop loss possible; mummified berries serve as inoculum source for multiple seasons.",
        "severity_factors": ["Warm, wet weather", "Dense canopy", "Nearby infected mummies"],
        "prevention": [
            "Remove all mummified berries before budbreak",
            "Prune for open canopy air circulation",
            "Begin fungicide programme at early shoot growth",
        ],
        "immediate_actions": [
            "Apply mancozeb or myclobutanil every 7–10 days during bloom",
            "Remove and destroy infected clusters",
        ],
        "cultural_biological": [
            "Copper-based fungicides (organic vineyards)",
            "Trichoderma harzianum shows some efficacy against Guignardia",
        ],
        "references": ["Penn State Extension", "Cornell Cooperative Extension", "USDA ARS"],
    },

    "Grape___Esca_(Black_Measles)": {
        "common_name": "Esca (Black Measles)",
        "scientific_name": "Phaeomoniella chlamydospora + Phaeoacremonium spp.",
        "type": "Fungal (Wood disease complex)",
        "summary": "Esca is a complex trunk disease caused by multiple wood-decaying fungi; it is one of the most damaging grapevine diseases worldwide.",
        "symptoms": [
            "Interveinal chlorosis and necrosis giving a 'tiger-stripe' pattern",
            "Small, dark spots on berries (measles symptom)",
            "Apoplexy: sudden wilting and death of entire shoot",
            "Internal wood shows dark streaking and decay",
        ],
        "cause": "Complex of fungi: Phaeomoniella chlamydospora, Phaeoacremonium spp., Fomitiporia mediterranea; enter via pruning wounds.",
        "effects": "Gradual decline and death of individual canes or whole vines; no cure once wood is extensively infected.",
        "severity_factors": ["Large pruning wounds", "Wet conditions after pruning", "Old vines"],
        "prevention": [
            "Prune during dry weather",
            "Apply wound sealants (Trichoderma products) immediately after pruning",
            "Avoid large pruning cuts",
        ],
        "immediate_actions": [
            "Remove and destroy severely infected wood",
            "Apply Trichoderma-based wound protectant to fresh cuts",
        ],
        "cultural_biological": [
            "Trichoderma harzianum-based products (e.g., Vinevax) are registered for wound protection in many countries",
        ],
        "references": ["INRAE France", "UC Davis Viticulture Extension"],
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "common_name": "Isariopsis Leaf Spot (Leaf Blight)",
        "scientific_name": "Pseudocercospora vitis (syn. Isariopsis clavispora)",
        "type": "Fungal",
        "summary": "A foliar disease causing irregular dark lesions that can lead to premature defoliation.",
        "symptoms": [
            "Irregular dark brown to black lesions on upper leaf surface",
            "Olive-gray sporulation on lower leaf surface",
            "Premature leaf drop in severe cases",
        ],
        "cause": "Fungus Pseudocercospora vitis; favoured by warm humid conditions.",
        "effects": "Premature defoliation reduces carbohydrate reserves; may affect fruit ripening.",
        "severity_factors": ["Warm temperatures", "High humidity", "Late-season infections"],
        "prevention": [
            "Maintain open canopy",
            "Avoid overhead irrigation",
        ],
        "immediate_actions": [
            "Apply copper or mancozeb-based fungicide",
            "Remove heavily infected leaves",
        ],
        "cultural_biological": ["Copper-based sprays"],
        "references": ["TNAU Agritech", "FAO Plant Disease Records"],
    },

    "Grape___healthy": {
        "common_name": "Healthy Grapevine",
        "scientific_name": "Vitis vinifera / V. labrusca",
        "type": "Healthy",
        "summary": "The vine appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Regular scouting", "Balanced nutrition", "Good canopy management"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── ORANGE ────────────────────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "common_name": "Huanglongbing (HLB) / Citrus Greening",
        "scientific_name": "Candidatus Liberibacter asiaticus",
        "type": "Bacterial (Phloem-limited)",
        "summary": "HLB is the most devastating citrus disease in the world; there is currently no cure for infected trees.",
        "symptoms": [
            "Asymmetric yellowing (blotchy mottle) of leaves, different from nutrient deficiency",
            "Small, lopsided, bitter fruit that fails to colour properly",
            "Aborted seeds; fruit remains green on one side",
            "Zinc-deficiency-like symptoms (interveinal chlorosis) on young shoots",
        ],
        "cause": "Phloem-limited bacterium Candidatus Liberibacter asiaticus (CLas); spread by the Asian citrus psyllid (Diaphorina citri).",
        "effects": "Progressive decline and death of trees within 5–8 years of infection; no commercial citrus variety is immune.",
        "severity_factors": ["Presence of psyllid vector", "Lack of quarantine enforcement", "Warm climate"],
        "prevention": [
            "Control Asian citrus psyllid (Diaphorina citri) with systemic insecticides",
            "Use certified disease-free nursery stock",
            "Remove and destroy infected trees promptly",
            "Strict quarantine of plant material",
        ],
        "immediate_actions": [
            "Report suspected HLB to local agricultural authority (mandatory in many jurisdictions)",
            "Do NOT move plant material from affected areas",
            "Begin intensive psyllid control on surrounding trees",
        ],
        "cultural_biological": [
            "Parasitic wasp Tamarixia radiata is an effective biological control for D. citri psyllid",
            "Nutritional management (micronutrient foliar sprays) can temporarily prolong tree productivity",
        ],
        "references": ["USDA APHIS", "University of Florida IFAS", "ICAR-Central Citrus Research Institute India"],
    },

    # ── PEACH ─────────────────────────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "common_name": "Bacterial Spot of Peach",
        "scientific_name": "Xanthomonas arboricola pv. pruni",
        "type": "Bacterial",
        "summary": "Bacterial spot is the most important bacterial disease of stone fruits in the eastern USA and other humid regions.",
        "symptoms": [
            "Small water-soaked lesions on leaves becoming angular purple-black spots",
            "Shot-hole appearance as lesion centres fall out",
            "Fruit develops sunken, water-soaked pits that become corky",
            "Twig cankers cause dieback",
        ],
        "cause": "Bacterium Xanthomonas arboricola pv. pruni; spread by rain splash and wind-driven rain.",
        "effects": "Defoliation, fruit quality loss, and increased susceptibility to secondary pathogens.",
        "severity_factors": ["Warm, rainy weather", "Susceptible varieties", "High wind"],
        "prevention": [
            "Plant resistant or tolerant varieties",
            "Apply copper-based bactericides at petal fall and during summer",
            "Avoid planting in sites exposed to prevailing winds",
        ],
        "immediate_actions": [
            "Apply copper hydroxide or oxytetracycline (where registered) during wet periods",
            "Remove severely infected twigs",
        ],
        "cultural_biological": [
            "Bacillus subtilis-based products show some suppression",
        ],
        "references": ["Clemson Extension", "NC State Extension"],
    },

    "Peach___healthy": {
        "common_name": "Healthy Peach",
        "scientific_name": "Prunus persica",
        "type": "Healthy",
        "summary": "The tree appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Regular monitoring", "Balanced fertilisation"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── PEPPER ────────────────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "common_name": "Bacterial Spot of Bell Pepper",
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "type": "Bacterial",
        "summary": "Bacterial spot is one of the most serious diseases of pepper and tomato in warm, humid, rainy conditions.",
        "symptoms": [
            "Water-soaked, circular to irregular spots on leaves",
            "Lesions turn brown with yellow halos; centres may fall out",
            "Raised, scabby lesions on fruit",
            "Severe defoliation exposes fruit to sunscald",
        ],
        "cause": "Bacterium Xanthomonas campestris pv. vesicatoria; seed-borne and soil-borne; spread by rain splash.",
        "effects": "Defoliation, reduced yields, and fruit quality degradation.",
        "severity_factors": ["Warm temperatures (24–30 °C)", "Rain and overhead irrigation", "Infected seed"],
        "prevention": [
            "Use certified disease-free or treated seed",
            "Rotate with non-solanaceous crops for 2–3 years",
            "Avoid overhead irrigation",
            "Use resistant cultivars where available",
        ],
        "immediate_actions": [
            "Apply copper-based bactericide + mancozeb mixture",
            "Remove heavily infected plant material",
        ],
        "cultural_biological": [
            "Bacillus subtilis (e.g., Serenade) registered as a biopesticide",
            "Compost teas with competitive microflora",
        ],
        "references": ["UF IFAS", "Cornell Cooperative Extension"],
    },

    "Pepper,_bell___healthy": {
        "common_name": "Healthy Bell Pepper",
        "scientific_name": "Capsicum annuum",
        "type": "Healthy",
        "summary": "Plant appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Monitor regularly", "Maintain soil health"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── POTATO ────────────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "common_name": "Early Blight of Potato",
        "scientific_name": "Alternaria solani",
        "type": "Fungal",
        "summary": "Early blight is a common foliage disease that typically affects older, senescing tissue but can cause serious defoliation.",
        "symptoms": [
            "Dark brown circular spots with concentric rings (bull's-eye pattern)",
            "Yellow halo surrounding lesions",
            "Lesions begin on lower, older leaves",
            "Stem lesions (collar rot) at soil level",
        ],
        "cause": "Fungus Alternaria solani; overwinters in infected plant debris; spreads via wind and rain.",
        "effects": "Premature defoliation reduces photosynthesis and tuber development; tuber quality may also be affected.",
        "severity_factors": ["Nutrient-stressed plants", "Warm days/cool nights", "Prolonged leaf wetness"],
        "prevention": [
            "Use certified disease-free seed potatoes",
            "Maintain balanced fertilisation (especially nitrogen)",
            "Rotate crops for 2–3 years",
            "Avoid wetting foliage with irrigation",
        ],
        "immediate_actions": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin fungicide",
            "Remove and destroy heavily infected foliage",
        ],
        "cultural_biological": [
            "Trichoderma viride seed treatment",
            "Bacillus subtilis foliar sprays",
        ],
        "references": ["University of Idaho Extension", "IARI New Delhi"],
    },

    "Potato___Late_blight": {
        "common_name": "Late Blight of Potato",
        "scientific_name": "Phytophthora infestans",
        "type": "Oomycete (Water mould)",
        "summary": "Late blight is the most destructive potato disease in the world; it caused the Great Irish Famine of the 1840s. Still causes billions in losses annually.",
        "symptoms": [
            "Water-soaked, irregular pale green lesions on leaves expanding rapidly",
            "White cottony sporulation on underside of leaves in humid conditions",
            "Lesions turn brown and necrotic; entire plant collapses in wet weather",
            "Brown, granular rot in tubers",
        ],
        "cause": "Oomycete Phytophthora infestans; spreads rapidly in cool, wet conditions; highly polycyclic.",
        "effects": "Complete crop destruction within days under favourable conditions.",
        "severity_factors": ["Temperatures 10–25 °C with night temperatures 10–15 °C", "Leaf wetness >10 hours", "High humidity"],
        "prevention": [
            "Use resistant varieties (e.g., Sarpo Mira, Defender)",
            "Use certified seed potatoes",
            "Scout fields regularly using disease forecasting models (BlightCast)",
            "Ensure good drainage",
        ],
        "immediate_actions": [
            "Apply metalaxyl-M + mancozeb (Ridomil Gold MZ) or cymoxanil + mancozeb immediately",
            "Do NOT compost infected material; destroy off-site",
            "Haulm kill if crop near maturity and infection is severe",
        ],
        "cultural_biological": [
            "Copper-based fungicides (organic standard)",
            "Bacillus subtilis (limited efficacy as standalone)",
        ],
        "references": ["International Potato Center (CIP)", "BASF AgriService", "Teagasc Ireland"],
    },

    "Potato___healthy": {
        "common_name": "Healthy Potato",
        "scientific_name": "Solanum tuberosum",
        "type": "Healthy",
        "summary": "Plant appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Monitor weekly", "Scout for aphids (PVY vector)"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── SQUASH ────────────────────────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "common_name": "Powdery Mildew of Squash / Cucurbits",
        "scientific_name": "Podosphaera xanthii (syn. Sphaerotheca fuliginea)",
        "type": "Fungal",
        "summary": "Powdery mildew is the most common and widely distributed foliar disease of cucurbits worldwide.",
        "symptoms": [
            "White to gray powdery fungal colonies on upper leaf surface",
            "Lesions expand to cover entire leaf surface",
            "Infected leaves yellow and die",
            "Distinctive white powder is easily rubbed off",
        ],
        "cause": "Obligate fungal parasite Podosphaera xanthii; spreads via airborne conidia; does NOT require free water.",
        "effects": "Premature defoliation reduces fruit size and quality; weakened plants susceptible to secondary infections.",
        "severity_factors": ["Dry weather with high humidity at night", "Dense planting", "Susceptible varieties"],
        "prevention": [
            "Plant resistant varieties",
            "Ensure adequate plant spacing",
            "Avoid excessive nitrogen",
        ],
        "immediate_actions": [
            "Apply sulfur, potassium bicarbonate, or myclobutanil fungicide",
            "Remove heavily infected leaves",
        ],
        "cultural_biological": [
            "Bacillus subtilis (Serenade) – effective biopesticide for powdery mildews",
            "Milk spray (40% dilution) has shown efficacy in trials",
            "Neem oil (azadirachtin)",
        ],
        "references": ["UC IPM", "Cornell Cooperative Extension"],
    },

    # ── STRAWBERRY ────────────────────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "common_name": "Strawberry Leaf Scorch",
        "scientific_name": "Diplocarpon earliana",
        "type": "Fungal",
        "summary": "Leaf scorch causes reddish-purple to brown irregular blotches on strawberry leaves.",
        "symptoms": [
            "Small, irregular purple to red spots on upper leaf surfaces",
            "Centres of spots remain purple (unlike leaf spot where centres turn white)",
            "Infected leaves appear scorched; severe infections cause leaf death",
        ],
        "cause": "Fungus Diplocarpon earliana; overwinters in infected leaves; spread by rain splash in spring.",
        "effects": "Severe defoliation weakens plants, reduces yield, and increases winter injury susceptibility.",
        "severity_factors": ["Wet, rainy springs", "Dense canopy", "Old planting beds"],
        "prevention": [
            "Plant resistant varieties",
            "Renovate plantings by mowing and removing old foliage after harvest",
            "Improve air circulation",
        ],
        "immediate_actions": [
            "Apply captan or myclobutanil fungicide",
            "Remove and destroy infected leaves",
        ],
        "cultural_biological": [
            "Copper hydroxide (organic option)",
        ],
        "references": ["Ohio State Extension", "NRAES Small Fruits Manual"],
    },

    "Strawberry___healthy": {
        "common_name": "Healthy Strawberry",
        "scientific_name": "Fragaria × ananassa",
        "type": "Healthy",
        "summary": "Plant appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Regular monitoring for spider mites and gray mould"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── TOMATO ────────────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "common_name": "Bacterial Spot of Tomato",
        "scientific_name": "Xanthomonas vesicatoria",
        "type": "Bacterial",
        "summary": "Bacterial spot is a serious disease of tomato in warm, humid, rainy regions.",
        "symptoms": [
            "Small, water-soaked circular spots with yellow halo on leaves",
            "Spots become brown/necrotic with ragged appearance",
            "Raised, dark, scab-like lesions on fruit",
            "Severe defoliation leaving fruit exposed to sunscald",
        ],
        "cause": "Seed-borne bacterium Xanthomonas vesicatoria; spread by rain, irrigation water, and handling.",
        "effects": "Defoliation, fruit quality loss, yield reduction, and increased sunscald damage.",
        "severity_factors": ["Warm temperatures", "Rain and overhead irrigation", "Infected transplants"],
        "prevention": [
            "Use certified clean seed",
            "Treat seed with hot water (52 °C for 30 minutes) before planting",
            "Use drip irrigation instead of overhead",
            "3–4 year crop rotation",
        ],
        "immediate_actions": [
            "Apply copper hydroxide + mancozeb tank mix",
            "Remove severely infected plant material",
        ],
        "cultural_biological": [
            "Bacillus subtilis (Serenade) as part of integrated management",
        ],
        "references": ["University of Florida IFAS", "Virginia Cooperative Extension"],
    },

    "Tomato___Early_blight": {
        "common_name": "Early Blight of Tomato",
        "scientific_name": "Alternaria solani",
        "type": "Fungal",
        "summary": "Early blight is one of the most common foliar diseases of tomato worldwide.",
        "symptoms": [
            "Dark brown spots with concentric rings (bull's-eye or target pattern)",
            "Yellow halo around lesions",
            "Lower leaves affected first",
            "Stem lesions near soil line (collar rot)",
        ],
        "cause": "Fungus Alternaria solani; survives in soil and plant debris; spread by wind and rain.",
        "effects": "Progressive defoliation from base upward reduces yield and fruit quality.",
        "severity_factors": ["High temperature and humidity", "Nutritional stress", "Dense plantings"],
        "prevention": [
            "Use disease-free transplants",
            "Stake plants and mulch soil surface",
            "Rotate crops 3–4 years",
            "Balanced fertilisation",
        ],
        "immediate_actions": [
            "Apply chlorothalonil, azoxystrobin, or difenoconazole",
            "Remove infected lower leaves",
        ],
        "cultural_biological": [
            "Trichoderma harzianum soil drench",
            "Bacillus subtilis foliar spray",
        ],
        "references": ["Cornell University", "UF IFAS Fact Sheet"],
    },

    "Tomato___Late_blight": {
        "common_name": "Late Blight of Tomato",
        "scientific_name": "Phytophthora infestans",
        "type": "Oomycete (Water mould)",
        "summary": "Late blight can devastate tomato crops within days under cool, wet conditions.",
        "symptoms": [
            "Large, irregular, water-soaked pale green to brown patches on leaves",
            "White downy sporulation on undersides in humid conditions",
            "Brown greasy fruit rot extending into flesh",
            "Dark lesions on stems causing rapid wilting",
        ],
        "cause": "Oomycete Phytophthora infestans; spreads rapidly via airborne sporangia in cool, wet weather.",
        "effects": "Complete crop loss within one to two weeks under epidemic conditions.",
        "severity_factors": ["Cool nights (10–15 °C)", "Leaf wetness > 10 hours", "Close spacing"],
        "prevention": [
            "Use certified disease-free transplants",
            "Resistant varieties (e.g., Mountain Merit, Defiant PhR)",
            "Stake and prune for air circulation",
            "Apply preventive fungicides in high-risk weather",
        ],
        "immediate_actions": [
            "Apply metalaxyl-M + chlorothalonil or copper-based fungicide immediately",
            "Remove and bag (do not compost) infected material",
        ],
        "cultural_biological": [
            "Copper-based sprays (organic certification compatible)",
        ],
        "references": ["Cornell Vegetable MD Online", "Royal Horticultural Society"],
    },

    "Tomato___Leaf_Mold": {
        "common_name": "Tomato Leaf Mould",
        "scientific_name": "Passalora fulva (syn. Cladosporium fulvum)",
        "type": "Fungal",
        "summary": "Leaf mould is primarily a greenhouse tomato problem; causes pale green to yellow spots on upper leaf surface.",
        "symptoms": [
            "Pale green to yellow spots on upper leaf surface",
            "Olive-green to brown velvety sporulation on lower leaf surface",
            "Infected leaves curl upward and eventually die",
        ],
        "cause": "Fungus Passalora fulva; spreads by air currents; favoured by high humidity (>85%).",
        "effects": "Severe infections cause defoliation and yield loss, especially in greenhouse production.",
        "severity_factors": ["High humidity", "Poor ventilation", "Susceptible cultivars"],
        "prevention": [
            "Plant resistant varieties (Cf resistance genes)",
            "Increase greenhouse ventilation",
            "Avoid overhead watering",
            "Reduce relative humidity to below 85%",
        ],
        "immediate_actions": [
            "Apply chlorothalonil or mancozeb",
            "Improve ventilation immediately",
        ],
        "cultural_biological": [
            "Bacillus subtilis",
            "Ampelomyces quisqualis (hyperparasite, limited availability)",
        ],
        "references": ["UC Davis Plant Pathology", "Horticulture Week UK"],
    },

    "Tomato___Septoria_leaf_spot": {
        "common_name": "Septoria Leaf Spot of Tomato",
        "scientific_name": "Septoria lycopersici",
        "type": "Fungal",
        "summary": "Septoria leaf spot is the most common foliar disease of tomatoes in the eastern USA and Canada.",
        "symptoms": [
            "Numerous small circular spots with dark brown borders and grey-white centres",
            "Tiny black pycnidia (fruiting bodies) visible in lesion centres with magnification",
            "Lower leaves affected first; disease progresses upward",
        ],
        "cause": "Fungus Septoria lycopersici; overwinters in infected debris; spread by rain and handling.",
        "effects": "Severe defoliation causes fruit sunscald and reduced yields.",
        "severity_factors": ["Warm temperatures (24–29 °C)", "Prolonged leaf wetness", "Dense planting"],
        "prevention": [
            "Crop rotation (2–3 years)",
            "Mulch around plants",
            "Stake plants for air circulation",
            "Remove lower leaves as a preventive measure",
        ],
        "immediate_actions": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin",
            "Remove and dispose of infected leaves",
        ],
        "cultural_biological": [
            "Copper-based fungicides",
            "Bacillus subtilis (biopesticide)",
        ],
        "references": ["Cornell Vegetable MD Online", "Penn State Extension"],
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "common_name": "Two-Spotted Spider Mite",
        "scientific_name": "Tetranychus urticae",
        "type": "Pest (Arachnid)",
        "summary": "Two-spotted spider mites are one of the most widespread agricultural pests, causing stippled yellowing and webbing.",
        "symptoms": [
            "Fine yellow stippling on upper leaf surface",
            "Fine silk webbing on underside of leaves",
            "Leaves turn bronze and dry out",
            "Tiny moving dots visible on underside with 10× magnification",
        ],
        "cause": "Herbivorous mite Tetranychus urticae; populations explode in hot, dry conditions; reproduces rapidly.",
        "effects": "Severe infestations cause defoliation, reduced photosynthesis, and yield loss; fruit quality affected.",
        "severity_factors": ["Hot, dry weather", "Pesticide resistance", "Broad-spectrum insecticide use (kills natural enemies)"],
        "prevention": [
            "Maintain adequate plant nutrition and irrigation (stressed plants are more susceptible)",
            "Conserve natural enemies (Phytoseiid predatory mites)",
            "Avoid unnecessary broad-spectrum insecticide use",
        ],
        "immediate_actions": [
            "Apply abamectin, bifenazate, or spiromesifen miticide",
            "Apply to underside of leaves where mites congregate",
            "Knock mites off plants with strong water spray",
        ],
        "cultural_biological": [
            "Phytoseiulus persimilis (predatory mite) – highly effective in greenhouse",
            "Neoseiulus californicus – effective in field and greenhouse",
            "Neem oil (azadirachtin) as repellent and growth disruptor",
        ],
        "references": ["UC IPM", "Cornell Cooperative Extension", "IOBC Biocontrol"],
    },

    "Tomato___Target_Spot": {
        "common_name": "Target Spot of Tomato",
        "scientific_name": "Corynespora cassiicola",
        "type": "Fungal",
        "summary": "Target spot is an increasingly important disease of tomato, especially in greenhouse and tropical production.",
        "symptoms": [
            "Brown, circular to irregular lesions with concentric rings (target pattern)",
            "Yellow halos around lesions",
            "Lesions on leaves, stems, and fruit",
        ],
        "cause": "Fungus Corynespora cassiicola; polyphagous; spreads by air and water splash.",
        "effects": "Defoliation reduces photosynthesis and exposes fruit to sunscald.",
        "severity_factors": ["Warm humid conditions", "Poor air circulation", "Dense canopy"],
        "prevention": [
            "Stake and prune tomatoes",
            "Use drip irrigation",
            "Rotate crops",
        ],
        "immediate_actions": [
            "Apply azoxystrobin, difenoconazole, or chlorothalonil",
        ],
        "cultural_biological": [
            "Bacillus subtilis",
        ],
        "references": ["UF IFAS", "AVRDC Taiwan"],
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "common_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "scientific_name": "Tomato yellow leaf curl virus (Begomovirus)",
        "type": "Viral",
        "summary": "TYLCV is one of the most devastating tomato viruses worldwide, transmitted exclusively by whiteflies.",
        "symptoms": [
            "Upward curling and yellowing of young leaves",
            "Stunted, bushy appearance with small cupped leaves",
            "Significant reduction in fruit set",
            "Plants infected early produce virtually no fruit",
        ],
        "cause": "Begomovirus transmitted by silverleaf whitefly (Bemisia tabaci); no cure once infected.",
        "effects": "Near-total crop loss if infection occurs in early plant stage.",
        "severity_factors": ["High whitefly populations", "Hot, dry conditions (favour whiteflies)", "Susceptible cultivars"],
        "prevention": [
            "Use TYLCV-resistant varieties (genes Ty-1 through Ty-6)",
            "Control whiteflies with yellow sticky traps, reflective mulches, and insecticides",
            "Use insect-proof screens in nurseries",
            "Remove infected plants immediately",
        ],
        "immediate_actions": [
            "Rogue out infected plants immediately",
            "Apply imidacloprid or thiamethoxam systemic insecticide to remaining healthy plants",
            "Install yellow sticky traps to monitor whitefly populations",
        ],
        "cultural_biological": [
            "Isaria fumosorosea – biopesticide for whitefly",
            "Beauveria bassiana – entomopathogenic fungus for whitefly control",
        ],
        "references": ["AVRDC", "FAO Whitefly-transmitted Viruses", "Cornell Vegetable MD"],
    },

    "Tomato___Tomato_mosaic_virus": {
        "common_name": "Tomato Mosaic Virus (ToMV)",
        "scientific_name": "Tomato mosaic virus (Tobamovirus)",
        "type": "Viral",
        "summary": "Tomato mosaic virus is mechanically transmitted and can persist for long periods on surfaces and tools.",
        "symptoms": [
            "Light and dark green mosaic mottling on leaves",
            "Leaf distortion (shoestring leaves in severe cases)",
            "Stunted growth",
            "Fruit may show internal browning or colour abnormalities",
        ],
        "cause": "Tobamovirus; transmitted mechanically through handling, tools, and infected seeds; not insect-transmitted.",
        "effects": "Reduced fruit quality and yield; no cure for infected plants.",
        "severity_factors": ["Contaminated tools", "Infected seed", "Smoker handling plants (tobacco mosaic virus cross-reacts)"],
        "prevention": [
            "Use certified virus-free seed or seed treated with 10% trisodium phosphate",
            "Disinfect tools with 10% bleach solution",
            "Wash hands before handling plants",
            "Remove and destroy infected plants",
        ],
        "immediate_actions": [
            "Remove infected plants immediately",
            "Disinfect all tools and work surfaces",
        ],
        "cultural_biological": [
            "No effective biocontrol available; prevention is key",
        ],
        "references": ["UC Davis Plant Pathology", "RHS"],
    },

    "Tomato___healthy": {
        "common_name": "Healthy Tomato",
        "scientific_name": "Solanum lycopersicum",
        "type": "Healthy",
        "summary": "Plant appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Regular monitoring", "Scout for pests and early disease"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── CHERRY ────────────────────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "common_name": "Cherry Powdery Mildew",
        "scientific_name": "Podosphaera clandestina",
        "type": "Fungal",
        "summary": "Powdery mildew is a common fungal disease of cherry causing white powdery growth on leaves and fruit.",
        "symptoms": [
            "White powdery growth on upper leaf surface",
            "Affected leaves curl and distort",
            "Fruit may show white powdery patches",
        ],
        "cause": "Obligate fungal parasite Podosphaera clandestina; does not require free water for infection.",
        "effects": "Defoliation, reduced fruit set; fruit cosmetic damage reduces marketability.",
        "severity_factors": ["High humidity at night", "Dry days", "Dense canopy"],
        "prevention": [
            "Plant resistant varieties",
            "Prune for open canopy",
            "Apply sulfur or myclobutanil at shoot growth",
        ],
        "immediate_actions": [
            "Apply potassium bicarbonate or sulfur dust/wettable sulfur",
        ],
        "cultural_biological": [
            "Bacillus subtilis (Serenade)",
            "Neem oil",
        ],
        "references": ["WSU Tree Fruit", "RHS Cherry Powdery Mildew"],
    },

    "Cherry_(including_sour)___healthy": {
        "common_name": "Healthy Cherry",
        "scientific_name": "Prunus avium / P. cerasus",
        "type": "Healthy",
        "summary": "Plant appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Regular monitoring"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── BLUEBERRY ─────────────────────────────────────────────────────────────
    "Blueberry___healthy": {
        "common_name": "Healthy Blueberry",
        "scientific_name": "Vaccinium corymbosum",
        "type": "Healthy",
        "summary": "Plant appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Monitor for mummy berry and Botrytis"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── RASPBERRY ─────────────────────────────────────────────────────────────
    "Raspberry___healthy": {
        "common_name": "Healthy Raspberry",
        "scientific_name": "Rubus idaeus",
        "type": "Healthy",
        "summary": "Plant appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Monitor for grey mould and cane blight"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },

    # ── SOYBEAN ───────────────────────────────────────────────────────────────
    "Soybean___healthy": {
        "common_name": "Healthy Soybean",
        "scientific_name": "Glycine max",
        "type": "Healthy",
        "summary": "Plant appears healthy.",
        "symptoms": [],
        "cause": "N/A",
        "effects": "N/A",
        "severity_factors": [],
        "prevention": ["Scout for sudden death syndrome, frogeye leaf spot, and SCN"],
        "immediate_actions": ["No action required"],
        "cultural_biological": [],
        "references": [],
    },
}


def get_disease_info(class_label: str) -> dict:
    """Return disease info dict for a class label, with fallback."""
    info = DISEASE_KB.get(class_label, {})
    if not info:
        plant, disease = parse_class_label(class_label)
        info = {
            "common_name": disease,
            "scientific_name": "Unknown",
            "type": "Unknown",
            "summary": f"Detailed information for {disease} on {plant} is not yet in the knowledge base.",
            "symptoms": [],
            "cause": "Unknown – consult a local agronomist.",
            "effects": "Unknown",
            "severity_factors": [],
            "prevention": [],
            "immediate_actions": [],
            "cultural_biological": [],
            "references": [],
        }
    return info
