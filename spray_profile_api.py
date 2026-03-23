import requests
import json

base_url = "http://207.180.233.84:8000/api"
username = "hieunguoimua"
password = "Trinh123456@"

print(f"Logging in as {username}...")
r = requests.post(f"{base_url}/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
token = r.json().get("token")
login_data = r.json().get("data", {})
user_id = login_data.get("sub")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Get real IDs from /auth/me
r_me = requests.get(f"{base_url}/auth/me", headers=headers)
me_data = r_me.json().get("data", {})
user_id = me_data.get("user_id")
buyer_id = me_data.get("buyer_id")

update_data = {
    "user_name": "Hieunguoimua Spray",
    "gender": "M",
}

endpoints = [
    "/auth/me",
    "/auth/profile",
    "/buyer/me",
    "/buyer/profile",
    f"/users/{user_id}",
    f"/buyer/{buyer_id}",
    "/auth/user",
]

methods = ["PATCH", "PUT", "POST"]

results = []

for ep in endpoints:
    for method in methods:
        url = f"{base_url}{ep}"
        print(f"Testing {method} {url}")
        try:
            if method == "PATCH":
                res = requests.patch(url, headers=headers, json=update_data)
            elif method == "PUT":
                res = requests.put(url, headers=headers, json=update_data)
            else:
                res = requests.post(url, headers=headers, json=update_data)
            
            if res.status_code != 404:
                print(f"🔥🔥 FOUND SOMETHING: {method} {url} -> {res.status_code}")
                results.append({
                    "method": method,
                    "url": url,
                    "status": res.status_code,
                    "data": res.json() if res.status_code in [200, 201] else res.text
                })
        except Exception as e:
            pass

with open("profile_spray_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Done!")
