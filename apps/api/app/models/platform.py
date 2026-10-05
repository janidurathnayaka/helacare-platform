from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SourceRecord(Base):
    __tablename__ = "source_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    plant_id: Mapped[int | None] = mapped_column(ForeignKey("plants.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    institution: Mapped[str | None] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(Text)
    publication_year: Mapped[int | None] = mapped_column(Integer)
    verification_status: Mapped[str] = mapped_column(String(64), default="PENDING", index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PractitionerReview(Base):
    __tablename__ = "practitioner_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id", ondelete="CASCADE"), index=True)
    reviewer_name: Mapped[str] = mapped_column(String(255))
    reviewer_role: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(64), default="PENDING", index=True)
    comments: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_audit_id: Mapped[int | None] = mapped_column(ForeignKey("chat_audits.id", ondelete="SET NULL"), index=True)
    helpful: Mapped[bool | None] = mapped_column(Boolean)
    category: Mapped[str] = mapped_column(String(64), default="GENERAL", index=True)
    comment: Mapped[str | None] = mapped_column(Text)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SafetyFlag(Base):
    __tablename__ = "safety_flags"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_audit_id: Mapped[int | None] = mapped_column(ForeignKey("chat_audits.id", ondelete="SET NULL"), index=True)
    message_excerpt: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(32), default="HIGH", index=True)
    reason: Mapped[str] = mapped_column(String(255), default="Emergency red-flag gate")
    status: Mapped[str] = mapped_column(String(64), default="OPEN", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor: Mapped[str] = mapped_column(String(255), default="system")
    action: Mapped[str] = mapped_column(String(128), index=True)
    entity_type: Mapped[str] = mapped_column(String(64), index=True)
    entity_id: Mapped[str | None] = mapped_column(String(64))
    details: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
