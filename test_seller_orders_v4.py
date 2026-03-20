import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    # 1. Login
    login_url = f"{BASE_URL}/auth/login"
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    print(f"Logging in...")
    resp = requests.post(login_url, json=login_data)
    if resp.status_code != 200:
        print(f"Login failed: {resp.status_code}")
        return
    token = resp.json().get('token')
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get Me
    print(f"Fetching /auth/me...")
    me_resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if me_resp.status_code == 200:
        print("--- FULL ME RESPONSE ---")
        print(json.dumps(me_resp.json(), indent=2, ensure_ascii=False))
        print("-------------------------")
    else:
        print(f"Me failed: {me_resp.status_code}")

if __name__ == "__main__":
    diagnose()
