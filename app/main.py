from fastapi import FastAPI
from app.models import Base
from app.config import engine

from app.router.user_router import user_router
from app.router.lead_router import lead_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(lead_router, prefix="/api", tags=["Leads"])

@app.get("/api")
def homepage():
    return "Welcome to the Leads Manager"