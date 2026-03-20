import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    words = [
        "orders", "order", "donhang", "don-hang", "danh-sach-don-hang",
        "products", "product", "sanpham", "san-pham",
        "revenue", "doanhthu", "doanh-thu",
        "nhom-nguyen-lieu", "nguyen-lieu",
        "items", "sales", "profile", "account", "shop", "gian-hang"
    ]
    
    for w in words:
        url = f"{BASE_URL}/seller/{w}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 404:
            print(f"SELLER PATH: {url} -> {resp.status_code}")

if __name__ == "__main__":
    diagnose()
