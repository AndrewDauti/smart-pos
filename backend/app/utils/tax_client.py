import os, requests

MOCK_URL = os.getenv("MOCK_EINVOICE_URL", "https://postman-echo.com/post")

def submit_invoice(payload: dict) -> dict:
    # In real life, include auth headers and robust error handling
    try:
        r = requests.post(MOCK_URL, json=payload, timeout=10)
        return {"status_code": r.status_code, "body": r.json() if r.headers.get("content-type","").startswith("application/json") else r.text}
    except Exception as e:
        return {"status_code": 0, "error": str(e)}
