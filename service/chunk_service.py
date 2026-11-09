from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models import Chunk


def upsert_chunks(db: Session, words: list[str]) -> None:
    unique = list(dict.fromkeys(w.strip() for w in words if w.strip()))
    if not unique:
        return

    stmt = insert(Chunk).values([{"text": w} for w in unique])
    stmt = stmt.on_conflict_do_update(
        index_elements=[Chunk.text],
        set_={
            "times_used": Chunk.times_used + 1,
            "last_used": func.now(),
        },
    )
    db.execute(stmt)
    db.flush()