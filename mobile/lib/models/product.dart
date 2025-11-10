class Product {
  final int id;
  final String sku;
  final String name;
  final double price;
  final double taxRate;

  Product({required this.id, required this.sku, required this.name, required this.price, required this.taxRate});

  factory Product.fromJson(Map<String, dynamic> j) => Product(
    id: j['id'],
    sku: j['sku'],
    name: j['name'],
    price: (j['price'] as num).toDouble(),
    taxRate: (j['tax_rate'] as num).toDouble(),
  );
}
