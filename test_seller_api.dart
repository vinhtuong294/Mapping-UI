import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final baseUrl = 'http://207.180.233.84:8000/api';
  final token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJOREZCQjciLCJ1c2VyX2lkIjoiTkRGQkI3Iiwicm9sZSI6Im5ndW9pX2JhbiIsImxvZ2luX25hbWUiOiJoaWV1bmd1b2liYW4iLCJ1c2VyX25hbWUiOiJOZ3V5XHUxZWM1biBWXHUwMTAzbiBIaVx1MWViZnUiLCJleHAiOjE3NzM5NTI1MDQsInR5cGUiOiJhY2Nlc3MifQ.6HP-JVODwxBBR3xncY__8QHYi-lXBkHASjdD_1Ri-Es';
  
  final headers = {
    'Authorization': 'Bearer $token',
    'Content-Type': 'application/json',
  };

  print('--- Testing Seller API for hieunguoiban ---');

  // 1. Get Me
  final meRes = await http.get(Uri.parse('$baseUrl/auth/me'), headers: headers);
  print('\n[AUTH ME] Status: ${meRes.statusCode}');
  print('Body: ${meRes.body}');

  // 2. Get Seller Products
  final productsRes = await http.get(Uri.parse('$baseUrl/seller/products?page=1&limit=10'), headers: headers);
  print('\n[SELLER PRODUCTS] Status: ${productsRes.statusCode}');
  print('Body: ${productsRes.body}');

  // 3. Get Seller Orders
  final ordersRes = await http.get(Uri.parse('$baseUrl/seller/orders?page=1&limit=10'), headers: headers);
  print('\n[SELLER ORDERS] Status: ${ordersRes.statusCode}');
  print('Body: ${ordersRes.body}');

  // 4. Get Seller Revenue
  final revenueRes = await http.get(Uri.parse('$baseUrl/seller/revenue'), headers: headers);
  print('\n[SELLER REVENUE] Status: ${revenueRes.statusCode}');
  print('Body: ${revenueRes.body}');
  
  // 5. Test Dahboard Stats (if exists in Swagger)
  final statsRes = await http.get(Uri.parse('$baseUrl/seller/dashboard'), headers: headers);
  print('\n[SELLER DASHBOARD] Status: ${statsRes.statusCode}');
  print('Body: ${statsRes.body}');
}
