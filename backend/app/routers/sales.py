from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..money import money

router = APIRouter(prefix="/sales", tags=["sales"])


def _line(product: models.Product, qty: int) -> dict:
    net = Decimal(str(product.price)) * Decimal(qty)
    tax = net * Decimal(str(product.tax_rate)) / Decimal(100)
    line_subtotal = money(net)
    line_tax = money(tax)
    return {
        "product_id": product.id,
        "sku": product.sku,
        "name": product.name,
        "category": product.category,
        "qty": qty,
        "price": money(product.price),
        "tax_rate": money(product.tax_rate),
        "line_subtotal": line_subtotal,
        "line_tax": line_tax,
        "line_total": money(line_subtotal + line_tax),
    }


@router.post("", response_model=schemas.SaleRead, status_code=201)
@router.post("/", response_model=schemas.SaleRead, status_code=201)
def create_sale(body: schemas.SaleCreate, db: Session = Depends(get_db)):
    items = []
    subtotal = 0.0
    tax_total = 0.0
    for it in body.items:
        product = db.get(models.Product, it.product_id)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {it.product_id} not found")
        line = _line(product, it.qty)
        items.append(line)
        subtotal = money(subtotal + line["line_subtotal"])
        tax_total = money(tax_total + line["line_tax"])

    gross = money(subtotal + tax_total)
    discount = money(body.discount)
    if discount > gross:
        raise HTTPException(status_code=400, detail="Discount is larger than the order total")

    sale = models.Sale(
        total=money(gross - discount),
        tax=tax_total,
        discount=discount,
        items_json=items,
    )
    db.add(sale)
    db.flush()
    for line in items:
        db.add(
            models.SaleItem(
                sale_id=sale.id,
                product_id=line["product_id"],
                sku=line["sku"],
                name=line["name"],
                qty=line["qty"],
                unit_price=line["price"],
                tax_rate=line["tax_rate"],
                line_subtotal=line["line_subtotal"],
                line_tax=line["line_tax"],
                line_total=line["line_total"],
            )
        )
    db.commit()
    db.refresh(sale)
    return sale
