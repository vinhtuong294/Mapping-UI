import requests, json, sys

base_url = "http://207.180.233.84:8000"

# Login
r = requests.post(f"{base_url}/api/auth/login", json={"ten_dang_nhap": "hieunguoimua", "mat_khau": "Trinh123456@"})
login_data = r.json()
token = login_data.get("token", "")
user_data = login_data.get("data", {})
buyer_id = user_data.get("sub", "")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

results = {}
results["login"] = {"buyer_id": buyer_id, "user_data_keys": list(user_data.keys()), "user_data": user_data}

# Get /auth/me for full user info
r_me = requests.get(f"{base_url}/api/auth/me", headers=headers)
results["auth_me"] = r_me.json()

# List some ingredients with detail
r_ing = requests.get(f"{base_url}/api/buyer/nguyen-lieu?limit=3", headers=headers)
ing_list = r_ing.json().get("data", [])
results["ingredients"] = []

for ing in ing_list[:3]:
    ma = ing["ma_nguyen_lieu"]
    r_det = requests.get(f"{base_url}/api/buyer/nguyen-lieu/{ma}", headers=headers)
    det = r_det.json()
    sellers = det.get("sellers", {}).get("data", [])
    
    ing_info = {
        "ma_nguyen_lieu": ma,
        "ten": ing.get("ten_nguyen_lieu", ""),
        "sellers": []
    }
    
    for s in sellers:
        seller_info = {
            "ma_gian_hang": s.get("ma_gian_hang"),
            "ten_gian_hang": s.get("ten_gian_hang"),
            "so_luong_ban": s.get("so_luong_ban"),
            "gia_goc": s.get("gia_goc"),
        }
        ing_info["sellers"].append(seller_info)
        
        # Try adding this to cart
        add_payload = {
            "ingredient_id": ma,
            "stall_id": s.get("ma_gian_hang"),
            "cart_quantity": 1
        }
        r_add = requests.post(
            f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}",
            headers=headers,
            json=add_payload
        )
        seller_info["add_result"] = {
            "status": r_add.status_code,
            "response": r_add.text[:500]
        }
        
        # Only test one seller per ingredient
        break
    
    results["ingredients"].append(ing_info)

# Also try with integer cart_quantity
if ing_list:
    first = ing_list[0]
    ma = first["ma_nguyen_lieu"]
    r_det2 = requests.get(f"{base_url}/api/buyer/nguyen-lieu/{ma}", headers=headers)
    sellers2 = r_det2.json().get("sellers", {}).get("data", [])
    if sellers2:
        s2 = sellers2[0]
        # Test with float
        add_float = {
            "ingredient_id": ma,
            "stall_id": s2["ma_gian_hang"],
            "cart_quantity": 1.0
        }
        r_f = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}", headers=headers, json=add_float)
        results["test_float_qty"] = {"status": r_f.status_code, "response": r_f.text[:500]}
        
        # Test with string quantity
        add_str = {
            "ingredient_id": ma,
            "stall_id": s2["ma_gian_hang"],
            "cart_quantity": "1"
        }
        r_s = requests.post(f"{base_url}/api/buyer/cart/items?buyer_id={buyer_id}", headers=headers, json=add_str)
        results["test_string_qty"] = {"status": r_s.status_code, "response": r_s.text[:500]}

# Get cart state
r_cart = requests.get(f"{base_url}/api/buyer/cart/?buyer_id={buyer_id}", headers=headers)
results["cart"] = {"status": r_cart.status_code, "response": r_cart.text[:500]}

with open("debug_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done! Check debug_results.json")
