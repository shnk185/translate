from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db import get_db
from service.translate_service import OllamaError, translate_and_store
from schemas.translate import TranslateRequest, TranslateRead
router = APIRouter()

@router.post("/translate", response_model=TranslateRead)
def translate(req: TranslateRequest, db: Session = Depends(get_db)):
    try:
        result = translate_and_store(req.query,  req.source_lang, req.dest_lang, db)
        db.commit()
        return result
    except OllamaError as exc:
        raise HTTPException(status_code=503, detail=str(exc))