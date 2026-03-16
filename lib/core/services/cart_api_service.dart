import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/cart_response.dart';
import '../config/app_config.dart';
import '../utils/app_logger.dart';
import 'auth/simple_auth_helper.dart';

/// Service để fetch thông tin giỏ hàng từ API
class CartApiService {
  static const String _baseUrl = AppConfig.buyerBaseUrl;

  /// Thêm sản phẩm vào giỏ hàng
  Future<AddToCartResponse> addToCart({
    required String maNguyenLieu,
    required String maGianHang,
    required double soLuong,
    String maCho = 'C01',
  }) async {
    print('🛒 [CART API] ========== ADD TO CART REQUEST ==========');
    print('🛒 [CART API] ma_nguyen_lieu: $maNguyenLieu');
    print('🛒 [CART API] ma_gian_hang: $maGianHang');
    print('🛒 [CART API] so_luong: $soLuong');
    print('🛒 [CART API] ma_cho: $maCho');

    if (AppConfig.enableApiLogging) {
      AppLogger.info('🛒 [CART API] Adding item to cart: $maNguyenLieu');
    }

    try {
      final token = await getToken();

      if (token == null) {
        throw Exception('User not logged in');
      }

    final url = Uri.parse('$_baseUrl/cart/items');
      
      final requestBody = {
        'ma_nguyen_lieu': maNguyenLieu,
        'ma_gian_hang': maGianHang,
        // Cho phép số lượng lẻ (ví dụ 0.5). Backend cần hỗ trợ giá trị này.
        'so_luong': soLuong,
        'ma_cho': maCho,
      };

      print('🛒 [CART API] URL: $url');
      print('🛒 [CART API] Request Body: ${json.encode(requestBody)}');

      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: json.encode(requestBody),
      );

      print('🛒 [CART API] Response Status: ${response.statusCode}');
      print('🛒 [CART API] Response Body: ${response.body}');
      print('🛒 [CART API] ========================================');

      if (AppConfig.enableApiLogging) {
        AppLogger.info('🛒 [CART API] Add to cart response: ${response.statusCode}');
      }

      if (response.statusCode == 200 || response.statusCode == 201) {
        final jsonData = json.decode(utf8.decode(response.bodyBytes));
        final result = AddToCartResponse.fromJson(jsonData);
        
        // Kiểm tra success từ API response
        if (!result.success) {
          throw Exception(result.message ?? 'Không thể thêm vào giỏ hàng');
        }
        
        return result;
      } else {
        throw Exception(
            'Failed to add to cart: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('❌ [CART API] Error: $e');
      if (AppConfig.enableApiLogging) {
        AppLogger.error('❌ [CART API] Add to cart error: $e');
      }
      rethrow;
    }
  }

  /// Checkout giỏ hàng với các items đã chọn
  /// 
  /// Parameters:
  /// - selectedItems: Danh sách items cần checkout
  /// - paymentMethod: Phương thức thanh toán ('tien_mat' hoặc 'chuyen_khoan')
  /// - recipient: Thông tin người nhận (name, phone, address)
  Future<CheckoutResponse> checkout({
    required List<Map<String, String>> selectedItems,
    String? paymentMethod,
    Map<String, String>? recipient,
  }) async {
    if (AppConfig.enableApiLogging) {
      AppLogger.info('💳 [CART API] Checkout with ${selectedItems.length} items');
      AppLogger.info('💳 [CART API] Payment method: $paymentMethod');
    }

    try {
      final token = await getToken();
      
      if (token == null) {
        throw Exception('User not logged in');
      }

      final url = Uri.parse('$_baseUrl/cart/checkout');
      
      final requestBody = <String, dynamic>{
        'selectedItems': selectedItems,
      };
      
      // Thêm payment_method nếu có
      if (paymentMethod != null) {
        requestBody['payment_method'] = paymentMethod;
      }
      
      // Thêm recipient nếu có
      if (recipient != null) {
        requestBody['recipient'] = recipient;
      }

      if (AppConfig.enableApiLogging) {
        AppLogger.info('💳 [CART API] Request body: $requestBody');
      }

      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: json.encode(requestBody),
      );

      if (AppConfig.enableApiLogging) {
        AppLogger.info('💳 [CART API] Response status: ${response.statusCode}');
        AppLogger.info('💳 [CART API] Response body: ${response.body}');
      }

      if (response.statusCode == 200 || response.statusCode == 201) {
        final jsonData = json.decode(utf8.decode(response.bodyBytes));
        return CheckoutResponse.fromJson(jsonData);
      } else {
        throw Exception(
            'Failed to checkout: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      if (AppConfig.enableApiLogging) {
        AppLogger.error('❌ [CART API] Checkout error: $e');
      }
      rethrow;
    }
  }

  /// Fetch thông tin giỏ hàng
  Future<CartResponse> getCart() async {
    if (AppConfig.enableApiLogging) {
      AppLogger.info('🛒 [CART API] Fetching cart data');
    }

    try {
      // Get authentication token
      final token = await getToken();
      
      if (token == null) {
        if (AppConfig.enableApiLogging) {
          AppLogger.warning('🛒 [CART API] No token found - user not logged in');
        }
        throw Exception('User not logged in');
      }

      final url = Uri.parse('$_baseUrl/cart');

      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      if (AppConfig.enableApiLogging) {
        AppLogger.info('🛒 [CART API] Response status: ${response.statusCode}');
      }

      if (response.statusCode == 200) {
        final jsonData = json.decode(utf8.decode(response.bodyBytes));

        if (AppConfig.enableApiLogging) {
          AppLogger.info('🛒 [CART API] Response data: $jsonData');
        }

        final cartResponse = CartResponse.fromJson(jsonData);

        if (AppConfig.enableApiLogging) {
          AppLogger.info(
              '✅ [CART API] Success - ${cartResponse.cart.soMatHang} items');
        }

        return cartResponse;
      } else {
        throw Exception(
            'Failed to load cart: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      if (AppConfig.enableApiLogging) {
        AppLogger.error('❌ [CART API] Error: $e');
      }
      rethrow;
    }
  }

  /// Xóa sản phẩm khỏi giỏ hàng
  /// API: DELETE /api/buyer/cart/items/{ma_nguyen_lieu}/{ma_gian_hang}
  /// Response: {success: bool, ma_don_hang: string, tong_tien: double, tong_tien_goc: double, tiet_kiem: double}
  Future<DeleteCartItemResponse> deleteCartItem({
    required String maNguyenLieu,
    required String maGianHang,
  }) async {
    if (AppConfig.enableApiLogging) {
      AppLogger.info('🗑️ [CART API] Deleting item: $maNguyenLieu from shop: $maGianHang');
    }

    try {
      final token = await getToken();
      
      if (token == null) {
        throw Exception('User not logged in');
      }

      final url = Uri.parse('$_baseUrl/cart/items/$maNguyenLieu/$maGianHang');

      print('🗑️ [CART API] DELETE URL: $url');

      final response = await http.delete(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      print('🗑️ [CART API] Response Status: ${response.statusCode}');
      print('🗑️ [CART API] Response Body: ${response.body}');

      if (AppConfig.enableApiLogging) {
        AppLogger.info('🗑️ [CART API] Delete response: ${response.statusCode}');
      }

      if (response.statusCode == 200 || response.statusCode == 204) {
        // Handle empty response body (204 No Content)
        if (response.body.isEmpty) {
          return DeleteCartItemResponse(
            success: true,
            message: 'Item deleted successfully',
          );
        }
        final jsonData = json.decode(utf8.decode(response.bodyBytes));
        return DeleteCartItemResponse.fromJson(jsonData);
      } else {
        throw Exception(
            'Failed to delete cart item: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('❌ [CART API] Delete error: $e');
      if (AppConfig.enableApiLogging) {
        AppLogger.error('❌ [CART API] Delete item error: $e');
      }
      rethrow;
    }
  }
}
