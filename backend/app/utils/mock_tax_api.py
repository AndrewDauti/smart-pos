from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import random
import string

# This is the mock server that pretends to be the ZRA/Tax Authority API.
# Your main application will send requests to this server.
app = FastAPI(
    title="Mock Tax Authority API",
    description="A fake server that mimics the real tax authority for development.",
    version="1.0.0",
)

@app.post("/")
async def mock_invoice_verification(request: Request):
    """
    This endpoint receives the invoice from your main POS API.
    It pretends to process it and then returns a successful response.
    """
    # We can print the invoice data we received to confirm everything is working.
    invoice_data = await request.json()
    print("--- Mock Tax API Received Invoice ---")
    print(invoice_data)
    print("-----------------------------------")

    # Generate a fake invoice ID to send back.
    fake_invoice_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    # This is the successful response structure your main API is expecting.
    response_data = {
        "status_code": 200,
        "message": "Invoice successfully received and verified by Mock API.",
        "invoice_id": f"ZRA-{fake_invoice_id}",
        "verification_code": "VC-" + ''.join(random.choices(string.digits, k=8)),
    }

    return JSONResponse(status_code=200, content=response_data)

@app.get("/")
def read_root():
    return {"message": "Mock Tax Authority API is running. Send POST requests to / to submit invoices."}