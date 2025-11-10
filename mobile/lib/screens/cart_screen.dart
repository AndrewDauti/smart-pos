import 'package:flutter/material.dart';
import '../services/api.dart';
import '../services/offline_queue.dart';
import 'receipt_screen.dart';

class CartScreen extends StatefulWidget {
  final List<Map<String, dynamic>> items;
  const CartScreen({super.key, required this.items});

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  double discount = 0;

  double get subtotal {
    return widget.items.fold(0, (sum, item) => sum + (item['price'] * item['qty']));
  }

  Future<void> _checkout() async {
    try {
      final sale = await Api.createSale(
        widget.items
            .map((e) => {'product_id': e['product_id'], 'qty': e['qty']})
            .toList(),
        discount: discount,
      );
      final log = await Api.submitInvoice(sale['id']);
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => ReceiptScreen(sale: sale, invoiceLog: log)),
      );
    } catch (_) {
      await OfflineQueue.addPendingSale(
          {'items': widget.items, 'discount': discount});
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No network. Sale queued.')),
      );
      Navigator.pop(context);
    }
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Cart')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: ListView.separated(
                itemCount: widget.items.length,
                separatorBuilder: (_, __) => const Divider(),
                itemBuilder: (context, i) {
                  final item = widget.items[i];
                  final lineTotal = item['price'] * item['qty'];
                  return ListTile(
                    title: Text(item['name']),
                    subtitle: Text(
                        'K${item['price'].toStringAsFixed(2)} × ${item['qty']}'),
                    trailing: Text(
                      'K${lineTotal.toStringAsFixed(2)}',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 12),
            Align(
              alignment: Alignment.centerRight,
              child: Text(
                'Subtotal: K${subtotal.toStringAsFixed(2)}',
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              decoration: const InputDecoration(labelText: 'Discount (K)'),
              keyboardType: TextInputType.number,
              onChanged: (v) => setState(() => discount = double.tryParse(v) ?? 0),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _checkout,
              icon: const Icon(Icons.check),
              label: const Text('Checkout'),
            ),
          ],
        ),
      ),
    );
  }
}

