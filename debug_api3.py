import requests

base_url = "http://207.180.233.84:8000"
username = "hieunguoimua"
password = "Trinh123456@"

r = requests.post(f"{base_url}/api/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
data = r.json()
token = data.get("token", "")
buyer_id = data.get("data", {}).get("sub", "")

headers = {"Authorization": f"Bearer {token}"}
print(f"Token: {token[:10]}... Buyer ID: {buyer_id}")

print("\n--- Getting Cart ---")
r2 = requests.get(f"{base_url}/api/buyer/cart/?buyer_id={buyer_id}", headers=headers)
print("Status:", r2.status_code)
print("Response:", r2.text)

print("\n--- Attempt Add To Cart Again ---")
add_data = {
    "ingredient_id": "NL3100",
    "stall_id": "GH01",
    "cart_quantity": 1
}
r_add = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}", headers=headers, json=add_data)
print("Add status:", r_add.status_code)
print("Add response:", r_add.text)

print("\n--- Trying To Checkout ---")
checkout_data = {
    "selected_items": [{"ingredient_id": "NL3100", "stall_id": "GH01"}],
    "payment_method": "tien_mat"
}
r_check = requests.post(f"{base_url}/api/buyer/cart/checkout", headers=headers, json=checkout_data)
print("Checkout status:", r_check.status_code)
print("Checkout response:", r_check.text)
