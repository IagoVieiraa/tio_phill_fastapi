from fastapi import FastAPI
from .api.menu_route import router as menu_router
from .core.db import Base, engine

app = FastAPI(title="Menu Service")
app.include_router(menu_router, prefix="/menu")

Base.metadata.create_all(bind=engine)
