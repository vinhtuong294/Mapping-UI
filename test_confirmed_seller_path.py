import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    shop_id = "GHNDBR01"
    
    tests = [
        f"/orders/seller/",
        f"/orders/seller/{shop_id}",
        f"/orders/shop/",
        f"/orders/shop/{shop_id}",
        f"/orders/seller/list",
        f"/orders/shop/list",
    ]
    
    for p in tests:
        url = f"{BASE_URL}{p}"
        resp = requests.get(url, headers=headers)
        print(f"GET {p} -> {resp.status_code}")
        if resp.status_code == 200:
            print("  SUCCESS!")
            # print(resp.text[:200])

if __name__ == "__main__":
    diagnose()
