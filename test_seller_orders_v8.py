import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user info
    me = requests.get(f"{BASE_URL}/auth/me", headers=headers).json()
    user_id = me['data'].get('ma_nguoi_dung') or me['data'].get('user_id')
    
    # Try different combinations
    words = ["orders", "order", "donhang", "don-hang", "list-orders", "all-orders"]
    prefixes = ["seller/", "seller-", "", "buyer/"]
    suffixes = ["", "/"]
    
    results = []
    for p in prefixes:
        for w in words:
            for s in suffixes:
                url = f"{BASE_URL}/{p}{w}{s}"
                try:
                    resp = requests.get(url, headers=headers, timeout=3)
                    if resp.status_code != 404:
                        print(f"INTERESTING: {url} -> {resp.status_code}")
                        results.append((url, resp.status_code))
                except:
                    pass
    
    # Also test /api/orders with common params
    shop_id = "GH1"
    tests_with_params = [
        ("/orders/", {"ma_gian_hang": shop_id}),
        ("/orders/", {"seller_id": user_id}),
        ("/seller/orders/", {"ma_gian_hang": shop_id}),
    ]
    
    for ep, params in tests_with_params:
        url = f"{BASE_URL}{ep}"
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=3)
            if resp.status_code != 404:
                print(f"PARAM_TEST: {url} with {params} -> {resp.status_code}")
        except:
            pass

if __name__ == "__main__":
    diagnose()
