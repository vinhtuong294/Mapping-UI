import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    # Login
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = resp.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    me = requests.get(f"{BASE_URL}/auth/me", headers=headers).json()
    user_id = me['data'].get('ma_nguoi_dung') or me['data'].get('user_id')
    
    # Try to find shop ID from products
    prod_resp = requests.get(f"{BASE_URL}/seller/products", headers=headers)
    shop_id = "GH1" # Default from previous observation
    if prod_resp.status_code == 200:
        p_data = prod_resp.json().get('data', [])
        if p_data:
            shop_id = p_data[0].get('ma_gian_hang') or shop_id

    print(f"IDs: user={user_id}, shop={shop_id}")

    endpoints = [
        "orders", "order", "list-orders", "all-orders", "get-orders", 
        "don-hang", "danh-sach-don-hang", "orders-list"
    ]
    suffixes = ["", "/"]
    
    found = []
    for ep in endpoints:
        for s in suffixes:
            url = f"{BASE_URL}/seller/{ep}{s}"
            r = requests.get(url, headers=headers)
            if r.status_code != 404:
                print(f"INTERESTING: {url} -> {r.status_code}")
                found.append((url, r.status_code))
                if r.status_code == 200:
                    print(f"  SUCCESS! Content head: {r.text[:200]}")
            
    # Also test /api/orders/ variations with shop_id
    for ep in ["orders", "order"]:
        for s in ["", "/"]:
            url = f"{BASE_URL}/{ep}{s}"
            r = requests.get(url, headers=headers, params={"ma_gian_hang": shop_id})
            if r.status_code != 404:
                print(f"INTERESTING: {url}?ma_gian_hang={shop_id} -> {r.status_code}")
                found.append((url, r.status_code))

    if not found:
        print("No matches found.")

if __name__ == "__main__":
    diagnose()
