"""
Treatment & Pesticide Guide
All information sourced from published product labels, university extension,
and official agricultural authorities.
DISCLAIMER: Always consult the current registered product label in your country
before applying any pesticide. Regulations, registrations, and dosages vary
by region and change over time. The information here is for educational purposes.
"""

TREATMENT_DB: dict[str, list[dict]] = {
    # ── APPLE ─────────────────────────────────────────────────────────────────
    "Apple___Apple_scab": [
        {
            "active_ingredient": "Myclobutanil",
            "product_example": "Rally 40WSP (Dow AgroSciences)",
            "use_for": "Preventive and curative control of apple scab (Venturia inaequalis)",
            "rate": "75–113 g/ha (field); follow label for specific concentration",
            "preparation": "Mix in water according to label; ensure thorough coverage",
            "when_to_apply": "At green tip (first application) through cover sprays during primary scab season",
            "frequency": "Every 7–10 days during wet, high-risk periods; extend interval in dry weather",
            "phi": "14 days (pre-harvest interval; verify current registered label)",
            "safety": [
                "Wear chemical-resistant gloves and eye protection",
                "Avoid spray drift to water bodies",
                "Do NOT mix with emulsifiable concentrate oils",
            ],
            "source": "Dow AgroSciences product label; Cornell Fruit IPM",
        },
        {
            "active_ingredient": "Mancozeb",
            "product_example": "Dithane M-45 (Corteva)",
            "use_for": "Protectant fungicide for apple scab prevention",
            "rate": "1.5–2.0 kg/ha; follow label",
            "preparation": "Mix with water; add spreader-sticker if recommended by label",
            "when_to_apply": "Green tip through first cover; preventive only (no curative activity)",
            "frequency": "Every 5–7 days during primary scab season",
            "phi": "77 days (verify current label)",
            "safety": [
                "Wear full PPE including respirator",
                "MANCOZEB is a probable human carcinogen (IARC Group 2B) at high doses",
                "Avoid application near waterways",
            ],
            "source": "Corteva label; PMRA Canada",
        },
    ],

    "Apple___Black_rot": [
        {
            "active_ingredient": "Thiophanate-methyl",
            "product_example": "Topsin M 70WP (UPI)",
            "use_for": "Control of black rot and frogeye leaf spot on apple",
            "rate": "420–630 g/ha",
            "preparation": "Mix in water; tank-mix compatible with most fungicides",
            "when_to_apply": "Petal fall through late summer cover sprays",
            "frequency": "Every 10–14 days",
            "phi": "1 day (verify current label)",
            "safety": ["Wear gloves and eye protection", "Avoid skin and eye contact"],
            "source": "UPI product label",
        },
    ],

    "Apple___Cedar_apple_rust": [
        {
            "active_ingredient": "Myclobutanil",
            "product_example": "Rally 40WSP",
            "use_for": "Cedar-apple rust prevention on apple",
            "rate": "75–113 g/ha",
            "preparation": "Mix per label; thorough coverage essential",
            "when_to_apply": "Tight cluster through first cover; apply during infection periods (spore release from galls)",
            "frequency": "Every 7–10 days during infection periods",
            "phi": "14 days",
            "safety": ["Standard PPE; avoid spray drift"],
            "source": "Cornell Fruit IPM; Dow label",
        },
    ],

    # ── CORN ──────────────────────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": [
        {
            "active_ingredient": "Azoxystrobin + Propiconazole",
            "product_example": "Quilt Xcel (Syngenta)",
            "use_for": "Gray leaf spot and other foliar diseases of corn",
            "rate": "0.75–1.0 L/ha",
            "preparation": "Mix with water; spray with good canopy penetration",
            "when_to_apply": "VT (tassel) to R1 (silking) stage, or when disease threshold is reached",
            "frequency": "Single application usually sufficient; second application if pressure is very high",
            "phi": "30 days",
            "safety": [
                "Wear full PPE",
                "Avoid application in high wind",
                "Strobilurin fungicides – manage resistance with alternation",
            ],
            "source": "Syngenta Quilt Xcel label; Purdue Extension",
        },
    ],

    "Corn_(maize)___Common_rust_": [
        {
            "active_ingredient": "Propiconazole",
            "product_example": "Tilt 250EC (Syngenta)",
            "use_for": "Common rust of corn/maize",
            "rate": "0.5 L/ha",
            "preparation": "Mix in water; apply with boom sprayer for good canopy coverage",
            "when_to_apply": "At first sign of rust; most effective before V8 stage on susceptible sweet corn",
            "frequency": "Once; repeat in 14 days if disease progresses",
            "phi": "30 days",
            "safety": ["Wear PPE", "Avoid off-target drift"],
            "source": "Syngenta Tilt label; Iowa State Extension",
        },
    ],

    "Corn_(maize)___Northern_Leaf_Blight": [
        {
            "active_ingredient": "Azoxystrobin",
            "product_example": "Amistar (Syngenta)",
            "use_for": "Northern Leaf Blight and grey leaf spot of maize",
            "rate": "0.75–1.0 L/ha",
            "preparation": "Mix per label; good canopy penetration is essential",
            "when_to_apply": "VT to R2 stage when disease present on ear leaf or above",
            "frequency": "1–2 applications; 14 days apart if needed",
            "phi": "14 days",
            "safety": ["Full PPE; alternate fungicide classes for resistance management"],
            "source": "Syngenta label; Nebraska Extension",
        },
    ],

    # ── GRAPE ─────────────────────────────────────────────────────────────────
    "Grape___Black_rot": [
        {
            "active_ingredient": "Myclobutanil",
            "product_example": "Rally 40WSP",
            "use_for": "Black rot (Guignardia bidwellii) control on grapevine",
            "rate": "75–113 g/ha",
            "preparation": "Mix per label; thorough coverage of fruit and foliage required",
            "when_to_apply": "Early shoot growth (2–5 cm) through pea-size berry; most critical period is bloom ± 3 weeks",
            "frequency": "Every 7–10 days during high-risk period",
            "phi": "14 days",
            "safety": ["Wear PPE", "Avoid use within 30 m of water bodies"],
            "source": "Cornell Cooperative Extension; Dow label",
        },
        {
            "active_ingredient": "Mancozeb",
            "product_example": "Penncozeb 75 DF",
            "use_for": "Protectant fungicide for black rot and downy mildew of grape",
            "rate": "2.0–3.0 kg/ha",
            "preparation": "Mix with water; add spreader for improved coverage",
            "when_to_apply": "Preventive sprays from shoot emergence through bunch closure",
            "frequency": "Every 7 days in wet conditions",
            "phi": "66 days",
            "safety": ["Full PPE including respirator; avoid waterways"],
            "source": "Penn State Extension; product label",
        },
    ],

    "Grape___Esca_(Black_Measles)": [
        {
            "active_ingredient": "Trichoderma harzianum (biological)",
            "product_example": "Trichodex / Vinevax (where registered)",
            "use_for": "Wound protection against Esca-associated fungi after pruning",
            "rate": "As per label (typically 1–5% suspension)",
            "preparation": "Mix in water and apply to freshly cut pruning wounds by brush or spray immediately after pruning",
            "when_to_apply": "Immediately after each pruning cut, before wounds dry",
            "frequency": "Every pruning season",
            "phi": "N/A – biological agent, no withholding period",
            "safety": ["Wear gloves; non-toxic to humans and environment at registered rates"],
            "source": "INRAE; BioStart NZ; University of California Cooperative Extension",
        },
        {
            "active_ingredient": "Flusilazole (chemical option – limited registration)",
            "product_example": "Punch EW (BASF) – CHECK LOCAL REGISTRATION",
            "use_for": "Suppression of Esca-associated wood pathogens (registration varies by country)",
            "rate": "Consult current registered label in your country",
            "preparation": "Apply as trunk injection or wound sealant where registered",
            "when_to_apply": "At pruning",
            "frequency": "Annual",
            "phi": "Consult label",
            "safety": [
                "IMPORTANT: Verify current registration status in your country before use",
                "Do NOT use if not registered for this purpose in your jurisdiction",
            ],
            "source": "Consult your national plant protection authority",
        },
    ],

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": [
        {
            "active_ingredient": "Copper hydroxide",
            "product_example": "Kocide 3000 (FMC)",
            "use_for": "Isariopsis leaf spot and other fungal/bacterial diseases of grape",
            "rate": "0.75–1.5 kg/ha",
            "preparation": "Mix per label; add spreader-sticker for improved retention",
            "when_to_apply": "Preventive; begin at early season and continue through growing season",
            "frequency": "Every 10–14 days",
            "phi": "0 days",
            "safety": ["Wear PPE", "Avoid phytotoxicity – do NOT apply in hot weather or on wet foliage"],
            "source": "FMC label",
        },
    ],

    # ── ORANGE / CITRUS ───────────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": [
        {
            "active_ingredient": "Imidacloprid (for psyllid vector control)",
            "product_example": "Confidor 200 SL (Bayer)",
            "use_for": "Control of Asian citrus psyllid (Diaphorina citri), the insect vector of HLB",
            "rate": "0.5–1.0 mL/L water for foliar spray; follow label for soil drench rates",
            "preparation": "Dilute in water; apply to all plant parts including new flush",
            "when_to_apply": "When new flush appears (psyllids prefer to lay eggs on new growth); treat every flush cycle",
            "frequency": "Every 4–6 weeks during active growth",
            "phi": "7 days",
            "safety": [
                "HIGHLY TOXIC to bees – do NOT apply to flowering trees",
                "Wear PPE",
                "Note: neonicotinoids are restricted or banned in some jurisdictions; verify local regulations",
            ],
            "source": "Bayer CropScience label; UF IFAS HLB Management Guide",
        },
        {
            "active_ingredient": "Doxycycline (thermotherapy / experimental only)",
            "product_example": "Experimental – NOT commercially registered for HLB as of 2024",
            "use_for": "Experimental suppression of HLB bacterial titer in trees",
            "rate": "Research protocols only",
            "preparation": "Trunk injection in research settings",
            "when_to_apply": "Research only",
            "frequency": "Research only",
            "phi": "Not established",
            "safety": [
                "NOT a registered treatment for HLB",
                "Do NOT use without proper regulatory authorisation",
            ],
            "source": "USDA ARS Research; FDA Exemption Notices",
        },
    ],

    # ── PEACH ─────────────────────────────────────────────────────────────────
    "Peach___Bacterial_spot": [
        {
            "active_ingredient": "Copper hydroxide",
            "product_example": "Kocide 3000 (FMC)",
            "use_for": "Bacterial spot of peach and nectarine",
            "rate": "0.75–1.5 kg/ha",
            "preparation": "Mix per label",
            "when_to_apply": "Dormant through petal fall; summer applications during wet periods",
            "frequency": "Every 7–14 days during wet conditions",
            "phi": "0 days",
            "safety": ["Wear PPE; avoid phytotoxicity on young foliage"],
            "source": "Clemson Extension; FMC label",
        },
        {
            "active_ingredient": "Oxytetracycline",
            "product_example": "Mycoshield (where registered)",
            "use_for": "Bacterial spot – antibiotic option where registered",
            "rate": "As per current registered label",
            "preparation": "Mix in water per label",
            "when_to_apply": "At petal fall; during extended wet periods in summer",
            "frequency": "Every 7–14 days",
            "phi": "Consult label",
            "safety": [
                "Antibiotic resistance concerns – use in rotation with copper",
                "NOT registered in all countries; verify local status",
            ],
            "source": "NC State Extension; product label",
        },
    ],

    # ── PEPPER ────────────────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": [
        {
            "active_ingredient": "Copper hydroxide + Mancozeb",
            "product_example": "Kocide 3000 + Penncozeb (tank mix)",
            "use_for": "Bacterial spot of pepper (Xanthomonas campestris pv. vesicatoria)",
            "rate": "Copper: 0.75–1.5 kg/ha + Mancozeb: 1.5–2.0 kg/ha",
            "preparation": "Mix separately then combine; ensure compatibility before mixing",
            "when_to_apply": "Preventive; begin at transplanting or first symptom",
            "frequency": "Every 5–7 days in wet conditions",
            "phi": "Copper: 0 days; Mancozeb: 5 days",
            "safety": ["Full PPE; avoid waterways"],
            "source": "UF IFAS; Cornell pepper disease management guide",
        },
    ],

    # ── POTATO ────────────────────────────────────────────────────────────────
    "Potato___Early_blight": [
        {
            "active_ingredient": "Chlorothalonil",
            "product_example": "Bravo 720 SC (Syngenta)",
            "use_for": "Early blight (Alternaria solani) control on potato and tomato",
            "rate": "1.5–2.0 L/ha",
            "preparation": "Mix per label; thorough coverage important",
            "when_to_apply": "Begin at row closure or when early blight first appears; reapply on schedule",
            "frequency": "Every 7–10 days",
            "phi": "7 days",
            "safety": [
                "Suspected carcinogen – minimise exposure; wear respirator",
                "Highly toxic to fish and aquatic invertebrates",
                "NOTE: Chlorothalonil is BANNED in the EU (2020). Verify legality in your country.",
            ],
            "source": "Syngenta label; University of Idaho Extension",
        },
        {
            "active_ingredient": "Azoxystrobin",
            "product_example": "Amistar (Syngenta)",
            "use_for": "Early blight control on potato",
            "rate": "0.5–0.75 L/ha",
            "preparation": "Mix per label",
            "when_to_apply": "Preventive; at first sign of disease",
            "frequency": "Every 7–14 days; max 4 applications per season; rotate with non-strobilurin",
            "phi": "14 days",
            "safety": ["Wear PPE; manage strobilurin resistance"],
            "source": "Syngenta label",
        },
    ],

    "Potato___Late_blight": [
        {
            "active_ingredient": "Metalaxyl-M + Mancozeb",
            "product_example": "Ridomil Gold MZ (Syngenta)",
            "use_for": "Late blight (Phytophthora infestans) control on potato and tomato",
            "rate": "2.5 kg/ha",
            "preparation": "Mix in water; apply with thorough canopy coverage",
            "when_to_apply": "Preventive at high-risk periods; curative within 24–48 h of infection",
            "frequency": "Every 7–10 days during wet conditions; alternate with cymoxanil + mancozeb",
            "phi": "21 days",
            "safety": [
                "Full PPE",
                "Manage metalaxyl resistance – rotate with copper or fluazinam",
                "Avoid application within 50 m of surface water",
            ],
            "source": "Syngenta Ridomil Gold MZ label; International Potato Center (CIP)",
        },
        {
            "active_ingredient": "Cymoxanil + Mancozeb",
            "product_example": "Curzate M (DuPont/Corteva)",
            "use_for": "Late blight preventive and curative control",
            "rate": "2.0 kg/ha",
            "preparation": "Mix per label",
            "when_to_apply": "At disease onset or when forecasting systems indicate high risk",
            "frequency": "Every 7–10 days; alternate with metalaxyl-based fungicides",
            "phi": "14 days",
            "safety": ["Wear PPE", "Resistance management: rotate fungicide classes"],
            "source": "Corteva label",
        },
        {
            "active_ingredient": "Copper (Bordeaux mixture) – Organic Option",
            "product_example": "Bordeaux Mixture (various manufacturers)",
            "use_for": "Late blight prevention – certified organic",
            "rate": "5–10 kg/ha (1% Bordeaux mixture)",
            "preparation": "Prepare fresh Bordeaux mixture: dissolve copper sulphate and lime separately; combine carefully",
            "when_to_apply": "Preventive; begin before disease onset in cool, wet periods",
            "frequency": "Every 7 days in wet conditions",
            "phi": "None for copper",
            "safety": [
                "Phytotoxic in hot or wet conditions",
                "Copper accumulates in soil – limit long-term applications",
                "Wear full PPE when preparing",
            ],
            "source": "Teagasc Ireland; Organic Research Centre UK",
        },
    ],

    # ── SQUASH ────────────────────────────────────────────────────────────────
    "Squash___Powdery_mildew": [
        {
            "active_ingredient": "Potassium bicarbonate",
            "product_example": "Kaligreen / Armicarb (various)",
            "use_for": "Powdery mildew on cucurbits – OMRI-listed organic option",
            "rate": "0.5–1.0 kg/ha",
            "preparation": "Dissolve in water; apply to upper and lower leaf surfaces",
            "when_to_apply": "At first symptom or early season preventively",
            "frequency": "Every 7 days",
            "phi": "0 days",
            "safety": ["Minimal toxicity; wear eye protection"],
            "source": "UC IPM; Cornell Cooperative Extension",
        },
        {
            "active_ingredient": "Myclobutanil",
            "product_example": "Rally 40WSP",
            "use_for": "Powdery mildew control on cucurbits",
            "rate": "75–150 g/ha",
            "preparation": "Mix per label",
            "when_to_apply": "At first sign of powdery mildew",
            "frequency": "Every 10–14 days; max 4 applications per season; rotate fungicide classes",
            "phi": "1 day",
            "safety": ["Wear PPE; manage resistance by alternating FRAC codes"],
            "source": "Dow/Corteva label",
        },
    ],

    # ── STRAWBERRY ────────────────────────────────────────────────────────────
    "Strawberry___Leaf_scorch": [
        {
            "active_ingredient": "Captan",
            "product_example": "Captan 50WP (various)",
            "use_for": "Leaf scorch and other fungal diseases of strawberry",
            "rate": "2.5–3.0 kg/ha",
            "preparation": "Mix per label",
            "when_to_apply": "At first sign of disease; from early spring through harvest period",
            "frequency": "Every 10–14 days",
            "phi": "0 days",
            "safety": [
                "Probable carcinogen (IARC Group 2A)",
                "Wear respirator and full PPE",
                "Highly toxic to fish",
            ],
            "source": "Ohio State Extension; product label",
        },
    ],

    # ── TOMATO ────────────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": [
        {
            "active_ingredient": "Copper hydroxide",
            "product_example": "Kocide 3000",
            "use_for": "Bacterial spot of tomato",
            "rate": "0.75–1.5 kg/ha",
            "preparation": "Mix per label; ensure thorough coverage",
            "when_to_apply": "Preventive; begin at transplanting or first sign of disease",
            "frequency": "Every 5–7 days in wet conditions",
            "phi": "0 days",
            "safety": ["Wear PPE; avoid phytotoxicity – do NOT apply in heat"],
            "source": "UF IFAS; FMC label",
        },
    ],

    "Tomato___Early_blight": [
        {
            "active_ingredient": "Azoxystrobin",
            "product_example": "Amistar (Syngenta)",
            "use_for": "Early blight, Septoria leaf spot on tomato",
            "rate": "0.5–0.75 L/ha",
            "preparation": "Mix per label",
            "when_to_apply": "Preventive from early season; at first sign",
            "frequency": "Every 7–10 days; alternate with protectant fungicides",
            "phi": "0 days",
            "safety": ["Wear PPE; FRAC Group 11 – manage resistance"],
            "source": "Syngenta label",
        },
        {
            "active_ingredient": "Chlorothalonil",
            "product_example": "Bravo 720 SC",
            "use_for": "Early blight and Septoria leaf spot protectant on tomato",
            "rate": "1.5–2.0 L/ha",
            "preparation": "Mix per label",
            "when_to_apply": "Preventive; begin when conditions favour disease",
            "frequency": "Every 7 days",
            "phi": "7 days",
            "safety": ["BANNED in EU; verify legality; wear respirator"],
            "source": "Syngenta label; Cornell Vegetable MD",
        },
    ],

    "Tomato___Late_blight": [
        {
            "active_ingredient": "Metalaxyl-M + Chlorothalonil",
            "product_example": "Ridomil Gold Bravo (Syngenta)",
            "use_for": "Late blight of tomato",
            "rate": "2.0–2.5 L/ha",
            "preparation": "Mix per label; thorough coverage essential",
            "when_to_apply": "Preventive; begin during cool, wet weather periods",
            "frequency": "Every 7 days; alternate with copper-based products for resistance management",
            "phi": "14 days",
            "safety": ["Full PPE; chlorothalonil banned in EU"],
            "source": "Syngenta label",
        },
    ],

    "Tomato___Leaf_Mold": [
        {
            "active_ingredient": "Chlorothalonil or Mancozeb",
            "product_example": "Bravo 720 SC or Dithane M-45",
            "use_for": "Tomato leaf mould prevention in greenhouse",
            "rate": "Per label",
            "preparation": "Mix per label; improve greenhouse ventilation before applying",
            "when_to_apply": "When humidity consistently above 85%; apply preventively",
            "frequency": "Every 7–10 days",
            "phi": "7 days (chlorothalonil), 5 days (mancozeb)",
            "safety": ["Full PPE; ventilate greenhouse before re-entry"],
            "source": "Horticulture Week; UC Davis",
        },
    ],

    "Tomato___Septoria_leaf_spot": [
        {
            "active_ingredient": "Chlorothalonil",
            "product_example": "Bravo 720 SC",
            "use_for": "Septoria leaf spot of tomato",
            "rate": "1.5–2.0 L/ha",
            "preparation": "Mix per label",
            "when_to_apply": "Begin at seedling stage or at transplanting; preventive",
            "frequency": "Every 7 days in wet conditions",
            "phi": "7 days",
            "safety": ["Banned in EU; wear respirator; toxic to aquatic life"],
            "source": "Cornell Vegetable MD; Penn State Extension",
        },
    ],

    "Tomato___Spider_mites Two-spotted_spider_mite": [
        {
            "active_ingredient": "Abamectin",
            "product_example": "Vertimec 018EC (Syngenta)",
            "use_for": "Two-spotted spider mite control on tomato",
            "rate": "0.75–1.5 L/ha",
            "preparation": "Mix per label; add spreader; apply to underside of leaves",
            "when_to_apply": "When threshold of 5–10 mites per leaf is reached",
            "frequency": "Every 14 days; maximum 2 applications per season; rotate IRAC class",
            "phi": "3 days",
            "safety": [
                "Highly toxic to bees – do NOT apply to flowering plants",
                "Wear full PPE",
                "Toxic to fish",
            ],
            "source": "Syngenta Vertimec label; UC IPM",
        },
        {
            "active_ingredient": "Bifenazate",
            "product_example": "Floramite SC (Chemtura/Lanxess)",
            "use_for": "Spider mite control; fast knockdown of all life stages",
            "rate": "0.6–0.9 L/ha",
            "preparation": "Mix per label",
            "when_to_apply": "At mite population detection; acts quickly",
            "frequency": "1–2 applications; rotate IRAC class",
            "phi": "1 day",
            "safety": ["Wear PPE; resistance risk – rotate with abamectin"],
            "source": "Chemtura label",
        },
    ],

    "Tomato___Target_Spot": [
        {
            "active_ingredient": "Azoxystrobin + Difenoconazole",
            "product_example": "Amistar Top (Syngenta)",
            "use_for": "Target spot (Corynespora cassiicola) on tomato",
            "rate": "0.75–1.0 L/ha",
            "preparation": "Mix per label",
            "when_to_apply": "At first sign of disease",
            "frequency": "Every 10–14 days; max 4 applications",
            "phi": "1 day",
            "safety": ["Wear PPE; manage resistance"],
            "source": "Syngenta label",
        },
    ],

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": [
        {
            "active_ingredient": "Thiamethoxam (for psyllid/whitefly vector control)",
            "product_example": "Actara 25WG (Syngenta)",
            "use_for": "Silverleaf whitefly (Bemisia tabaci) control – prevents TYLCV spread",
            "rate": "0.14–0.2 kg/ha",
            "preparation": "Mix per label; soil drench or foliar application",
            "when_to_apply": "At transplanting (preventive) and at first whitefly detection",
            "frequency": "As needed; rotate insecticide classes; max per label",
            "phi": "3 days",
            "safety": [
                "HIGHLY TOXIC to bees and pollinators",
                "Neonicotinoid – restricted in EU and some other regions",
                "Verify current registration and restrictions in your country",
            ],
            "source": "Syngenta Actara label; Cornell Vegetable MD",
        },
    ],

    "Tomato___Tomato_mosaic_virus": [
        {
            "active_ingredient": "N/A – No chemical cure for viral infections",
            "product_example": "Prevention only",
            "use_for": "No pesticide cures viral infections. Management is preventive.",
            "rate": "N/A",
            "preparation": "N/A",
            "when_to_apply": "N/A",
            "frequency": "N/A",
            "phi": "N/A",
            "safety": ["Focus on sanitation and roguing infected plants"],
            "source": "UC Davis Plant Pathology; RHS",
        },
    ],

    # ── CHERRY ────────────────────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": [
        {
            "active_ingredient": "Sulfur",
            "product_example": "Thiovit Jet (Syngenta)",
            "use_for": "Powdery mildew on cherry (Podosphaera clandestina)",
            "rate": "3–6 kg/ha",
            "preparation": "Mix per label; wettable sulfur",
            "when_to_apply": "Preventive; begin at shoot emergence",
            "frequency": "Every 7–10 days during active growth",
            "phi": "1 day",
            "safety": [
                "Do NOT apply in temperatures above 32 °C (risk of phytotoxicity)",
                "Wear PPE",
            ],
            "source": "WSU Tree Fruit; Syngenta label",
        },
    ],
}


