import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final baseUrl = 'http://207.180.233.84:8000/api';
  final loginUrl = '$baseUrl/auth/login';
  
  print('Testing Login for hieunguoiban...');
  
  try {
    // 1. Try JSON
    print('\n[TRY 1] JSON Body...');
    final responseJson = await http.post(
      Uri.parse(loginUrl),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'ten_dang_nhap': 'hieunguoiban',
        'mat_khau': 'Trinh123456@',
      }),
    );
    print('Status: ${responseJson.statusCode}');
    print('Body: ${responseJson.body}');

    // 2. Try Form Data (username/password)
    if (responseJson.statusCode != 200) {
      print('\n[TRY 2] Form Data (username/password)...');
      final responseForm = await http.post(
        Uri.parse(loginUrl),
        body: {
          'username': 'hieunguoiban',
          'password': 'Trinh123456@',
        },
      );
      print('Status: ${responseForm.statusCode}');
      print('Body: ${responseForm.body}');
    }

    // 3. Try Form Data (ten_dang_nhap/mat_khau)
    if (responseJson.statusCode != 200) {
      print('\n[TRY 3] Form Data (ten_dang_nhap/mat_khau)...');
      final responseForm2 = await http.post(
        Uri.parse(loginUrl),
        body: {
          'ten_dang_nhap': 'hieunguoiban',
          'mat_khau': 'Trinh123456@',
        },
      );
      print('Status: ${responseForm2.statusCode}');
      print('Body: ${responseForm2.body}');
    }
  } catch (e) {
    print('Error: $e');
  }
}
