import requests, json

base_url = "http://207.180.233.84:8000"
username = "hieunguoimua"
password = "Trinh123456@"

r = requests.post(f"{base_url}/api/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
data = r.json()
token = data.get("token", "")

buyer_id = data.get("data", {}).get("ma_nguoi_dung", data.get("data", {}).get("sub", ""))

headers = {"Authorization": f"Bearer {token}"}
r = requests.get(f"{base_url}/api/buyer/nguyen-lieu?hinh_anh=true&limit=10", headers=headers)
ing_data = r.json().get("data", [])

found = False
for ing in ing_data:
    ma_nguyen_lieu = ing["ma_nguyen_lieu"]
    # Get details
    r_det = requests.get(f"{base_url}/api/buyer/nguyen-lieu/{ma_nguyen_lieu}", headers=headers)
    det_data = r_det.json()
    sellers = det_data.get("sellers", {}).get("data", [])
    if sellers:
        ma_gian_hang = sellers[0]["ma_gian_hang"]
        print(f"Trying to add {ma_nguyen_lieu} from {ma_gian_hang}")
        add_data = {
            "ingredient_id": ma_nguyen_lieu,
            "stall_id": ma_gian_hang,
            "cart_quantity": 1
        }
        r_add = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}", headers=headers, json=add_data)
        print("Status", r_add.status_code)
        print("Response", r_add.text)
        found = True
        break

if not found:
    print("Could not find any product with sellers")
