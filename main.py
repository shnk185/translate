from fastapi import FastAPI
from api.translate import router as translate_router

app = FastAPI()
app.include_router(translate_router)