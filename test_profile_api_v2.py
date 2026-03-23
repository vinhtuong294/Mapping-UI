import requests
import json

base_url = "http://207.180.233.84:8000/api"
username = "hieunguoimua"
password = "Trinh123456@"

def log_res(label, res):
    print(f"\n--- {label} ---")
    print(f"Status: {res.status_code}")
    try:
        data = res.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response (text): {res.text}")

print(f"Logging in as {username}...")
r = requests.post(f"{base_url}/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
if r.status_code != 200:
    print("Login failed:", r.text)
    exit(1)

token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1. GET Profile
r_me = requests.get(f"{base_url}/auth/me", headers=headers)
log_res("GET /auth/me", r_me)

# 2. Try PATCH variations
update_data = {
    "ten_nguoi_dung": "Hieunguoimua (Updated)",
    "gioi_tinh": "M",
}

for path in ["/auth/me", "/auth/me/", "/buyer/me", "/buyer/me/"]:
    r_patch = requests.patch(f"{base_url}{path}", headers=headers, json=update_data)
    log_res(f"PATCH {path}", r_patch)
    if r_patch.status_code == 200:
        print(f"✅ Success with {path}")
        break
