import 'dart:convert';
import 'package:http/http.dart' as http;

class Api {
  // Emulator to host machine mapping
  static String baseUrl = 'http://10.0.2.2:8000';

  static Future<List<dynamic>> listProducts() async {
    final res = await http.get(Uri.parse('$baseUrl/products/'));
    if (res.statusCode == 200) {
      return jsonDecode(res.body);
    } else {
      throw Exception('Failed to load products');
    }
  }

  static Future<Map<String, dynamic>> createSale(List<Map<String,dynamic>> items, {double discount = 0}) async {
    final res = await http.post(Uri.parse('$baseUrl/sales/'),
        headers: {'Content-Type':'application/json'},
        body: jsonEncode({'items': items, 'discount': discount}));
    if (res.statusCode == 201) {
      return jsonDecode(res.body);
    } else {
      throw Exception('Failed to create sale');
    }
  }

  static Future<Map<String, dynamic>> submitInvoice(int saleId) async {
    final res = await http.post(Uri.parse('$baseUrl/invoices/submit'),
        headers: {'Content-Type':'application/json'},
        body: jsonEncode({'sale_id': saleId}));
    if (res.statusCode == 200) {
      return jsonDecode(res.body);
    } else {
      throw Exception('Failed to submit invoice');
    }
  }
}



