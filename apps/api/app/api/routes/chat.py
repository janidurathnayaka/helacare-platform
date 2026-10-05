from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.metrics import CHAT_REQUESTS
from app.db.session import get_db
from app.models.chat_audit import ChatAudit
from app.models.platform import SafetyFlag
from app.schemas.chat import ChatRequest, ChatResponse, ChatSource
from app.services.answering import DISCLAIMER_EN, DISCLAIMER_SI, compose_grounded_answer, compose_urgent_answer
from app.services.retrieval import retrieve_verified_plants
from app.services.safety import evaluate_safety

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    safety = evaluate_safety(payload.message)
    disclaimer = DISCLAIMER_SI if payload.language == "si" else DISCLAIMER_EN

    if safety.urgent:
        answer = compose_urgent_answer(payload.language)
        record = ChatAudit(message=payload.message, language=payload.language, triage_level="urgent", answer=answer, source_ids=[])
        db.add(record)
        await db.flush()
        db.add(SafetyFlag(chat_audit_id=record.id, message_excerpt=payload.message[:500], severity="HIGH", reason="Emergency red-flag gate", status="OPEN"))
        await db.commit()
        CHAT_REQUESTS.labels(payload.language, "urgent").inc()
        return ChatResponse(triage_level="urgent", answer=answer, sources=[], disclaimer=disclaimer, audit_id=record.id)

    plants = await retrieve_verified_plants(db, payload.message)
    answer = compose_grounded_answer(plants, payload.language)
    sources = [
        ChatSource(plant_id=p.id, name=p.sinhala_name or p.common_name or p.scientific_name or f"Plant #{p.id}", source_url=p.source_url)
        for p in plants
    ]
    record = ChatAudit(message=payload.message, language=payload.language, triage_level="normal", answer=answer, source_ids=[p.id for p in plants])
    db.add(record)
    await db.commit()
    await db.refresh(record)
    CHAT_REQUESTS.labels(payload.language, "normal").inc()
    return ChatResponse(triage_level="normal", answer=answer, sources=sources, disclaimer=disclaimer, audit_id=record.id)
