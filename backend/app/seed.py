from sqlalchemy.orm import Session

from . import models

# Menu shared with pos_schema_and_seed.sql. Prices are tax-exclusive, in ZMW.
MENU = [
    {"sku": "SKU-001", "name": "Oreos", "category": "Starters", "price": 15.00, "tax_rate": 16.0},
    {"sku": "SKU-002", "name": "Grape Juice", "category": "Drinks", "price": 30.00, "tax_rate": 16.0},
    {"sku": "SKU-003", "name": "Cranberry Juice", "category": "Drinks", "price": 30.00, "tax_rate": 16.0},
    {"sku": "SKU-004", "name": "Orange Juice", "category": "Drinks", "price": 32.00, "tax_rate": 16.0},
    {"sku": "SKU-005", "name": "Crispy Chicken Wings (6 pc.)", "category": "Starters", "price": 113.00, "tax_rate": 12.0},
    {"sku": "SKU-006", "name": "Fried Mozzarella Sticks (6 pc.)", "category": "Starters", "price": 120.00, "tax_rate": 12.0},
    {"sku": "SKU-007", "name": "Grilled Steak and Wedges", "category": "Plates", "price": 120.00, "tax_rate": 12.0},
    {"sku": "SKU-008", "name": "Double Patty Cheese Burger", "category": "Plates", "price": 180.00, "tax_rate": 12.0},
    {"sku": "SKU-009", "name": "Large Cheese Burger", "category": "Plates", "price": 200.00, "tax_rate": 12.0},
    {"sku": "SKU-010", "name": "Nshima with T-bone", "category": "Plates", "price": 160.00, "tax_rate": 12.0},
    {"sku": "SKU-011", "name": "Nshima with Fish", "category": "Plates", "price": 165.00, "tax_rate": 12.0},
    {"sku": "SKU-012", "name": "Nshima with Chicken", "category": "Plates", "price": 165.00, "tax_rate": 12.0},
    {"sku": "SKU-013", "name": "Bottled Water", "category": "Drinks", "price": 10.00, "tax_rate": 0.0},
    {"sku": "SKU-014", "name": "Nshima Plate", "category": "Plates", "price": 45.00, "tax_rate": 16.0},
]


def seed_if_empty(db: Session) -> None:
    if db.query(models.Product).first():
        backfill_categories(db)
        return
    for row in MENU:
        db.add(models.Product(**row))
    db.commit()


def backfill_categories(db: Session) -> None:
    """Older SQL seeds stored every item as a plate. Restore the known menu groups."""
    expected = {row["sku"]: row["category"] for row in MENU}
    changed = False
    for product in db.query(models.Product).all():
        category = expected.get(product.sku)
        if category and category != "Plates" and product.category in (None, "", "Plates", "General"):
            product.category = category
            changed = True
    if changed:
        db.commit()
