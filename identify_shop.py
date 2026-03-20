import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def find_shop():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Get one product ID of this seller
    prod_resp = requests.get(f"{BASE_URL}/seller/products", headers=headers).json()
    if not prod_resp.get('data'):
        print("No products found for this seller.")
        return
    
    my_product_id = prod_resp['data'][0]['ma_nguoi_dung'] if 'ma_nguoi_dung' in prod_resp['data'][0] else prod_resp['data'][0]['ma_nguyen_lieu']
    print(f"My product ID: {my_product_id}")
    
    # 2. List all shops and find which one has this product
    shops_resp = requests.get(f"{BASE_URL}/buyer/gian-hang?limit=100", headers=headers).json()
    shops = shops_resp.get('data', [])
    
    for s in shops:
        sid = s['ma_gian_hang']
        # Search this shop's products
        # Correct endpoint from ShopDetailModel: /api/buyer/gian-hang/{ma_gian_hang}
        detail = requests.get(f"{BASE_URL}/buyer/gian-hang/{sid}", headers=headers).json()
        items = detail.get('san_pham', {}).get('data', [])
        for item in items:
            if item.get('ma_nguyen_lieu') == my_product_id:
                print(f"FOUND MATCH! Shop ID: {sid}, Shop Name: {s['ten_gian_hang']}")
                return

if __name__ == "__main__":
    find_shop()
