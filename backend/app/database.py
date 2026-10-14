from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")

DEFAULT_DB = BACKEND_DIR / "pos.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_compat() -> None:
    """Add columns introduced after the original SQL seed, without dropping data."""
    if not DATABASE_URL.startswith("sqlite"):
        return
    additions = {
        "products": {"category": "TEXT NOT NULL DEFAULT 'Plates'"},
        "sales": {"items_json": "TEXT"},
    }
    with engine.begin() as conn:
        for table, columns in additions.items():
            existing = conn.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")).first()
            if not existing:
                continue
            present = {row[1] for row in conn.execute(text(f"PRAGMA table_info({table})"))}
            for name, ddl in columns.items():
                if name not in present:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))
