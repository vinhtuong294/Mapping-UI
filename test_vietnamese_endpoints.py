import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    words = ["don-hang", "donhang", "danh-sach-don-hang", "quan-ly-don-hang"]
    suffixes = ["", "/"]
    
    for w in words:
        for s in suffixes:
            url = f"{BASE_URL}/seller/{w}{s}"
            resp = requests.get(url, headers=headers)
            print(f"GET {url} -> {resp.status_code}")
            if resp.status_code == 200:
                print("  FOUND IT!")

if __name__ == "__main__":
    diagnose()
