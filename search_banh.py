import requests, json

base_url = "http://207.180.233.84:8000"
username = "hieunguoimua"
password = "Trinh123456@"

r = requests.post(f"{base_url}/api/auth/login", json={"ten_dang_nhap": username, "mat_khau": password})
t = r.json().get("token")
b = r.json().get("data").get("sub")
h = {"Authorization": "Bearer "+t}

res = requests.get(f"{base_url}/api/buyer/nguyen-lieu?search=bánh", headers=h).json()
items = res.get("data", [])

with open("test.txt", "w", encoding="utf-8") as f:
    f.write("Banh mi search results:\n")
    for i in items:
        f.write(f"{i['ma_nguyen_lieu']} - {i['ten_nguyen_lieu']}\n")
        # Get details to see sellers
        det = requests.get(f"{base_url}/api/buyer/nguyen-lieu/{i['ma_nguyen_lieu']}", headers=h).json()
        sellers = det.get("sellers", {}).get("data", [])
        for s in sellers:
            f.write(f"  Seller: {s['ma_gian_hang']} - {s['ten_gian_hang']}\n")
            if "Kim Hùng" in s['ten_gian_hang']:
                print(f"Adding from {s['ma_gian_hang']}")
                add_data = {"ingredient_id": i['ma_nguyen_lieu'], "stall_id": s['ma_gian_hang'], "cart_quantity": 1}
                r_add = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={b}", headers=h, json=add_data)
                f.write(f"  Add result: {r_add.status_code} {r_add.text}\n")
