from pydantic import BaseModel, Field

class TranslateRequest(BaseModel):
    query: str
    source_lang: str
    dest_lang: str = "English"
    words: list[str] = Field(default_factory=list, max_length=200)


