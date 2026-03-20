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
token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Proposed English payload based on GET result
update_data = {
    "user_name": "Hieunguoimua Updated V4",
    "gender": "M",
    "phone": "0912345678",
    "address": "123 Nguyễn Văn Linh, Đà Nẵng",
    "bank_account": "123456789",
    "bank_name": "TPBank",
    "weight": 60.5,
    "height": 170.0
}

endpoints = ["/auth/me", "/auth/me/"]
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
            
            results.append({
                "method": method,
                "url": url,
                "status": res.status_code,
                "data": res.json() if res.status_code in [200, 201] else res.text
            })
        except Exception as e:
            results.append({"method": method, "url": url, "error": str(e)})

with open("profile_update_matrix.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Done! Check profile_update_matrix.json")
