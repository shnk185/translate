from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Language


def get_available_languages(db: Session):
    return list(db.execute(
        select(Language.name)
        .order_by(Language.name)
    ).scalars())