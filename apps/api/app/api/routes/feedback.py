from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.platform import UserFeedback
from app.schemas.admin import FeedbackCreate, FeedbackOut

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackOut, status_code=status.HTTP_201_CREATED)
async def create_feedback(payload: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    item = UserFeedback(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
