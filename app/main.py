from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.accounts import router as accounts_router
from app.api.orders import router as orders_router 
from app.api.instruments import router as instruments_router 

app = FastAPI(title="DevSecOps Trading Platform Lab")

app.include_router(health_router, prefix="/api")
app.include_router(accounts_router, prefix="/api")
app.include_router(orders_router, prefix="/api")  
app.include_router(instruments_router, prefix="/api")