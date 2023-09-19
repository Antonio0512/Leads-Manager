from fastapi import FastAPI
from app.models import Base
from app.config import engine

from app.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/api", tags=["Users"])
