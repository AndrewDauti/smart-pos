import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import '../services/api.dart';

class OfflineQueue {
  static const _key = 'pending_sales';

  static Future<void> addPendingSale(Map<String, dynamic> saleBody) async {
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList(_key) ?? [];
    list.add(jsonEncode(saleBody));
    await prefs.setStringList(_key, list);
  }

  static Future<int> retryAll() async {
    final prefs = await SharedPreferences.getInstance();
    var list = prefs.getStringList(_key) ?? [];
    int success = 0;
    final conn = await Connectivity().checkConnectivity();
    if (conn.contains(ConnectivityResult.none)) return 0;

    final remaining = <String>[];
    for (final item in list) {
      final body = jsonDecode(item);
      try {
        final sale = await Api.createSale(List<Map<String,dynamic>>.from(body['items']), discount: body['discount'] ?? 0);
        await Api.submitInvoice(sale['id']);
        success += 1;
      } catch (_) {
        remaining.add(item);
      }
    }
    await prefs.setStringList(_key, remaining);
    return success;
  }
}
