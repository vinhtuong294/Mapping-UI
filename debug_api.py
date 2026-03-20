import requests, json

base_url = "http://207.180.233.84:8000"
username = "hieunguoimua"
password = "Trinh123456@"

r = requests.post(f"{base_url}/api/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
data = r.json()
token = data.get("token", "")
if "data" in data and "ma_nguoi_dung" in data["data"]:
    buyer_id = data["data"]["ma_nguoi_dung"]
elif "data" in data and "sub" in data["data"]:
    # Maybe "sub" holds buyer_id
    buyer_id = data["data"]["sub"]
else:
    buyer_id = data.get("ma_nguoi_dung", "")

print(f"Token: {token[:10]}... Buyer ID: {buyer_id}")

headers = {"Authorization": f"Bearer {token}"}
r = requests.get(f"{base_url}/api/buyer/nguyen-lieu?limit=1", headers=headers)
ing_data = r.json()

if type(ing_data) == dict and "data" in ing_data:
    ingredients = ing_data["data"]
else:
    ingredients = ing_data

ingredient_id = ingredients[0].get("ma_nguyen_lieu")
stall_id = ingredients[0].get("ma_gian_hang", "GH01")

print(f"Adding {ingredient_id} at {stall_id} to cart...")

add_data = {
    "ingredient_id": ingredient_id,
    "stall_id": stall_id,
    "cart_quantity": 1
}
r_add = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}", headers=headers, json=add_data)
print("Add status:", r_add.status_code)
print("Add text:", r_add.text)
