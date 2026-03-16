/// Model cho món ăn từ API danh sách món ăn
/// API: GET /api/buyer/mon-an
class MonAnModel {
  final String maMonAn;
  final String tenMonAn;
  final List<DanhMucMonAn> danhMuc;

  MonAnModel({
    required this.maMonAn,
    required this.tenMonAn,
    required this.danhMuc,
  });

  /// Parse từ JSON response
  factory MonAnModel.fromJson(Map<String, dynamic> json) {
    return MonAnModel(
      maMonAn: (json['ma_mon_an'] ?? json['id'] ?? '').toString(),
      tenMonAn: (json['ten_mon_an'] ?? json['market_name'] ?? json['name'] ?? '').toString(),
      danhMuc: (json['danh_muc'] as List<dynamic>?)
              ?.map((item) => DanhMucMonAn.fromJson(item as Map<String, dynamic>))
              .toList() ?? [],
    );
  }

  /// Convert sang JSON
  Map<String, dynamic> toJson() {
    return {
      'ma_mon_an': maMonAn,
      'ten_mon_an': tenMonAn,
      'danh_muc': danhMuc.map((item) => item.toJson()).toList(),
    };
  }
}

/// Model cho danh mục món ăn
class DanhMucMonAn {
  final String maDanhMucMonAn;
  final String tenDanhMucMonAn;

  DanhMucMonAn({
    required this.maDanhMucMonAn,
    required this.tenDanhMucMonAn,
  });

  factory DanhMucMonAn.fromJson(Map<String, dynamic> json) {
    return DanhMucMonAn(
      maDanhMucMonAn: json['ma_danh_muc_mon_an'] as String? ?? '',
      tenDanhMucMonAn: json['ten_danh_muc_mon_an'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'ma_danh_muc_mon_an': maDanhMucMonAn,
      'ten_danh_muc_mon_an': tenDanhMucMonAn,
    };
  }
}

/// Model cho metadata phân trang
class MonAnMeta {
  final int page;
  final int limit;
  final int total;
  final bool hasNext;

  MonAnMeta({
    required this.page,
    required this.limit,
    required this.total,
    required this.hasNext,
  });

  factory MonAnMeta.fromJson(Map<String, dynamic> json) {
    return MonAnMeta(
      page: (json['page'] as num?)?.toInt() ?? 1,
      limit: (json['limit'] as num?)?.toInt() ?? 12,
      total: (json['total'] as num?)?.toInt() ?? 0,
      hasNext: json['hasNext'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'page': page,
      'limit': limit,
      'total': total,
      'hasNext': hasNext,
    };
  }
}
