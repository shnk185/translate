from click import pause
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from schemas.chunk import ChunkKnown
from service.chunk_service import update_chunk_known

router = APIRouter(prefix="/chunks", tags=["chunks"])

@router.post("/known")
def update_known(payload: ChunkKnown, db: Session = Depends(get_db)):
    update_chunk_known(payload, db)
    db.commit()
    return ""

