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
    
    patterns = [
        f"/seller/gian-hang/{shop_id}/orders",
        f"/seller/gian-hang/{shop_id}/orders/",
        f"/seller/{user_id}/orders",
        f"/seller/{user_id}/orders/",
        f"/seller/orders/shop/{shop_id}",
        f"/seller/orders/user/{user_id}",
        "/seller/me/orders",
    ]
    
    for p in patterns:
        url = f"{BASE_URL}{p}"
        resp = requests.get(url, headers=headers)
        print(f"GET {p} -> {resp.status_code}")
        if resp.status_code == 200:
            print("  SUCCESS!")

if __name__ == "__main__":
    diagnose()
