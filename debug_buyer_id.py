import requests, json

base_url = "http://207.180.233.84:8000"

# Login
r = requests.post(f"{base_url}/api/auth/login", json={"ten_dang_nhap": "hieunguoimua", "mat_khau": "Trinh123456@"})
login_data = r.json()
token = login_data.get("token", "")
user_id = login_data.get("data", {}).get("sub", "")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Get actual buyer_id from /auth/me
r_me = requests.get(f"{base_url}/api/auth/me", headers=headers)
me_data = r_me.json().get("data", {})
buyer_id = me_data.get("buyer_id", "")

results = {
    "user_id_from_login": user_id,
    "buyer_id_from_me": buyer_id,
}

# Find ingredient with sellers
r_ing = requests.get(f"{base_url}/api/buyer/nguyen-lieu?limit=20&hinh_anh=true", headers=headers)
ing_list = r_ing.json().get("data", [])

found_seller = None
for ing in ing_list:
    ma = ing["ma_nguyen_lieu"]
    r_det = requests.get(f"{base_url}/api/buyer/nguyen-lieu/{ma}", headers=headers)
    det = r_det.json()
    sellers = det.get("sellers", {}).get("data", [])
    if sellers:
        found_seller = {
            "ma_nguyen_lieu": ma,
            "ten": ing.get("ten_nguyen_lieu", ""),
            "ma_gian_hang": sellers[0]["ma_gian_hang"],
            "ten_gian_hang": sellers[0]["ten_gian_hang"],
        }
        break

results["found_product"] = found_seller

if found_seller:
    # Test 1: With WRONG buyer_id (user_id from login)
    add_payload = {
        "ingredient_id": found_seller["ma_nguyen_lieu"],
        "stall_id": found_seller["ma_gian_hang"],
        "cart_quantity": 1
    }
    r_wrong = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={user_id}", headers=headers, json=add_payload)
    results["test_wrong_buyer_id"] = {"status": r_wrong.status_code, "response": r_wrong.text[:500]}
    
    # Test 2: With CORRECT buyer_id from /auth/me
    r_correct = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}", headers=headers, json=add_payload)
    results["test_correct_buyer_id"] = {"status": r_correct.status_code, "response": r_correct.text[:500]}

    # Test 3: Get cart with correct buyer_id
    r_cart = requests.get(f"{base_url}/api/buyer/cart/?buyer_id={buyer_id}", headers=headers)
    results["cart_correct_id"] = {"status": r_cart.status_code, "response": r_cart.text[:500]}

    # Test 4: Get cart with wrong buyer_id
    r_cart2 = requests.get(f"{base_url}/api/buyer/cart/?buyer_id={user_id}", headers=headers)
    results["cart_wrong_id"] = {"status": r_cart2.status_code, "response": r_cart2.text[:500]}

with open("debug_buyer_id.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done! Check debug_buyer_id.json")
