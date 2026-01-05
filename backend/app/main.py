from fastapi import FastAPI
from app.api import router as api_router

from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Farming Management Platform",
    version="0.1.0"
)

app.include_router(api_router)
