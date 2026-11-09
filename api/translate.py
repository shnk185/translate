from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db import get_db
from service.translate_service import OllamaError
from service.translate_service import translate as translate_text
from schemas.translate import TranslateRequest
from service.chunk_service import upsert_chunks
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/translate")
def translate(req: TranslateRequest, db: Session = Depends(get_db)):
    try:
        result = {"translation": translate_text(req.query,  req.source_lang, req.dest_lang, req.words)}
        upsert_chunks(db, words=req.words)
        db.commit()
        return result
    except OllamaError as exc:
        raise HTTPException(status_code=503, detail=str(exc))