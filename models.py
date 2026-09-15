"""
SQLAlchemy ORM models
"""
import datetime
from sqlalchemy import Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class PredictionRecord(Base):
    __tablename__ = "prediction_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    image_path: Mapped[str] = mapped_column(String(512))
    plant_name: Mapped[str] = mapped_column(String(128))
    disease_name: Mapped[str] = mapped_column(String(256))
    class_label: Mapped[str] = mapped_column(String(256), default="")
    confidence: Mapped[float] = mapped_column(Float)
    severity: Mapped[str] = mapped_column(String(64))
    top3: Mapped[str] = mapped_column(Text, default="[]")         # JSON string
    gradcam_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    model_used: Mapped[str] = mapped_column(String(256), default="EfficientNetB0")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
