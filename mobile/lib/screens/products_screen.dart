import 'package:flutter/material.dart';
import '../services/api.dart';
import '../models/product.dart';
import 'cart_screen.dart';

class ProductsScreen extends StatefulWidget {
  const ProductsScreen({super.key});
  @override
  State<ProductsScreen> createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  List<Product> products = [];
  Map<int,int> cart = {};

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final list = await Api.listProducts();
    setState(() {
      products = list.map<Product>((j) => Product.fromJson(j)).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mpepo Kitchen - POS')),
      body: ListView.builder(
        itemCount: products.length,
        itemBuilder: (_, i) {
          final p = products[i];
          return ListTile(
            title: Text(p.name),
            subtitle: Text('K ${p.price.toStringAsFixed(2)} • Tax ${p.taxRate}%'),
            trailing: Row(mainAxisSize: MainAxisSize.min, children: [
              IconButton(icon: const Icon(Icons.remove_circle_outline), onPressed: (){
                setState(() => cart[p.id] = (cart[p.id] ?? 0) > 0 ? (cart[p.id]! - 1) : 0);
              }),
              Text('${cart[p.id] ?? 0}'),
              IconButton(icon: const Icon(Icons.add_circle_outline), onPressed: (){
                setState(() => cart[p.id] = (cart[p.id] ?? 0) + 1);
              }),
            ]),
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          final items = cart.entries
              .where((e) => e.value > 0)
              .map((e) {
            final product = products.firstWhere((p) => p.id == e.key);
            return {
              'product_id': product.id,
              'name': product.name,
              'price': product.price,
              'qty': e.value,
            };
          })
              .toList();

          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => CartScreen(items: items),
            ),
          );
        },
        label: const Text('View Cart'),
        icon: const Icon(Icons.shopping_cart),
      ),
    );
  }
}



