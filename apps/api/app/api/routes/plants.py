from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.plant import Plant
from app.schemas.plant import PlantOut

router = APIRouter(prefix="/plants", tags=["plants"])

@router.get("", response_model=list[PlantOut])
async def list_plants(
    search: str | None = Query(default=None, max_length=200),
    verified_only: bool = True,
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Plant)

    if verified_only:
        stmt = stmt.where(Plant.is_verified.is_(True))

    if search:
        q = f"%{search}%"
        stmt = stmt.where(
            or_(
                Plant.sinhala_name.ilike(q),
                Plant.common_name.ilike(q),
                Plant.scientific_name.ilike(q),
                Plant.traditional_use.ilike(q),
            )
        )

    stmt = stmt.order_by(Plant.common_name.asc().nullslast()).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())
