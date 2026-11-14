from pydantic import BaseModel

class LanguagesResponse(BaseModel):
    languages: list[str]