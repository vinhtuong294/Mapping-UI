import requests
import json

base_url = "http://207.180.233.84:8000/api"
username = "hieunguoimua"
password = "Trinh123456@"

def main():
    print(f"Logging in as {username}...")
    r = requests.post(f"{base_url}/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
    if r.status_code != 200:
        print("Login failed:", r.text)
        return

    token = r.json().get("token")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    results = {}

    # 1. GET Profile
    r_me = requests.get(f"{base_url}/auth/me", headers=headers)
    results["get_profile"] = {
        "status": r_me.status_code,
        "data": r_me.json() if r_me.status_code == 200 else r_me.text
    }

    # 2. Try PATCH variations
    update_data = {
        "ten_nguoi_dung": "Hieunguoimua TEST",
        "gioi_tinh": "M",
    }

    results["patch_tests"] = []
    for path in ["/auth/me", "/auth/me/", "/buyer/me", "/buyer/me/"]:
        r_patch = requests.patch(f"{base_url}{path}", headers=headers, json=update_data)
        results["patch_tests"].append({
            "path": path,
            "status": r_patch.status_code,
            "data": r_patch.json() if r_patch.status_code in [200, 201] else r_patch.text
        })

    with open("profile_api_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Results written to profile_api_results.json")

if __name__ == "__main__":
    main()
