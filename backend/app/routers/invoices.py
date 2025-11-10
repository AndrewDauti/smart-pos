from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..utils.tax_client import submit_invoice
from typing import Dict, Any

router = APIRouter(prefix="/invoices", tags=["invoices"])


def build_invoice_json(sale: models.Sale) -> Dict[str, Any]:
    """
    Build invoice JSON according to ZRA Smart Invoice (Tax Invoice) structure.
    This is simplified for demo purposes — in production you'd map fields exactly
    to ZRA's published e-invoicing JSON schema.
    """
    return {
        "Invoice": {
            "InvoiceNumber": f"INV-{sale.id:06d}",
            "InvoiceDate": sale.created_at.strftime("%Y-%m-%d"),
            "InvoiceTime": sale.created_at.strftime("%H:%M:%S"),
            "Currency": "ZMW",
            "Seller": {
                "TIN": "1001234567",
                "BusinessName": "Smart POS Demo Ltd",
                "Address": "Lusaka, Zambia",
            },
            "Buyer": {
                # If your sale does not contain buyer info, keep it as N/A / walk-in
                "TIN": getattr(sale, "buyer_tin", "") or "N/A",
                "BusinessName": getattr(sale, "buyer_name", "") or "Walk-in Customer",
                "Address": getattr(sale, "buyer_address", "") or "N/A",
            },
            "LineItems": [
                {
                    "LineNumber": i + 1,
                    "ProductCode": item.get("sku"),
                    "Description": item.get("name"),
                    "Quantity": item.get("qty"),
                    "UnitPrice": item.get("price"),
                    "TaxRate": item.get("tax_rate"),
                    "TaxCategoryCode": "A" if (item.get("tax_rate") or 0) > 0 else "Z",
                    "NetAmount": item.get("line_subtotal"),
                    "TaxAmount": item.get("line_tax"),
                    "GrossAmount": (item.get("line_subtotal") or 0) + (item.get("line_tax") or 0),
                }
                for i, item in enumerate(sale.items_json)
            ],
            "Totals": {
                "NetAmount": sum((i.get("line_subtotal") or 0) for i in sale.items_json),
                "TaxAmount": sale.tax,
                "Discount": sale.discount,
                "GrossAmount": sale.total,
            },
        }
    }


@router.post("/submit", response_model=schemas.InvoiceLogRead)
def submit_invoice_endpoint(body: schemas.InvoiceSubmission, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).get(body.sale_id)
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

    payload = build_invoice_json(sale)

    try:
        resp = submit_invoice(payload)  # returns dict like {"status_code":200, "body": {...}} or error dict
    except Exception as exc:
        log = models.InvoiceLog(
            sale_id=sale.id,
            request_json=jsonable_encoder(payload),
            response_json={"error": str(exc)},
            status="FAILED",
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Invoice submission failed: {str(exc)}")

    # Normalize response_json to include original invoice payload + external response
    try:
        external = resp if isinstance(resp, dict) else {"raw": str(resp)}
        response_record = {
            "submitted_invoice": jsonable_encoder(payload.get("Invoice", payload)),  # include invoice payload under this key
            "external_response": external
        }
    except Exception:
        response_record = {"submitted_invoice": payload.get("Invoice", payload), "external_response": str(resp)}

    status_text = "SUCCESS" if external.get("status_code") in (200, 201) else "FAILED"

    log = models.InvoiceLog(
        sale_id=sale.id,
        request_json=jsonable_encoder(payload),
        response_json=response_record,
        status=status_text,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    if status_text != "SUCCESS":
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail={"status": status_text, "response": response_record})

    return log



# alias route to be tolerant of trailing slash (accept both /submit and /submit/)
@router.post("/submit/")
def submit_invoice_endpoint_slash(body: schemas.InvoiceSubmission, db: Session = Depends(get_db)):
    return submit_invoice_endpoint(body, db)

