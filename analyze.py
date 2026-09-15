"""
/api/analyze – image upload & inference endpoint
"""
from __future__ import annotations

import os
import uuid
import json
import logging
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import Image
import io

from app.db.database import get_db
from app.db.models import PredictionRecord
from app.services.model_service import run_inference
from app.services.disease_kb import get_disease_info, parse_class_label
from app.services.treatment_db import get_treatment_info, get_product_listing

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_CONTENT_TYPES = {
    "image/jpeg", "image/jpg", "image/png", "image/webp",
    "image/gif",  # allow gif for robustness
}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


class Top3Item(BaseModel):
    label: str
    confidence: float
    plant_name: str = ""
    disease_name: str = ""


class AnalysisResponse(BaseModel):
    id: int
    is_demo: bool
    plant_name: str
    disease_name: str
    class_label: str
    confidence: float
    severity: str
    low_confidence_warning: bool
    top3: list[dict]
    # Grad-CAM: three variants (original, heatmap-only, overlay)
    gradcam_original_b64: str
    gradcam_heatmap_b64: str
    gradcam_overlay_b64: str
    model_used: str
    disease_info: dict
    treatments: list[dict]
    products: list[dict]
    image_url: str


@router.post("/", response_model=AnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # ── Validate content type ─────────────────────────────────────────────────
    ct = (file.content_type or "").lower()
    if ct not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ct}'. Please upload JPEG, PNG, or WEBP."
        )

    raw = await file.read()

    # ── Validate file size ────────────────────────────────────────────────────
    if len(raw) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 20 MB.")

    if len(raw) < 100:
        raise HTTPException(status_code=400, detail="File is too small to be a valid image.")

    # ── Open and validate image ───────────────────────────────────────────────
    try:
        img = Image.open(io.BytesIO(raw))
        img.verify()  # Checks for corruption
        img = Image.open(io.BytesIO(raw))  # Re-open after verify (verify closes file)
    except Exception:
        raise HTTPException(status_code=400, detail="Cannot read image file. Ensure it is a valid JPEG/PNG/WEBP.")

    # Check minimum resolution
    if img.width < 32 or img.height < 32:
        raise HTTPException(status_code=400, detail="Image too small. Minimum 32×32 pixels required.")

    # ── Save uploaded image ───────────────────────────────────────────────────
    filename = f"{uuid.uuid4().hex}.jpg"
    save_path = UPLOAD_DIR / filename
    img.convert("RGB").save(str(save_path), format="JPEG", quality=92)

    # ── Run inference ──────────────────────────────────────────────────────────
    try:
        result = run_inference(img)
    except Exception as e:
        logger.error(f"Inference error: {e}", exc_info=True)
        # Fall back to demo mode on inference failure
        result = run_inference(img, use_demo=True)

    # ── Persist to DB ─────────────────────────────────────────────────────────
    record = PredictionRecord(
        image_path=f"/uploads/{filename}",
        plant_name=result["plant_name"],
        disease_name=result["disease_name"],
        class_label=result["class_label"],
        confidence=result["confidence"],
        severity=result["severity"],
        top3=json.dumps(result["top3"]),
        is_demo=result["is_demo"],
        model_used=result["model_used"],
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    disease_info = get_disease_info(result["class_label"])
    treatments = get_treatment_info(result["class_label"])
    products = get_product_listing(result["class_label"])

    return AnalysisResponse(
        id=record.id,
        is_demo=result["is_demo"],
        plant_name=result["plant_name"],
        disease_name=result["disease_name"],
        class_label=result["class_label"],
        confidence=result["confidence"],
        severity=result["severity"],
        low_confidence_warning=result["low_confidence_warning"],
        top3=result["top3"],
        gradcam_original_b64=result.get("gradcam_original_b64", ""),
        gradcam_heatmap_b64=result.get("gradcam_heatmap_b64", ""),
        gradcam_overlay_b64=result.get("gradcam_overlay_b64", ""),
        model_used=result["model_used"],
        disease_info=disease_info,
        treatments=treatments,
        products=products,
        image_url=f"/uploads/{filename}",
    )
