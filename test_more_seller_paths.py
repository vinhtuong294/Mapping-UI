import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    words = ["orders", "order", "donhang", "don-hang", "list-orders", "all-orders", "items"]
    shop_id = "GHNDBR01"
    
    for w in words:
        url = f"{BASE_URL}/seller/{w}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 404:
            print(f"SELLER PATH EXISTS: {url} -> {resp.status_code}")
            
        # Try with param
        resp = requests.get(url, headers=headers, params={"ma_gian_hang": shop_id})
        if resp.status_code != 404:
            print(f"SELLER PATH WITH PARAM EXISTS: {url} -> {resp.status_code}")

if __name__ == "__main__":
    diagnose()