def get_treatment_info(class_label: str) -> list[dict]:
    """Return list of treatment options for a class label."""
    treatments = TREATMENT_DB.get(class_label, [])
    if not treatments:
        # Healthy class or unknown
        from app.services.disease_kb import parse_class_label
        plant, disease = parse_class_label(class_label)
        if disease.lower() == "healthy":
            return [{
                "active_ingredient": "None required",
                "product_example": "N/A",
                "use_for": "Plant is healthy – no treatment needed",
                "rate": "N/A",
                "preparation": "N/A",
                "when_to_apply": "N/A",
                "frequency": "N/A",
                "phi": "N/A",
                "safety": ["Continue regular monitoring"],
                "source": "N/A",
            }]
        return [{
            "active_ingredient": "Consult a local agronomist",
            "product_example": "Not available in this database",
            "use_for": f"Specific treatment information for {disease} on {plant} is not yet in this database.",
            "rate": "Consult local agricultural extension service",
            "preparation": "N/A",
            "when_to_apply": "N/A",
            "frequency": "N/A",
            "phi": "N/A",
            "safety": ["Always consult a qualified agronomist before applying any pesticide"],
            "source": "Consult local agricultural authority",
        }]
    return treatments


# ── Product listing (curated, no fabricated links) ───────────────────────────
PRODUCT_LISTING: dict[str, list[dict]] = {
    "Apple___Apple_scab": [
        {
            "product_name": "Rally 40WSP",
            "active_ingredient": "Myclobutanil 40%",
            "manufacturer": "Dow AgroSciences (now Corteva)",
            "type": "Fungicide – DMI (FRAC Group 3)",
            "availability": "Available through authorised agricultural dealers in USA, Canada, UK, Australia",
            "buy_link_note": "Search 'Rally 40WSP' on agri-retailer sites such as Wilbur-Ellis, Helena, or your local co-op",
        },
        {
            "product_name": "Dithane M-45",
            "active_ingredient": "Mancozeb 80%",
            "manufacturer": "Corteva Agriscience",
            "type": "Fungicide – Multi-site (FRAC Group M3)",
            "availability": "Widely available globally through agri-retailers",
            "buy_link_note": "Search 'Dithane M-45' on Amazon Agricultural, Nutrien, or local dealers",
        },
    ],
    "Potato___Late_blight": [
        {
            "product_name": "Ridomil Gold MZ",
            "active_ingredient": "Metalaxyl-M 3.8% + Mancozeb 64%",
            "manufacturer": "Syngenta",
            "type": "Fungicide – Phenylamide + Multi-site (FRAC Group 4 + M3)",
            "availability": "Available in most potato-producing countries",
            "buy_link_note": "Search 'Ridomil Gold MZ' on Syngenta.com or local distributors",
        },
    ],
}


def get_product_listing(class_label: str) -> list[dict]:
    return PRODUCT_LISTING.get(class_label, [])
