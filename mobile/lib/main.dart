import 'package:flutter/material.dart';
import 'screens/products_screen.dart';

void main() {
  runApp(const SmartPOSApp());
}

class SmartPOSApp extends StatelessWidget {
  const SmartPOSApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart POS',
      theme: ThemeData(useMaterial3: true),
      home: const ProductsScreen(),
    );
  }
}


