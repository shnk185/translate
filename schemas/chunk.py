from pydantic import BaseModel, Field

class ChunkStatus(BaseModel):
    id: int
    status: bool

class ChunkKnown(BaseModel):
    chunks: list[ChunkStatus]