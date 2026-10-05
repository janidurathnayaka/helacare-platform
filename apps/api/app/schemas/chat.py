from typing import Literal
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)
    language: Literal["en", "si"] = "en"

class ChatSource(BaseModel):
    plant_id: int
    name: str
    source_url: str | None

class ChatResponse(BaseModel):
    audit_id: int | None = None
    triage_level: Literal["normal", "urgent"]
    answer: str
    sources: list[ChatSource]
    disclaimer: str
