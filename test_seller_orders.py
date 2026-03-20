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

    token = response.json().get('token')
    print(f"Login successful, token retrieved.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Test endpoints
    endpoints = [
        "/seller/orders",
        "/seller/orders/",
        "/orders",
        "/orders/"
    ]

    results = {}
    for ep in endpoints:
        url = f"{BASE_URL}{ep}"
        print(f"Testing GET {url}...")
        try:
            resp = requests.get(url, headers=headers)
            results[url] = {
                "status": resp.status_code,
                "body": resp.text[:200]
            }
            print(f"Result: {resp.status_code}")
        except Exception as e:
            print(f"Error testing {url}: {e}")
            results[url] = {"error": str(e)}

    with open('seller_orders_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Test complete. Results saved to seller_orders_test_results.json")

if __name__ == "__main__":
    test_seller_orders()
