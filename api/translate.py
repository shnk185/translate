from fastapi import APIRouter, HTTPException

from service.translate_service import OllamaError
from service.translate_service import translate as translate_text
from schemas.translate import TranslateRequest
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/translate")
def translate(req: TranslateRequest):
    try:
        return {"translation": translate_text(req.query,  req.source_lang, req.dest_lang, req.words)}
    except OllamaError as exc:
        raise HTTPException(status_code=503, detail=str(exc))