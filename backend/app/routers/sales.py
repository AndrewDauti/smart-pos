from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=schemas.SaleRead, status_code=201)
def create_sale(body: schemas.SaleCreate, db: Session = Depends(get_db)):
    # fetch products + compute totals
    items = []
    subtotal = 0.0
    tax_total = 0.0
    for it in body.items:
        p = db.query(models.Product).get(it.product_id)
        if not p:
            raise HTTPException(status_code=400, detail=f"Product {it.product_id} not found")
        line_sub = p.price * it.qty
        line_tax = (p.tax_rate / 100.0) * line_sub
        items.append({"product_id": p.id, "sku": p.sku, "name": p.name, "qty": it.qty, "price": p.price, "tax_rate": p.tax_rate, "line_subtotal": line_sub, "line_tax": line_tax})
        subtotal += line_sub
        tax_total += line_tax
    total = max(0.0, subtotal + tax_total - body.discount)
    sale = models.Sale(total=total, tax=tax_total, discount=body.discount, items_json=items)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale
