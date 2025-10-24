from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import fields, users
from app.core.config import get_settings
from app.db.database import engine, Base

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME)

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(fields.router, prefix=f"{settings.API_PREFIX}")
app.include_router(users.router, prefix=f"{settings.API_PREFIX}")

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API des terrains de Montréal!"}
