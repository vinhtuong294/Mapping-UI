import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # hieunguoiban is a seller
    url = f"{BASE_URL}/orders/"
    resp = requests.get(url, headers=headers)
    print(f"Seller GET /orders/ -> {resp.status_code}")
    
    # Try with buyer_id param even as a seller
    resp = requests.get(url, headers=headers, params={"buyer_id": "NDFBB7"})
    print(f"Seller GET /orders/ with buyer_id=NDFBB7 -> {resp.status_code}")

    # Try seller/orders again very carefully
    url2 = f"{BASE_URL}/seller/orders"
    print(f"Seller GET /seller/orders -> {requests.get(url2, headers=headers).status_code}")
    print(f"Seller GET /seller/orders/ -> {requests.get(url2 + '/', headers=headers).status_code}")

if __name__ == "__main__":
    diagnose()
