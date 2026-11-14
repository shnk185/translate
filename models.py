from datetime import datetime
from sqlalchemy import String, func, DateTime, Boolean, Integer, UniqueConstraint
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

class Translation(Base):
    __tablename__ = "translations"
    id: Mapped[int] = mapped_column(primary_key=True)
    query: Mapped[str] = mapped_column(String, index=True)
    translation: Mapped[str] = mapped_column(String, index=True)
    source_lang: Mapped[str] = mapped_column(String, index=True)
    dest_lang: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class TranslationChunk(Base):
    __tablename__ = "translation_chunks"
    __table_args__ = (
        UniqueConstraint("translation_id", "sequence_number", name="uq_translation_sequence"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    translation_id: Mapped[int] = mapped_column(Integer)
    chunk_id: Mapped[int] = mapped_column(Integer)
    stored_meaning: Mapped[str] = mapped_column(String, index=True)
    sequence_number: Mapped[int] = mapped_column(Integer)
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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Preset(Base):
    __tablename__ = "presets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PresetConfig(Base):
    __tablename__ = "preset_configs"
    id: Mapped[int] = mapped_column(primary_key=True)
    preset_id: Mapped[int] = mapped_column(Integer)
    prompt_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Language(Base):
    __tablename__ = "languages"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())