from fastapi import FastAPI
from .api.order_route import router as order_router
from .core.db import Base, engine

app = FastAPI(title="Order Service")
app.include_router(order_router, prefix="/order")

Base.metadata.create_all(bind=engine)
