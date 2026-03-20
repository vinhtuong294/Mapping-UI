import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    # Login
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = resp.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get ID
    me = requests.get(f"{BASE_URL}/auth/me", headers=headers).json()
    user_id = me['data'].get('ma_nguoi_dung') or me['data'].get('user_id')
    
    # We suspect ma_gian_hang might be NDFBB7 (seller id) or something else
    # Let's try to find products list first to see if it works
    print(f"Testing /seller/products...")
    prod_resp = requests.get(f"{BASE_URL}/seller/products", headers=headers)
    print(f"Products Status: {prod_resp.status_code}")
    if prod_resp.status_code == 200:
        data = prod_resp.json().get('data', [])
        if data:
            print(f"Sample product ma_gian_hang: {data[0].get('ma_gian_hang')}")
            shop_id = data[0].get('ma_gian_hang')
    else:
        shop_id = None

    print(f"User ID: {user_id}, Shop ID: {shop_id}")

    # Exhaustive test of order endpoints
    tests = [
        ("/seller/orders", {}),
        ("/seller/orders/", {}),
        ("/seller/order", {}),
        ("/seller/order/", {}),
        ("/orders", {"seller_id": user_id}),
        ("/orders/", {"seller_id": user_id}),
        ("/orders", {"ma_gian_hang": shop_id} if shop_id else {}),
        ("/orders/", {"ma_gian_hang": shop_id} if shop_id else {}),
        ("/seller/orders", {"ma_gian_hang": shop_id} if shop_id else {}),
        ("/seller/orders/", {"ma_gian_hang": shop_id} if shop_id else {}),
    ]

    for ep, params in tests:
        url = f"{BASE_URL}{ep}"
        r = requests.get(url, headers=headers, params=params)
        print(f"GET {ep} | Params: {params} | STATUS: {r.status_code}")
        if r.status_code == 200:
            print(f"  SUCCESS! Sample data: {r.text[:100]}")

if __name__ == "__main__":
    diagnose()
