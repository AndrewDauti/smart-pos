import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils.tax_client import submit_invoice

router = APIRouter(prefix="/invoices", tags=["invoices"])


def build_invoice_json(sale: models.Sale) -> dict[str, Any]:
    """Build a simplified ZRA-style tax invoice for the sale."""
    created = sale.created_at
    items = sale.items_json or []
    return {
        "Invoice": {
            "InvoiceNumber": f"INV-{sale.id:06d}",
            "InvoiceDate": created.strftime("%Y-%m-%d") if created else "",
            "InvoiceTime": created.strftime("%H:%M:%S") if created else "",
            "Currency": "ZMW",
            "Seller": {
                "TIN": os.getenv("BUSINESS_TIN", "1001234567"),
                "BusinessName": os.getenv("BUSINESS_NAME", "Mpepo Kitchen"),
                "Address": os.getenv("BUSINESS_ADDRESS", "Lusaka, Zambia"),
            },
            "Buyer": {
                "TIN": "N/A",
                "BusinessName": "Walk-in Customer",
                "Address": "N/A",
            },
            "LineItems": [
                {
                    "LineNumber": index + 1,
                    "ProductCode": item.get("sku"),
                    "Description": item.get("name"),
                    "Quantity": item.get("qty"),
                    "UnitPrice": item.get("price"),
                    "TaxRate": item.get("tax_rate"),
                    "TaxCategoryCode": "A" if (item.get("tax_rate") or 0) > 0 else "Z",
                    "NetAmount": item.get("line_subtotal"),
                    "TaxAmount": item.get("line_tax"),
                    "GrossAmount": item.get("line_total")
                    or ((item.get("line_subtotal") or 0) + (item.get("line_tax") or 0)),
                }
                for index, item in enumerate(items)
            ],
            "Totals": {
                "NetAmount": sum((item.get("line_subtotal") or 0) for item in items),
                "TaxAmount": sale.tax,
                "Discount": sale.discount,
                "GrossAmount": sale.total,
            },
        }
    }


def _record_submission(sale: models.Sale, payload: dict, external: dict, db: Session) -> models.InvoiceLog:
    status_text = "SUCCESS" if external.get("status_code") in (200, 201) else "FAILED"
    response_record = {
        "submitted_invoice": jsonable_encoder(payload.get("Invoice", payload)),
        "external_response": external if isinstance(external, dict) else {"raw": str(external)},
    }
    log = models.InvoiceLog(
        sale_id=sale.id,
        request_json=jsonable_encoder(payload),
        response_json=response_record,
        status=status_text,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.post("/submit", response_model=schemas.InvoiceLogRead)
@router.post("/submit/", response_model=schemas.InvoiceLogRead)
def submit_invoice_endpoint(body: schemas.InvoiceSubmission, db: Session = Depends(get_db)):
    sale = db.get(models.Sale, body.sale_id)
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

    already = (
        db.query(models.InvoiceLog)
        .filter_by(sale_id=sale.id, status="SUCCESS")
        .order_by(models.InvoiceLog.id.desc())
        .first()
    )
    if already:
        return already

    payload = build_invoice_json(sale)
    external = submit_invoice(payload)
    return _record_submission(sale, payload, external, db)
