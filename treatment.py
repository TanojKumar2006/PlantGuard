"""
/api/treatment – treatment & pesticide guide lookup
"""
from __future__ import annotations
from fastapi import APIRouter, Query
from app.services.treatment_db import get_treatment_info, get_product_listing, TREATMENT_DB

router = APIRouter()


@router.get("/")
async def get_all_treatments():
    """Return all available treatment entries."""
    return {
        "disclaimer": "All treatment information is sourced from published product labels and university extension services. Always consult the current registered product label in your country before applying any pesticide.",
        "entries": list(TREATMENT_DB.keys()),
    }


@router.get("/{class_label:path}")
async def get_treatment(class_label: str):
    from app.services.disease_kb import get_disease_info, parse_class_label
    plant, disease = parse_class_label(class_label)
    treatments = get_treatment_info(class_label)
    products = get_product_listing(class_label)
    disease_info = get_disease_info(class_label)
    return {
        "class_label": class_label,
        "plant_name": plant,
        "disease_name": disease,
        "disclaimer": "Always verify pesticide registration and follow the current product label in your country. This information is for educational purposes only.",
        "treatments": treatments,
        "products": products,
        "prevention": disease_info.get("prevention", []),
        "cultural_biological": disease_info.get("cultural_biological", []),
    }
