"""
/api/history – prediction history CRUD
"""
from __future__ import annotations

import json
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.database import get_db
from app.db.models import PredictionRecord
from app.services.disease_kb import get_disease_info, parse_class_label
from app.services.treatment_db import get_treatment_info, get_product_listing

router = APIRouter()


class HistoryItem(BaseModel):
    id: int
    created_at: str
    image_path: str
    plant_name: str
    disease_name: str
    class_label: str
    confidence: float
    severity: str
    top3: list
    is_demo: bool
    model_used: str

    class Config:
        from_attributes = True


def _parse_record(r: PredictionRecord) -> HistoryItem:
    try:
        top3 = json.loads(r.top3) if r.top3 else []
    except Exception:
        top3 = []
    return HistoryItem(
        id=r.id,
        created_at=r.created_at.isoformat() if r.created_at else "",
        image_path=r.image_path,
        plant_name=r.plant_name,
        disease_name=r.disease_name,
        class_label=getattr(r, 'class_label', '') or '',
        confidence=r.confidence,
        severity=r.severity,
        top3=top3,
        is_demo=r.is_demo,
        model_used=r.model_used,
    )


@router.get("/", response_model=list[HistoryItem])
async def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    plant: Optional[str] = Query(None),
    disease: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(PredictionRecord).order_by(PredictionRecord.created_at.desc())
    if plant:
        stmt = stmt.where(PredictionRecord.plant_name.ilike(f"%{plant}%"))
    if disease:
        stmt = stmt.where(PredictionRecord.disease_name.ilike(f"%{disease}%"))
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    records = result.scalars().all()
    return [_parse_record(r) for r in records]


@router.get("/count")
async def get_history_count(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count()).select_from(PredictionRecord))
    count = result.scalar() or 0

    # Most detected disease
    from sqlalchemy import text
    most_common_result = await db.execute(
        text(
            "SELECT disease_name, COUNT(*) as cnt FROM prediction_history "
            "WHERE disease_name != 'Healthy' "
            "GROUP BY disease_name ORDER BY cnt DESC LIMIT 1"
        )
    )
    row = most_common_result.fetchone()
    most_common = row[0] if row else None

    # Healthy vs diseased
    healthy_result = await db.execute(
        select(func.count()).select_from(PredictionRecord)
        .where(PredictionRecord.disease_name == "Healthy")
    )
    healthy_count = healthy_result.scalar() or 0

    return {
        "count": count,
        "healthy": healthy_count,
        "diseased": count - healthy_count,
        "most_common_disease": most_common,
    }


@router.get("/{record_id}", response_model=dict)
async def get_record(record_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single history record with full disease info and treatments."""
    result = await db.execute(
        select(PredictionRecord).where(PredictionRecord.id == record_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found.")

    item = _parse_record(record)
    class_label = item.class_label or ""

    # Reconstruct class_label if missing (from plant+disease names)
    if not class_label:
        class_label = f"{record.plant_name.replace(' ', '_')}___{record.disease_name.replace(' ', '_')}"

    disease_info = get_disease_info(class_label) if class_label else {}
    treatments = get_treatment_info(class_label) if class_label else []
    products = get_product_listing(class_label) if class_label else []

    return {
        **item.model_dump(),
        "disease_info": disease_info,
        "treatments": treatments,
        "products": products,
    }


@router.delete("/{record_id}")
async def delete_record(record_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PredictionRecord).where(PredictionRecord.id == record_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found.")
    await db.execute(delete(PredictionRecord).where(PredictionRecord.id == record_id))
    await db.commit()
    return {"deleted": record_id}


@router.delete("/")
async def clear_history(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(PredictionRecord))
    await db.commit()
    return {"message": "History cleared"}
