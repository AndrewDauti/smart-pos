from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import products, invoices, reports, sales, auth

app = FastAPI(title="Smart POS API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(invoices.router)
app.include_router(reports.router)

@app.get("/health")
def health():
    return {"status": "ok"}
