from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class AdminLogin(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class PlantWrite(BaseModel):
    external_id: str | None = Field(default=None, max_length=64)
    sinhala_name: str | None = Field(default=None, max_length=255)
    common_name: str | None = Field(default=None, max_length=255)
    scientific_name: str | None = Field(default=None, max_length=255)
    part_used: str | None = None
    traditional_use: str = Field(min_length=3)
    preparation: str | None = None
    safety_note: str | None = None
    source_url: str | None = None
    verification_status: str = "UNVERIFIED"
    safety_review_status: str = "REVIEW_REQUIRED"
    is_verified: bool = False


class SourceWrite(BaseModel):
    plant_id: int | None = None
    title: str = Field(min_length=2, max_length=255)
    institution: str | None = Field(default=None, max_length=255)
    url: str
    publication_year: int | None = Field(default=None, ge=1800, le=2200)
    verification_status: str = "PENDING"
    notes: str | None = None


class SourceOut(SourceWrite):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class ReviewWrite(BaseModel):
    plant_id: int
    reviewer_name: str = Field(min_length=2, max_length=255)
    reviewer_role: str | None = Field(default=None, max_length=255)
    status: str = "PENDING"
    comments: str | None = None


class ReviewOut(ReviewWrite):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class FeedbackCreate(BaseModel):
    chat_audit_id: int | None = None
    helpful: bool | None = None
    category: str = "GENERAL"
    comment: str | None = Field(default=None, max_length=2000)


class FeedbackOut(FeedbackCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    resolved: bool
    created_at: datetime


class SafetyFlagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    chat_audit_id: int | None
    message_excerpt: str
    severity: str
    reason: str
    status: str
    created_at: datetime


class AuditOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    actor: str
    action: str
    entity_type: str
    entity_id: str | None
    details: str | None
    created_at: datetime
