from fastapi import APIRouter

from app.api.routes import admin, chat, feedback, health, plants

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(plants.router)
api_router.include_router(chat.router)
api_router.include_router(feedback.router)
api_router.include_router(admin.router)
