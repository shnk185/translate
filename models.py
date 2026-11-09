from datetime import datetime
from sqlalchemy import String, func, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, index=True, unique=True)
    known: Mapped[bool] = mapped_column(Boolean, default=False)
    times_used: Mapped[int] = mapped_column(Integer, default=0)
    last_used: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
