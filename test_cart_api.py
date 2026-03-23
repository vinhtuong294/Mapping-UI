import requests
import json

base_url = "http://207.180.233.84:8000"
username = "hieunguoimua"
password = "Trinh123456@"

print("Logging in...")
login_data = {"ten_dang_nhap": username, "mat_khau": password}
r = requests.post(f"{base_url}/api/auth/login", json=login_data)
data = r.json()
token = data.get("token", "")
if "data" in data and "ma_nguoi_dung" in data["data"]:
    buyer_id = data["data"]["ma_nguoi_dung"]
else:
    buyer_id = data.get("ma_nguoi_dung", "")

headers = {"Authorization": f"Bearer {token}"}
print(f"Token: {token[:10]}... Buyer ID: {buyer_id}")

print("\nGetting cart...")
r = requests.get(f"{base_url}/api/buyer/cart/?buyer_id={buyer_id}", headers=headers)
print(r.status_code, r.text)

print("\nListing ingredients...")
r = requests.get(f"{base_url}/api/buyer/nguyen-lieu?limit=1", headers=headers)
ing_data = r.json()

if type(ing_data) == dict and "data" in ing_data:
    ingredients = ing_data["data"]
else:
    ingredients = ing_data

if not ingredients:
    print("No ingredients found")
    exit(1)

print("First ingredient:", json.dumps(ingredients[0], ensure_ascii=False))

ingredient_id = ingredients[0].get("ma_nguyen_lieu")
stall_id = ingredients[0].get("ma_gian_hang", "GH01") # fallback if not found
print(f"Found ingredient: {ingredient_id} at stall: {stall_id}")

print("\nAdding to cart...")
add_data = {
    "ingredient_id": ingredient_id,
    "stall_id": stall_id,
    "cart_quantity": 1
}
r_add = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}", headers=headers, json=add_data)
print(r_add.status_code, r_add.text)

print("\nGetting cart after add...")
r2 = requests.get(f"{base_url}/api/buyer/cart/?buyer_id={buyer_id}", headers=headers)
print(r2.status_code, r2.text)
