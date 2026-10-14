def _product(client, sku):
    products = client.get("/products").json()
    return next(item for item in products if item["sku"] == sku)


def test_health_and_seeded_menu(client):
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["products"] == 14
    drinks = [item for item in client.get("/products/").json() if item["category"] == "Drinks"]
    assert {item["name"] for item in drinks} >= {"Grape Juice", "Bottled Water"}


def test_register_page_is_served(client):
    page = client.get("/")
    assert page.status_code == 200
    assert "Mpepo Kitchen" in page.text
    assert "Take payment" in page.text


def test_login_checks_staff_credentials(client):
    refused = client.post("/auth/login", json={"username": "cashier", "password": "nope"})
    assert refused.status_code == 401
    accepted = client.post("/auth/login", json={"username": "cashier", "password": "mpepo"})
    assert accepted.status_code == 200
    assert accepted.json()["token_type"] == "bearer"


def test_sale_matches_documented_nshima_ticket(client):
    oreos = _product(client, "SKU-001")
    nshima = _product(client, "SKU-014")
    response = client.post("/sales/", json={
        "items": [
            {"product_id": oreos["id"], "qty": 2},
            {"product_id": nshima["id"], "qty": 1},
        ],
        "discount": 0,
    })
    assert response.status_code == 201
    sale = response.json()
    assert sale["tax"] == 12.0
    assert sale["total"] == 87.0
    assert len(sale["items_json"]) == 2


def test_discount_cannot_exceed_the_ticket(client):
    water = _product(client, "SKU-013")
    response = client.post("/sales", json={"items": [{"product_id": water["id"], "qty": 1}], "discount": 50})
    assert response.status_code == 400


def test_invoice_is_readable_and_not_submitted_twice(client):
    water = _product(client, "SKU-013")
    sale = client.post("/sales", json={"items": [{"product_id": water["id"], "qty": 2}], "discount": 0}).json()
    first = client.post("/invoices/submit", json={"sale_id": sale["id"]})
    assert first.status_code == 200
    body = first.json()
    invoice = body["response_json"]["submitted_invoice"]
    assert body["status"] == "SUCCESS"
    assert invoice["InvoiceNumber"] == f"INV-{sale['id']:06d}"
    assert invoice["Seller"]["BusinessName"] == "Mpepo Kitchen"
    assert invoice["LineItems"][0]["Description"] == "Bottled Water"
    assert invoice["Totals"]["GrossAmount"] == 20.0
    assert body["response_json"]["external_response"]["body"]["verification_code"].startswith("VC-")

    second = client.post("/invoices/submit/", json={"sale_id": sale["id"]})
    assert second.status_code == 200
    assert second.json()["id"] == body["id"]


def test_failed_fiscalization_keeps_the_sale(client, monkeypatch):
    monkeypatch.setenv("MOCK_EINVOICE_URL", "http://127.0.0.1:9/einvoice")
    wings = _product(client, "SKU-005")
    sale = client.post("/sales", json={"items": [{"product_id": wings["id"], "qty": 1}]}).json()
    assert sale["total"] == 126.56
    log = client.post("/invoices/submit", json={"sale_id": sale["id"]})
    assert log.status_code == 200
    assert log.json()["status"] == "FAILED"
    assert log.json()["response_json"]["submitted_invoice"]["InvoiceNumber"] == f"INV-{sale['id']:06d}"


def test_unknown_product_is_rejected(client):
    response = client.post("/sales", json={"items": [{"product_id": 99999, "qty": 1}]})
    assert response.status_code == 400
