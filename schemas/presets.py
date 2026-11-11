from pydantic import BaseModel, Field

class PresetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    prompt_ids: list[int]

class PresetResponse(PresetCreate):
    id: int
    model_config = {"from_attributes": True}