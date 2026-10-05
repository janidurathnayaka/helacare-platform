from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.db.base import Base

class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    sinhala_name: Mapped[str | None] = mapped_column(String(255), index=True)
    common_name: Mapped[str | None] = mapped_column(String(255), index=True)
    scientific_name: Mapped[str | None] = mapped_column(String(255), index=True)
    part_used: Mapped[str | None] = mapped_column(Text)
    traditional_use: Mapped[str] = mapped_column(Text)
    preparation: Mapped[str | None] = mapped_column(Text)
    safety_note: Mapped[str | None] = mapped_column(Text)
    source_url: Mapped[str | None] = mapped_column(Text)
    verification_status: Mapped[str] = mapped_column(String(64), default="UNVERIFIED")
    safety_review_status: Mapped[str] = mapped_column(String(64), default="REVIEW_REQUIRED")
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
