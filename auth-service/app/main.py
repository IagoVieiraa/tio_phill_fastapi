from fastapi import FastAPI
from .api.user_route import router as auth_router
from .core.db import Base, engine

app = FastAPI(title="Auth Service")
app.include_router(auth_router, prefix="/auth")

Base.metadata.create_all(bind=engine)
