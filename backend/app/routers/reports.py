from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/daily-sales")
def daily_sales(db: Session = Depends(get_db)):
    rows = (
        db.query(
            func.date(models.Sale.created_at).label("date"),
            func.sum(models.Sale.total).label("total"),
            func.count(models.Sale.id).label("sales"),
        )
        .group_by(func.date(models.Sale.created_at))
        .order_by(func.date(models.Sale.created_at).desc())
        .all()
    )
    return [{"date": str(r[0]), "total": round(float(r[1] or 0), 2), "sales": int(r[2] or 0)} for r in rows]

@router.get("/tax-summary")
def tax_summary(db: Session = Depends(get_db)):
    rows = (
        db.query(func.date(models.Sale.created_at).label("date"), func.sum(models.Sale.tax).label("tax"))
        .group_by(func.date(models.Sale.created_at))
        .order_by(func.date(models.Sale.created_at).desc())
        .all()
    )
    return [{"date": str(r[0]), "tax": round(float(r[1] or 0), 2)} for r in rows]
