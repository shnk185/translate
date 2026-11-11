from pydantic import BaseModel, Field

class TranslateRequest(BaseModel):
    query: str
    source_lang: str
    dest_lang: str = "English"
    preset: int

class TranslateWord(BaseModel):
    id: int
    chunk: str
    meaning: str

class TranslateRead(BaseModel):
    id: int
    translation: str
    words: list[TranslateWord]


