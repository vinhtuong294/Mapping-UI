import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    prefixes = ["seller-orders", "seller_orders", "orders/seller", "all-orders", "orders/shop"]
    for p in prefixes:
        url = f"{BASE_URL}/{p}"
        resp = requests.get(url, headers=headers)
        print(f"GET {p} -> {resp.status_code}")
        if resp.status_code != 404:
            print(f"  INTERESTING: {resp.status_code}")

if __name__ == "__main__":
    diagnose()
