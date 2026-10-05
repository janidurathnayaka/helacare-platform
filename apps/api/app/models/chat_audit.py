from datetime import datetime

from sqlalchemy import DateTime, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class ChatAudit(Base):
    __tablename__ = "chat_audits"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(16))
    triage_level: Mapped[str] = mapped_column(String(32))
    answer: Mapped[str] = mapped_column(Text)
    source_ids: Mapped[list[int]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
