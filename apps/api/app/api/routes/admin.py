from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import authenticate_admin, create_admin_token, require_admin
from app.core.config import settings
from app.db.session import get_db
from app.models.chat_audit import ChatAudit
from app.models.plant import Plant
from app.models.platform import AuditEvent, PractitionerReview, SafetyFlag, SourceRecord, UserFeedback
from app.schemas.admin import (
    AdminLogin,
    AuditOut,
    FeedbackOut,
    PlantWrite,
    ReviewOut,
    ReviewWrite,
    SafetyFlagOut,
    SourceOut,
    SourceWrite,
    TokenOut,
)
from app.schemas.plant import PlantOut
from app.services.embeddings import embed_text, plant_embedding_text

router = APIRouter(prefix="/admin", tags=["admin"])


async def audit(db: AsyncSession, actor: str, action: str, entity_type: str, entity_id=None, details=None):
    db.add(AuditEvent(actor=actor, action=action, entity_type=entity_type, entity_id=str(entity_id) if entity_id is not None else None, details=details))


@router.post("/login", response_model=TokenOut)
async def login(payload: AdminLogin):
    if not authenticate_admin(payload.email, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenOut(
        access_token=create_admin_token(payload.email),
        expires_in_minutes=settings.jwt_exp_minutes,
    )


@router.get("/stats")
async def stats(_: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    async def count(model, *criteria):
        stmt = select(func.count()).select_from(model)
        for criterion in criteria:
            stmt = stmt.where(criterion)
        return (await db.execute(stmt)).scalar_one()

    return {
        "plants": await count(Plant),
        "verified_plants": await count(Plant, Plant.is_verified.is_(True)),
        "pending_plants": await count(Plant, Plant.is_verified.is_(False)),
        "sources": await count(SourceRecord),
        "pending_reviews": await count(PractitionerReview, PractitionerReview.status == "PENDING"),
        "open_feedback": await count(UserFeedback, UserFeedback.resolved.is_(False)),
        "open_safety_flags": await count(SafetyFlag, SafetyFlag.status == "OPEN"),
        "chat_audits": await count(ChatAudit),
    }


@router.get("/analytics")
async def analytics(_: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    langs = await db.execute(select(ChatAudit.language, func.count(ChatAudit.id)).group_by(ChatAudit.language))
    triage = await db.execute(select(ChatAudit.triage_level, func.count(ChatAudit.id)).group_by(ChatAudit.triage_level))
    feedback = await db.execute(select(UserFeedback.helpful, func.count(UserFeedback.id)).group_by(UserFeedback.helpful))
    recent = await db.execute(select(ChatAudit).order_by(ChatAudit.created_at.desc()).limit(10))
    return {
        "languages": {k: v for k, v in langs.all()},
        "triage": {k: v for k, v in triage.all()},
        "feedback": {str(k): v for k, v in feedback.all()},
        "recent_queries": [
            {"id": x.id, "message": x.message[:120], "language": x.language, "triage": x.triage_level, "created_at": x.created_at}
            for x in recent.scalars().all()
        ],
    }


@router.get("/plants", response_model=list[PlantOut])
async def admin_plants(
    search: str | None = Query(default=None, max_length=200),
    _: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Plant)
    if search:
        q = f"%{search}%"
        stmt = stmt.where(or_(Plant.sinhala_name.ilike(q), Plant.common_name.ilike(q), Plant.scientific_name.ilike(q), Plant.traditional_use.ilike(q)))
    result = await db.execute(stmt.order_by(Plant.id.desc()).limit(250))
    return list(result.scalars().all())


@router.post("/plants", response_model=PlantOut, status_code=status.HTTP_201_CREATED)
async def create_plant(payload: PlantWrite, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    plant = Plant(**payload.model_dump())
    plant.embedding = embed_text(plant_embedding_text(plant))
    db.add(plant)
    await db.flush()
    await audit(db, admin["sub"], "CREATE", "plant", plant.id, plant.common_name or plant.sinhala_name)
    await db.commit()
    await db.refresh(plant)
    return plant


@router.put("/plants/{plant_id}", response_model=PlantOut)
async def update_plant(plant_id: int, payload: PlantWrite, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    plant = await db.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    for key, value in payload.model_dump().items():
        setattr(plant, key, value)
    plant.embedding = embed_text(plant_embedding_text(plant))
    await audit(db, admin["sub"], "UPDATE", "plant", plant.id, plant.common_name or plant.sinhala_name)
    await db.commit()
    await db.refresh(plant)
    return plant


@router.post("/plants/{plant_id}/verify", response_model=PlantOut)
async def verify_plant(plant_id: int, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    plant = await db.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    plant.is_verified = True
    plant.verification_status = "VERIFIED"
    await audit(db, admin["sub"], "VERIFY", "plant", plant.id)
    await db.commit()
    await db.refresh(plant)
    return plant


@router.delete("/plants/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_plant(plant_id: int, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    plant = await db.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    await audit(db, admin["sub"], "DELETE", "plant", plant.id, plant.common_name or plant.sinhala_name)
    await db.delete(plant)
    await db.commit()


@router.get("/sources", response_model=list[SourceOut])
async def list_sources(_: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SourceRecord).order_by(SourceRecord.created_at.desc()).limit(250))
    return list(result.scalars().all())


@router.post("/sources", response_model=SourceOut, status_code=201)
async def create_source(payload: SourceWrite, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    item = SourceRecord(**payload.model_dump())
    db.add(item)
    await db.flush()
    await audit(db, admin["sub"], "CREATE", "source", item.id, item.title)
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/sources/{item_id}", response_model=SourceOut)
async def update_source(item_id: int, payload: SourceWrite, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    item = await db.get(SourceRecord, item_id)
    if not item:
        raise HTTPException(404, "Source not found")
    for k, v in payload.model_dump().items():
        setattr(item, k, v)
    await audit(db, admin["sub"], "UPDATE", "source", item.id, item.title)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/sources/{item_id}", status_code=204)
async def delete_source(item_id: int, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    item = await db.get(SourceRecord, item_id)
    if not item:
        raise HTTPException(404, "Source not found")
    await audit(db, admin["sub"], "DELETE", "source", item.id, item.title)
    await db.delete(item)
    await db.commit()


@router.get("/reviews", response_model=list[ReviewOut])
async def list_reviews(_: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PractitionerReview).order_by(PractitionerReview.created_at.desc()).limit(250))
    return list(result.scalars().all())


@router.post("/reviews", response_model=ReviewOut, status_code=201)
async def create_review(payload: ReviewWrite, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    item = PractitionerReview(**payload.model_dump())
    db.add(item)
    await db.flush()
    await audit(db, admin["sub"], "CREATE", "practitioner_review", item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/reviews/{item_id}", response_model=ReviewOut)
async def update_review(item_id: int, payload: ReviewWrite, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    item = await db.get(PractitionerReview, item_id)
    if not item:
        raise HTTPException(404, "Review not found")
    for k, v in payload.model_dump().items():
        setattr(item, k, v)
    await audit(db, admin["sub"], "UPDATE", "practitioner_review", item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/feedback", response_model=list[FeedbackOut])
async def list_feedback(_: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserFeedback).order_by(UserFeedback.created_at.desc()).limit(250))
    return list(result.scalars().all())


@router.post("/feedback/{item_id}/resolve", response_model=FeedbackOut)
async def resolve_feedback(item_id: int, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    item = await db.get(UserFeedback, item_id)
    if not item:
        raise HTTPException(404, "Feedback not found")
    item.resolved = True
    await audit(db, admin["sub"], "RESOLVE", "feedback", item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/safety-flags", response_model=list[SafetyFlagOut])
async def list_flags(_: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SafetyFlag).order_by(SafetyFlag.created_at.desc()).limit(250))
    return list(result.scalars().all())


@router.post("/safety-flags/{item_id}/close", response_model=SafetyFlagOut)
async def close_flag(item_id: int, admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    item = await db.get(SafetyFlag, item_id)
    if not item:
        raise HTTPException(404, "Safety flag not found")
    item.status = "CLOSED"
    await audit(db, admin["sub"], "CLOSE", "safety_flag", item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/audit", response_model=list[AuditOut])
async def audit_events(_: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(250))
    return list(result.scalars().all())


@router.post("/rag/reindex")
async def reindex(admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plant))
    plants = list(result.scalars().all())
    for plant in plants:
        plant.embedding = embed_text(plant_embedding_text(plant))
    await audit(db, admin["sub"], "REINDEX", "rag", details=f"{len(plants)} plant embeddings refreshed")
    await db.commit()
    return {"indexed": len(plants), "dimensions": 256}
