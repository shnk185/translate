from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Prompt
from schemas.prompts import PromptRead, PromptCreate

router = APIRouter(prefix="/prompts", tags=["prompts"])

@router.post("", response_model=PromptRead)
def create_prompt(payload: PromptCreate, db: Session = Depends(get_db)):
    prompt = Prompt(name=payload.name, text=payload.text, type=payload.prompt_type)
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt