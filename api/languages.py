from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from schemas.languages import LanguagesResponse
from service.language_service import get_available_languages

router = APIRouter(prefix="/languages", tags=["languages"])

@router.get("", response_model=LanguagesResponse)
def languages(db: Session = Depends(get_db)):
    available_langs = get_available_languages(db)
    return LanguagesResponse(languages=available_langs)
