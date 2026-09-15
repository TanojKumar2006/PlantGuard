"""
/api/library – plant encyclopedia
"""
from __future__ import annotations
from fastapi import APIRouter, Query
from app.services.disease_kb import DISEASE_KB, CLASS_LABELS, parse_class_label

router = APIRouter()

# Build plant library from the KB
def _build_library():
    plants: dict[str, dict] = {}
    for label in CLASS_LABELS:
        plant, disease = parse_class_label(label)
        if plant not in plants:
            plants[plant] = {
                "name": plant,
                "diseases": [],
                "healthy_class": None,
            }
        info = DISEASE_KB.get(label, {})
        if disease.lower() == "healthy":
            plants[plant]["healthy_class"] = label
        else:
            plants[plant]["diseases"].append({
                "class_label": label,
                "disease_name": disease,
                "common_name": info.get("common_name", disease),
                "type": info.get("type", "Unknown"),
                "summary": info.get("summary", ""),
            })
    return list(plants.values())


_LIBRARY = _build_library()


@router.get("/")
async def get_library(search: str = Query("", alias="q")):
    if not search:
        return _LIBRARY
    q = search.lower()
    return [
        p for p in _LIBRARY
        if q in p["name"].lower()
        or any(q in d["disease_name"].lower() or q in d["common_name"].lower() for d in p["diseases"])
    ]


@router.get("/{plant_name}")
async def get_plant(plant_name: str):
    for p in _LIBRARY:
        if p["name"].lower() == plant_name.lower():
            return p
    return {"error": "Plant not found"}


@router.get("/disease/{class_label:path}")
async def get_disease_detail(class_label: str):
    from app.services.disease_kb import get_disease_info
    from app.services.treatment_db import get_treatment_info, get_product_listing
    info = get_disease_info(class_label)
    treatments = get_treatment_info(class_label)
    products = get_product_listing(class_label)
    plant, disease = parse_class_label(class_label)
    return {
        "class_label": class_label,
        "plant_name": plant,
        "disease_name": disease,
        "disease_info": info,
        "treatments": treatments,
        "products": products,
    }
