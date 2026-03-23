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
    
    paths = ["/orders", "/orders/", "/seller/orders", "/seller/orders/"]
    params_keys = ["ma_gian_hang", "shop_id", "seller_id", "ma_nguoi_ban", "ma_chu_gian_hang", "ma_nguoi_dung"]
    ids = [user_id, shop_id]
    
    for p in paths:
        # Try without params first
        url = f"{BASE_URL}{p}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 404:
            print(f"PATH EXISTS: {url} -> {resp.status_code}")
            
        # Try with params
        for k in params_keys:
            for v in ids:
                params = {k: v}
                resp = requests.get(url, headers=headers, params=params)
                if resp.status_code != 404:
                    print(f"URL: {url} | Params: {params} | STATUS: {resp.status_code}")
                    if resp.status_code == 200:
                        print(f"  SUCCESS! Data: {resp.text[:200]}")
                        return

if __name__ == "__main__":
    diagnose()
