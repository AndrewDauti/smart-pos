import os
import random
import string

import requests

# The sample env file used to point at example.com, which cannot fiscalize.
_PLACEHOLDER_URLS = {
    "",
    "https://example.com/mock/einvoice",
    "http://example.com/mock/einvoice",
}


def submit_invoice(payload: dict) -> dict:
    url = os.getenv("MOCK_EINVOICE_URL", "").strip()
    if url in _PLACEHOLDER_URLS:
        return _local_acceptance(payload)
    try:
        response = requests.post(url, json=payload, timeout=10)
        content_type = response.headers.get("content-type", "")
        body = response.json() if content_type.startswith("application/json") else response.text
        return {"status_code": response.status_code, "body": body}
    except Exception as exc:
        return {"status_code": 0, "error": str(exc)}


def _local_acceptance(payload: dict) -> dict:
    invoice = payload.get("Invoice", {})
    serial = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    verification = "VC-" + "".join(random.choices(string.digits, k=8))
    return {
        "status_code": 200,
        "body": {
            "Result": "Success",
            "message": "Invoice accepted by the Mpepo Kitchen Smart Invoice sandbox.",
            "InvoiceNumber": invoice.get("InvoiceNumber"),
            "invoice_id": f"ZRA-{serial}",
            "verification_code": verification,
        },
    }
