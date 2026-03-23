import requests
import json

base_url = "http://207.180.233.84:8000/api"
username = "hieunguoimua"
password = "Trinh123456@"

print(f"Logging in as {username}...")
r = requests.post(f"{base_url}/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
if r.status_code != 200:
    print("Login failed:", r.text)
    exit(1)

data = r.json()
token = data.get("token")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

print("\n--- Getting Profile (/auth/me) ---")
r_me = requests.get(f"{base_url}/auth/me", headers=headers)
print("Status:", r_me.status_code)
print("Response:", json.dumps(r_me.json(), indent=2, ensure_ascii=False))

print("\n--- Updating Profile (/auth/me) ---")
# Let's try to update the name to see if it works
update_data = {
    "ten_nguoi_dung": "Nguyễn Văn Hưng (Test)",
    "gioi_tinh": "M",
    "sdt": "0987654321",
    "dia_chi": "Hà Nội, Việt Nam"
}
r_update = requests.patch(f"{base_url}/auth/me", headers=headers, json=update_data)
print("Update Status:", r_update.status_code)
print("Update Response:", json.dumps(r_update.json(), indent=2, ensure_ascii=False))
