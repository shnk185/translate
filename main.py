from contextlib import asynccontextmanager
from db import Base, engine
from fastapi import FastAPI
from api.translate import router as translate_router
from api.prompts import router as prompt_router
from api.chunks import router as chunks_router
from api.presets import router as preset_router

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield
app = FastAPI()
app.include_router(translate_router, prefix="/api")
app.include_router(prompt_router, prefix="/api")
app.include_router(chunks_router, prefix="/api")
app.include_router(preset_router, prefix="/api")
