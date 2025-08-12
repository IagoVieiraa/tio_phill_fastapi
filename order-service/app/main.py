from fastapi import FastAPI
from .api.order_route import router as order_router

app = FastAPI(title="Order Service")
app.include_router(order_router, prefix="/order")
