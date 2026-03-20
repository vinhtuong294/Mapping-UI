import requests
import json

BASE_URL = "http://207.180.233.84:8000/api"

def test_buyer_ingredients():
    # Login first
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "ten_dang_nhap": "hieunguoiban",
        "mat_khau": "Trinh123456@"
    }
    print(f"Logging in...")
    login_resp = requests.post(login_url, json=login_data)
    token = login_resp.json().get('token')
    
    headers = {"Authorization": f"Bearer {token}"}
    
    search_url = f"{BASE_URL}/buyer/nguyen-lieu?limit=50"
    
    print(f"Searching as buyer...")
    try:
        response = requests.get(search_url, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            with open('buyer_ingredients_output.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved to buyer_ingredients_output.json")
            
            items = data.get('data', [])
            print(f"Found {len(items)} items")
            for item in items:
                print(f"Name: {item.get('ten_nguyen_lieu')}")
                print(f"Image: {item.get('hinh_anh')}")
                print("-" * 20)
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_buyer_ingredients()
