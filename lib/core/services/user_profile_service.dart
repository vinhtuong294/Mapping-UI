import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/app_config.dart';
import 'auth/simple_auth_helper.dart';

/// Service để quản lý thông tin user profile
class UserProfileService {
  static const String _baseUrl = AppConfig.authBaseUrl;

  /// Lấy thông tin user hiện tại
  Future<UserProfileResponse> getProfile() async {
    print('👤 [PROFILE SERVICE] Fetching user profile...');

    try {
      final token = await getToken();

      if (token == null) {
        throw Exception('User not logged in');
      }

      final url = Uri.parse('$_baseUrl/me');

      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      print('👤 [PROFILE SERVICE] Response status: ${response.statusCode}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        final jsonData = json.decode(utf8.decode(response.bodyBytes));
        return UserProfileResponse.fromJson(jsonData);
      } else {
        throw Exception(
            'Failed to fetch profile: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('❌ [PROFILE SERVICE] Error: $e');
      rethrow;
    }
  }

  /// Cập nhật thông tin user
  Future<UserProfileResponse> updateProfile({
    required String tenNguoiDung,
    String? gioiTinh,
    String? sdt,
    String? diaChi,
    String? soTaiKhoan,
    String? nganHang,
    double? canNang,
    double? chieuCao,
  }) async {
    print('👤 [PROFILE SERVICE] Updating user profile...');

    try {
      final token = await getToken();

      if (token == null) {
        throw Exception('User not logged in');
      }

      final url = Uri.parse('$_baseUrl/me');

      final body = <String, dynamic>{
        'ten_nguoi_dung': tenNguoiDung,
      };

      if (gioiTinh != null) body['gioi_tinh'] = gioiTinh;
      if (sdt != null) body['sdt'] = sdt;
      if (diaChi != null) body['dia_chi'] = diaChi;
      if (soTaiKhoan != null) body['so_tai_khoan'] = soTaiKhoan;
      if (nganHang != null) body['ngan_hang'] = nganHang;
      if (canNang != null) body['can_nang'] = canNang;
      if (chieuCao != null) body['chieu_cao'] = chieuCao;

      print('👤 [PROFILE SERVICE] Request body: ${json.encode(body)}');

      final response = await http.patch(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: json.encode(body),
      );

      print('👤 [PROFILE SERVICE] Response status: ${response.statusCode}');
      print('👤 [PROFILE SERVICE] Response body: ${response.body}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        final jsonData = json.decode(utf8.decode(response.bodyBytes));
        return UserProfileResponse.fromJson(jsonData);
      } else {
        throw Exception(
            'Failed to update profile: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('❌ [PROFILE SERVICE] Error: $e');
      rethrow;
    }
  }
}

/// Model cho response profile
class UserProfileResponse {
  final UserProfileData data;

  UserProfileResponse({required this.data});

  factory UserProfileResponse.fromJson(Map<String, dynamic> json) {
    return UserProfileResponse(
      data: UserProfileData.fromJson(json['data'] ?? {}),
    );
  }
}

/// Model cho data profile
class UserProfileData {
  final String maNguoiDung;
  final String tenDangNhap;
  final String tenNguoiDung;
  final String vaiTro;
  final String? gioiTinh;
  final String? sdt;
  final String? diaChi;
  final String? soTaiKhoan;
  final String? nganHang;
  final double? canNang;
  final double? chieuCao;

  UserProfileData({
    required this.maNguoiDung,
    required this.tenDangNhap,
    required this.tenNguoiDung,
    required this.vaiTro,
    this.gioiTinh,
    this.sdt,
    this.diaChi,
    this.soTaiKhoan,
    this.nganHang,
    this.canNang,
    this.chieuCao,
  });

  factory UserProfileData.fromJson(Map<String, dynamic> json) {
    return UserProfileData(
      maNguoiDung: json['ma_nguoi_dung'] ?? '',
      tenDangNhap: json['ten_dang_nhap'] ?? '',
      tenNguoiDung: json['ten_nguoi_dung'] ?? '',
      vaiTro: json['vai_tro'] ?? '',
      gioiTinh: json['gioi_tinh'],
      sdt: json['sdt'],
      diaChi: json['dia_chi'],
      soTaiKhoan: json['so_tai_khoan'],
      nganHang: json['ngan_hang'],
      canNang: _parseDouble(json['can_nang']),
      chieuCao: _parseDouble(json['chieu_cao']),
    );
  }

  static double? _parseDouble(dynamic value) {
    if (value == null) return null;
    if (value is double) return value;
    if (value is int) return value.toDouble();
    if (value is String) return double.tryParse(value);
    return null;
  }

  /// Hiển thị giới tính
  String get gioiTinhDisplay {
    switch (gioiTinh) {
      case 'M':
        return 'Nam';
      case 'F':
        return 'Nữ';
      default:
        return 'Khác';
    }
  }
}
