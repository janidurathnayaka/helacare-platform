from pydantic import BaseModel, ConfigDict

class PlantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str | None
    sinhala_name: str | None
    common_name: str | None
    scientific_name: str | None
    part_used: str | None
    traditional_use: str
    preparation: str | None
    safety_note: str | None
    source_url: str | None
    verification_status: str
    safety_review_status: str
    is_verified: bool
