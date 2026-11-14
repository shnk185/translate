from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Preset, PresetConfig
from schemas.presets import PresetCreate, PresetResponse, FetchPresetsResponse
from service.preset_service import get_available_presets

router = APIRouter(prefix="/presets", tags=["presets"])

@router.post("", response_model=PresetResponse)
def create_preset(payload: PresetCreate, db: Session = Depends(get_db)):
    preset = Preset(name=payload.name)
    db.add(preset)
    db.flush()
    for prompt_id in payload.prompt_ids:
        preset_config = PresetConfig(preset_id=preset.id, prompt_id=prompt_id)
        db.add(preset_config)
    db.commit()
    db.refresh(preset)
    return {"id": preset.id, "name": preset.name, "prompt_ids": payload.prompt_ids}

@router.get("", response_model=FetchPresetsResponse)
def fetch_presets(db: Session = Depends(get_db)):
    presets = get_available_presets(db)
    print(presets)
    return FetchPresetsResponse(presets = presets)