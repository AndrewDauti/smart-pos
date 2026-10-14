-- Optional manual seed. The API also loads this menu on startup when products is empty.
INSERT INTO products (sku, name, category, price, tax_rate) VALUES
('SKU-001','Oreos','Starters',15.00,16.0),
('SKU-002','Grape Juice','Drinks',30.00,16.0),
('SKU-003','Cranberry Juice','Drinks',30.00,16.0),
('SKU-004','Orange Juice','Drinks',32.00,16.0),
('SKU-005','Crispy Chicken Wings (6 pc.)','Starters',113.00,12.0),
('SKU-006','Fried Mozzarella Sticks (6 pc.)','Starters',120.00,12.0),
('SKU-007','Grilled Steak and Wedges','Plates',120.00,12.0),
('SKU-008','Double Patty Cheese Burger','Plates',180.00,12.0),
('SKU-009','Large Cheese Burger','Plates',200.00,12.0),
('SKU-010','Nshima with T-bone','Plates',160.00,12.0),
('SKU-011','Nshima with Fish','Plates',165.00,12.0),
('SKU-012','Nshima with Chicken','Plates',165.00,12.0),
('SKU-013','Bottled Water','Drinks',10.00,0.0),
('SKU-014','Nshima Plate','Plates',45.00,16.0);
