import requests

BASE_URL = "http://207.180.233.84:8000/api"

def get_token():
    login_url = f"{BASE_URL}/auth/login"
    # Testing for seller account
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    r = requests.post(login_url, json=login_data)
    if r.status_code == 200:
        return r.json().get('token')
    return None

token = get_token()
if token:
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: With trailing slash
    url1 = f"{BASE_URL}/seller/orders/"
    r1 = requests.get(url1, headers=headers)
    print(f"Test 1 (with slash) Status: {r1.status_code}")
    
    # Test with Params
    url_params = f"{BASE_URL}/seller/orders?page=1&limit=50"
    r_params = requests.get(url_params, headers=headers)
    print(f"Params Test Status: {r_params.status_code}")
    if r_params.status_code == 200:
        print("Success with params!")
    else:
        print(f"Failed with params: {r_params.text}")
else:
    print("Failed to login")
