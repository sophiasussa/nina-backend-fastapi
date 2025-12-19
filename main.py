from fastapi import FastAPI
from app.database.session import engine
from app.database.base import Base
from app.models import user
from app.routes.auth_routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
