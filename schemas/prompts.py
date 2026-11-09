from pydantic import BaseModel, Field
from enums import PromptType

class PromptCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    text: str = Field(min_length=1)
    prompt_type: PromptType = PromptType.USER

class PromptRead(PromptCreate):
    id: int
    model_config = {"from_attributes": True}
