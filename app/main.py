from fastapi import FastAPI
from . import database
from .routers.router import router

app = FastAPI(title="Ecommerce API MongoDB")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "MongoDB Ecommerce API running"}