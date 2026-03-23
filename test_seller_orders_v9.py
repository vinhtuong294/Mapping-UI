import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # List all shops to find which one belongs to hieunguoiban
    # The buyer API has /gian-hang
    print("Listing all shops...")
    shops_resp = requests.get(f"{BASE_URL}/buyer/gian-hang?limit=100", headers=headers)
    if shops_resp.status_code == 200:
        shops = shops_resp.json().get('data', [])
        print(f"Found {len(shops)} shops.")
        for s in shops:
            # We don't know the owner field, but let's see details of each
            sid = s.get('ma_gian_hang')
            sname = s.get('ten_gian_hang')
            # Check if name sounds like hieu
            if "hieu" in sname.lower():
                print(f"POTENTIAL MATCH: {sid} - {sname}")
            
            # Get detail to see if owner is mentioned
            # s_detail = requests.get(f"{BASE_URL}/buyer/gian-hang/{sid}", headers=headers).json()
            # print(f"Detail for {sid}: {json.dumps(s_detail, indent=2)}")
    else:
        print(f"Failed to list shops: {shops_resp.status_code}")

if __name__ == "__main__":
    diagnose()
