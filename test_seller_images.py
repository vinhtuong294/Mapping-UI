import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def test_seller_products():
    # Login as seller
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "ten_dang_nhap": "hieunguoiban",
        "mat_khau": "Trinh123456@"
    }
    
    print(f"Logging in as {login_data['ten_dang_nhap']}...")
    print(f"URL: {login_url}")
    try:
        response = requests.post(login_url, json=login_data)
        print(f"Login Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Login Failed: {response.text}")
            return
            
        print(f"Token received. Getting data...")
        token = response.json().get('token')
        if not token:
            print(f"No token found in response: {response.json()}")
            return
            
        print(f"Token: {token[:20]}...")
            
        # Get seller products
        products_url = f"{BASE_URL}/seller/products?page=1&limit=5"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        print(f"Fetching seller products from: {products_url}")
        response = requests.get(products_url, headers=headers)
        print(f"Products Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            with open('seller_products_output.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Full response saved to seller_products_output.json")
        else:
            print(f"Failed to get products: {response.status_code}")
            print(f"Error Body: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_seller_products()
