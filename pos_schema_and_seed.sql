
PRAGMA foreign_keys = ON;

-- ========== SCHEMA ==========

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    tax_rate REAL NOT NULL DEFAULT 0, -- percentage, e.g. 16.0 for 16%
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sales table (summary per sale)
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    total REAL NOT NULL CHECK(total >= 0),
    tax REAL NOT NULL DEFAULT 0,
    discount REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'ZMW'
);

-- Sale items (normalized lines)
CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    product_id INTEGER,
    sku TEXT, -- denormalized for audit
    name TEXT,
    qty INTEGER NOT NULL CHECK(qty > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    tax_rate REAL NOT NULL DEFAULT 0,
    line_subtotal REAL NOT NULL, -- qty * unit_price before tax
    line_tax REAL NOT NULL,
    line_total REAL NOT NULL, -- line_subtotal + line_tax
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- Invoice logs (store what was submitted and the external response)
CREATE TABLE IF NOT EXISTS invoice_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    request_json TEXT, -- stored invoice payload submitted to tax endpoint
    response_json TEXT, -- response returned by external system (or error record)
    status TEXT NOT NULL, -- e.g. SUCCESS, FAILED
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sales_created_at ON sales(created_at);
CREATE INDEX IF NOT EXISTS idx_invoice_logs_sale_id ON invoice_logs(sale_id);
CREATE INDEX IF NOT EXISTS idx_sale_items_sale_id ON sale_items(sale_id);

-- ========== SEED DATA ==========

-- Products (sample set used in the app)
INSERT INTO products (sku, name, price, tax_rate) VALUES
('SKU-001','Oreos',15.00,16.0),
('SKU-002','Grape Juice',30.00,16.0),
('SKU-003','Cranberry Juice',30.00,16.0),
('SKU-004','Orange Juice',32.00,16.0),
('SKU-005','Crispy Chicken Wings (6 pc.)',113.00,12.0),
('SKU-006','Fried Mozzarella Sticks (6 pc.)',120.00,12.0),
('SKU-007','Grilled Steak and Wedges',120.00,12.0),
('SKU-008','Double Patty Cheese Burger',180.00,12.0),
('SKU-009','Large Cheese Burger',200.00,12.0),
('SKU-010','Nshima with T-bone',160.00,12.0),
('SKU-011','Nshima with Fish',165.00,12.0),
('SKU-012','Nshima with Chicken',165.00,12.0),
('SKU-013','Bottled Water',10.00,0.0),
('SKU-014','Nshima Plate',45.00,16.0);

-- Single sample sale with two items (demonstrates calculations)
-- Items: Oreos x2 (15.00 each, 16% tax), Nshima Plate x1 (45.00, 16% tax)
INSERT INTO sales (created_at, total, tax, discount, currency) VALUES
('2025-09-24 12:00:00', 87.00, 12.00, 0.00, 'ZMW');

-- Determine the sale_id inserted (SQLite AUTOINCREMENT gives id=1 if DB empty)
-- For compatibility when importing, assume this is sale id 1. If not, adjust accordingly.
INSERT INTO sale_items (sale_id, product_id, sku, name, qty, unit_price, tax_rate, line_subtotal, line_tax, line_total) VALUES
(1, (SELECT id FROM products WHERE sku='SKU-001'), 'SKU-001', 'Oreos', 2, 15.00, 16.0, 30.00, 4.80, 34.80),
(1, (SELECT id FROM products WHERE sku='SKU-014'), 'SKU-014', 'Nshima Plate', 1, 45.00, 16.0, 45.00, 7.20, 52.20);

-- Example invoice log for that sale (the request_json contains the simplified invoice we would have submitted)
INSERT INTO invoice_logs (sale_id, request_json, response_json, status) VALUES
(1,
'{"Invoice":{"InvoiceNumber":"INV-000001","InvoiceDate":"2025-09-24","InvoiceTime":"12:00:00","Currency":"ZMW","Seller":{"TIN":"1001234567","BusinessName":"Mpepo Kitchen","Address":"Lusaka"},"Buyer":{"TIN":"N/A","BusinessName":"Walk-in Customer","Address":"N/A"},"LineItems":[{"LineNumber":1,"ProductCode":"SKU-001","Description":"Oreos","Quantity":2,"UnitPrice":15.0,"TaxRate":16.0,"TaxCategoryCode":"A","NetAmount":30.0,"TaxAmount":4.8,"GrossAmount":34.8},{"LineNumber":2,"ProductCode":"SKU-014","Description":"Nshima Plate","Quantity":1,"UnitPrice":45.0,"TaxRate":16.0,"TaxCategoryCode":"A","NetAmount":45.0,"TaxAmount":7.2,"GrossAmount":52.2}],"Totals":{"NetAmount":75.0,"TaxAmount":12.0,"Discount":0.0,"GrossAmount":87.0}}}',
'{"submitted_invoice":{"InvoiceNumber":"INV-000001","InvoiceDate":"2025-09-24"},"external_response":{"status_code":200,"body":{"Result":"Success","InvoiceNumber":"INV-000001","verification_code":"ABC123XYZ"}}}',
'SUCCESS');

-- ========== END OF FILE ==========