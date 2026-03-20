import requests

BASE_URL = "http://207.180.233.84:8000/api"
headers = {
    "Authorization": "Bearer hieunguoimua_token" # I'll need to login first or use the one from previous tests
}

def get_token():
    login_url = f"{BASE_URL}/auth/login"
    login_data = {"ten_dang_nhap": "hieunguoimua", "mat_khau": "Trinh123456@"}
    r = requests.post(login_url, json=login_data)
    if r.status_code == 200:
        return r.json().get('token')
    return None

token = get_token()
if token:
    headers["Authorization"] = f"Bearer {token}"
    # Search for something with results
    url = f"{BASE_URL}/search/"
    r = requests.get(url, headers=headers, params={"q": "bánh mì"})
    print(f"Status: {r.status_code}")
    print(f"Body: {r.text[:2000]}") # Print more text
else:
    print("Failed to login")
