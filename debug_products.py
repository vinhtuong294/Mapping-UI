import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def debug():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    h = {'Authorization': f'Bearer {token}'}
    
    prod = requests.get(f"{BASE_URL}/seller/products", headers=h).json()
    if prod.get('data'):
        print(json.dumps(prod['data'][0], indent=2))
    else:
        print("No products found")

if __name__ == "__main__":
    debug()
