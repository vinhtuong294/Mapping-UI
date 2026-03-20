import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def test_seller_orders():
    # Login as seller
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "user_name": "hieunguoiban",
        "password": "Trinh123456@"
    }
    
    print(f"Logging in as seller...")
    response = requests.post(login_url, json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} - {response.text}")
        return

    login_json = response.json()
    token = login_json.get('token')
    
    # Check if there's any ID in initial login
    print(f"Login successful. Parsing user info...")
    user_data = login_json.get('data', {})
    user_id = user_data.get('ma_nguoi_dung') or user_data.get('id')
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Fetch /me to get more info
    print(f"Fetching /auth/me...")
    me_resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    me_data = {}
    if me_resp.status_code == 200:
        me_data = me_resp.json().get('data', {})
        print(f"Me data: {json.dumps(me_data, indent=2, ensure_ascii=False)}")
        user_id = me_data.get('ma_nguoi_dung') or user_id
    else:
        print(f"Failed to fetch /auth/me: {me_resp.status_code}")

    # For seller, we might need ma_gian_hang or seller_id
    shop_id = me_data.get('ma_gian_hang')
    print(f"User ID: {user_id}, Shop ID: {shop_id}")

    # Test endpoints with potential IDs
    params_to_test = [
        {},
        {"seller_id": user_id},
        {"ma_gian_hang": shop_id} if shop_id else None,
        {"buyer_id": user_id}, # Just in case it's mis-labeled
    ]
    # Remove None
    params_to_test = [p for p in params_to_test if p is not None]

    endpoints = [
        "/seller/orders",
        "/seller/orders/",
        "/orders",
        "/orders/"
    ]

    combined_results = []
    for ep in endpoints:
        for params in params_to_test:
            url = f"{BASE_URL}{ep}"
            print(f"Testing GET {url} with params {params}...")
            try:
                resp = requests.get(url, headers=headers, params=params)
                combined_results.append({
                    "url": url,
                    "params": params,
                    "status": resp.status_code,
                    "body_preview": resp.text[:200]
                })
                print(f"Result: {resp.status_code}")
                if resp.status_code == 200:
                    print(f"FOUND WORKING ENDPOINT!")
            except Exception as e:
                print(f"Error testing {url}: {e}")

    with open('seller_orders_complex_results.json', 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)
    
    print(f"Test complete. Results saved to seller_orders_complex_results.json")

if __name__ == "__main__":
    test_seller_orders()
