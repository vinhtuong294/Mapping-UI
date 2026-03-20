import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    user_id = "NDFBB7"
    shop_id = "GH1"
    
    tests = [
        # Under /seller/
        ("/seller/orders", {}),
        ("/seller/orders/", {}),
        ("/seller/orders", {"ma_gian_hang": shop_id}),
        ("/seller/orders/", {"ma_gian_hang": shop_id}),
        ("/seller/orders", {"seller_id": user_id}),
        ("/seller/orders/", {"seller_id": user_id}),
        
        # At top level
        ("/orders", {"ma_gian_hang": shop_id}),
        ("/orders/", {"ma_gian_hang": shop_id}),
        ("/orders", {"seller_id": user_id}),
        ("/orders/", {"seller_id": user_id}),
    ]
    
    for ep, params in tests:
        url = f"{BASE_URL}{ep}"
        resp = requests.get(url, headers=headers, params=params)
        print(f"GET {ep} | {params} -> {resp.status_code}")
        if resp.status_code == 200:
            print(f"  SUCCESS! Item count: {len(resp.json().get('items', [])) if isinstance(resp.json(), dict) else 'Unknown'}")
            # print(resp.text[:200])

if __name__ == "__main__":
    diagnose()
