import 'package:flutter/material.dart';

class ReceiptScreen extends StatelessWidget {
  final Map<String,dynamic> sale;
  final Map<String,dynamic> invoiceLog;
  const ReceiptScreen({super.key, required this.sale, required this.invoiceLog});

  @override
  Widget build(BuildContext context) {
    // Pull out ZRA invoice fields
    final invoice = invoiceLog['response_json']?['body']?['Invoice'] ?? {};
    final seller = invoice['Seller'] ?? {};
    final buyer  = invoice['Buyer'] ?? {};
    final totals = invoice['Totals'] ?? {};

    return Scaffold(
      appBar: AppBar(title: const Text('Receipt / Tax Invoice')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            Text('INVOICE NUMBER: ${invoice['InvoiceNumber'] ?? ''}',
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('DATE: ${invoice['InvoiceDate'] ?? ''}   TIME: ${invoice['InvoiceTime'] ?? ''}'),
            const Divider(),

            Text('SELLER', style: const TextStyle(fontWeight: FontWeight.bold)),
            Text('TIN: ${seller['TIN'] ?? ''}'),
            Text('Name: ${seller['BusinessName'] ?? ''}'),
            Text('Address: ${seller['Address'] ?? ''}'),
            const SizedBox(height: 12),

            Text('BUYER', style: const TextStyle(fontWeight: FontWeight.bold)),
            Text('TIN: ${buyer['TIN'] ?? ''}'),
            Text('Name: ${buyer['BusinessName'] ?? ''}'),
            Text('Address: ${buyer['Address'] ?? ''}'),
            const Divider(),

            Text('LINE ITEMS', style: const TextStyle(fontWeight: FontWeight.bold)),
            ...(invoice['LineItems'] as List? ?? []).map((item) {
              return ListTile(
                title: Text(item['Description']),
                subtitle: Text(
                    'Qty: ${item['Quantity']} × K${item['UnitPrice']} • Tax ${item['TaxRate']}% (${item['TaxCategoryCode']})'
                ),
                trailing: Text(
                  'K${item['GrossAmount']}',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              );
            }).toList(),
            const Divider(),

            Text('TOTALS', style: const TextStyle(fontWeight: FontWeight.bold)),
            Text('Net: K${totals['NetAmount']}'),
            Text('Tax: K${totals['TaxAmount']}'),
            Text('Discount: K${totals['Discount']}'),
            Text('Gross: K${totals['GrossAmount']}',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            const Divider(),

            Text('STATUS: ${invoiceLog['status'] ?? ''}',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: invoiceLog['status'] == 'SUCCESS' ? Colors.green : Colors.red,
                )),
          ],
        ),
      ),
    );
  }
}

