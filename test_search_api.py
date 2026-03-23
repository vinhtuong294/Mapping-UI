import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def test_search(query):
    # Login to get token
    login_data = {"ten_dang_nhap": "hieunguoimua", "mat_khau": "Trinh123456@"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if r.status_code != 200:
        print("Login failed")
        return
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"--- Searching for '{query}' ---")
    
    # 1. Test MonAnService style: /buyer/mon-an?search=...
    url1 = f"{BASE_URL}/buyer/mon-an"
    params1 = {"search": query}
    r1 = requests.get(url1, headers=headers, params=params1)
    print(f"1. MonAnService (/buyer/mon-an?search={query}) -> STATUS: {r1.status_code}")
    if r1.status_code == 200:
        data = r1.json().get('data', [])
        print(f"   Found {len(data)} results")
        if data:
            print(f"   First Result: {data[0].get('ten_mon_an')}")
    
    # 4. Find exact 'mướp' dish
    url4 = f"{BASE_URL}/buyer/mon-an"
    r4 = requests.get(url4, headers=headers, params={"limit": 100})
    if r4.status_code == 200:
        data = r4.json().get('data', [])
        matches = [d for d in data if "mướp" in d.get('ten_mon_an', '').lower()]
    # 13. Test /api/search (no slash)
    url13 = f"{BASE_URL}/search"
    r13 = requests.get(url13, headers=headers, params={"q": "canh"})
    print(f"13. /api/search?q=canh -> STATUS: {r13.status_code}")
    if r13.status_code == 200:
        print(f"    Body: {r13.text}")

if __name__ == "__main__":
    test_search("canh")
