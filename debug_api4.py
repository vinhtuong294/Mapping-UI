import requests, json

base_url = "http://207.180.233.84:8000"
username = "hieunguoimua"
password = "Trinh123456@"

r = requests.post(f"{base_url}/api/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
data = r.json()
token = data.get("token", "")
buyer_id = data.get("data", {}).get("sub", "")

headers = {"Authorization": f"Bearer {token}"}

r2 = requests.get(f"{base_url}/api/buyer/cart/?buyer_id={buyer_id}", headers=headers)
add_data = {"ingredient_id": "NL3100", "stall_id": "GH01", "cart_quantity": 1}
r_add = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}", headers=headers, json=add_data)

checkout_data = {"selected_items": [{"ingredient_id": "NL3100", "stall_id": "GH01"}], "payment_method": "tien_mat"}
r_check = requests.post(f"{base_url}/api/buyer/cart/checkout", headers=headers, json=checkout_data)

out = {
    "get_cart": {"status": r2.status_code, "text": r2.text},
    "add_cart": {"status": r_add.status_code, "text": r_add.text},
    "checkout": {"status": r_check.status_code, "text": r_check.text}
}
with open("api_debug.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
