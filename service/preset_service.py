from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Preset


def get_available_presets(db: Session):
    return db.execute(
        select(Preset.id, Preset.name)
        .order_by(Preset.id)
    ).mappings().all()