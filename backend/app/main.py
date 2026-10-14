from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import models
from .database import Base, SessionLocal, engine, ensure_compat
from .routers import auth, invoices, products, reports, sales
from .seed import seed_if_empty

app = FastAPI(title="Smart POS API", version="1.1.0", redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
ensure_compat()
with SessionLocal() as db:
    seed_if_empty(db)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(invoices.router)
app.include_router(reports.router)

STATIC_DIR = Path(__file__).resolve().parent / "static"


@app.get("/health")
def health():
    with SessionLocal() as db:
        product_count = db.query(models.Product).count()
    return {"status": "ok", "products": product_count}


@app.get("/")
def register():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/menu", StaticFiles(directory=STATIC_DIR / "menu"), name="menu")
