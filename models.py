from datetime import datetime
from sqlalchemy import String, func, DateTime, Boolean, Integer
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from enums import PromptType
from db import Base


class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, index=True, unique=True)
    known: Mapped[bool] = mapped_column(Boolean, default=False)
    times_used: Mapped[int] = mapped_column(Integer, default=0)
    last_used: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Prompt(Base):
    __tablename__ = "prompts"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[PromptType] = mapped_column(
        SAEnum(PromptType, native_enum=False, length=32,
               values_callable=lambda e: [m.value for m in e]),
        default=PromptType.USER,
    )
    text: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String(255), unique=True)