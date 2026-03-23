import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    # 1. Login
    login_url = f"{BASE_URL}/auth/login"
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    resp = requests.post(login_url, json=login_data)
    if resp.status_code != 200:
        return
    token = resp.json().get('token')
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 2. Get User Info
    me_resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    me_data = me_resp.json().get('data', {})
    user_id = me_data.get('ma_nguoi_dung') or me_data.get('id') or me_data.get('user_id')
    # For seller, shop_id is crucial
    shop_id = me_data.get('ma_gian_hang') or me_data.get('shop_id')
    
    print(f"User ID: {user_id}, Shop ID: {shop_id}")
    
    # 3. Test Endpoints
    endpoints = [
        "/seller/orders",
        "/seller/orders/",
        "/orders",
        "/orders/",
        "/seller/order",
        "/seller/order/"
    ]
    
    params_list = [
        {},
        {"ma_gian_hang": shop_id},
        {"seller_id": user_id},
        {"buyer_id": user_id},
        {"shop_id": shop_id}
    ]
    
    for ep in endpoints:
        for p in params_list:
            if p is None: continue
            full_url = f"{BASE_URL}{ep}"
            try:
                r = requests.get(full_url, headers=headers, params=p, timeout=5)
                # Only print interesting results
                if r.status_code != 404:
                    print(f"URL: {ep} | Params: {p} | STATUS: {r.status_code}")
                    if r.status_code == 200:
                        print(f"CONTENT: {r.text[:200]}")
            except Exception as e:
                pass

if __name__ == "__main__":
    diagnose()
