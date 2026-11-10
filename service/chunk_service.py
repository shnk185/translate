from sqlalchemy import func, bindparam, update
from sqlalchemy.orm import Session

from models import Chunk
from schemas.chunk import ChunkKnown


def update_chunk_known(chunk_known: ChunkKnown, db: Session):
    values = [{"cid": c.id, "known": c.status} for c in chunk_known.chunks]
    if not values:
        return ""

    stmt = (
        update(Chunk)
        .where(Chunk.id == bindparam("cid"))
        .values(known=bindparam("known"))
    )
    db.connection().execute(stmt, values)
    db.flush()
    return ""