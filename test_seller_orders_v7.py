import requests
import json

def diagnose():
    login_data = {"ten_dang_nhap": "hieunguoiban", "mat_khau": "Trinh123456@"}
    
    ports = [80, 8000]
    base_urls = [f"http://207.180.233.84:{p}/api" if p != 80 else "http://207.180.233.84/api" for p in ports]
    
    results = []
    for b_url in base_urls:
        print(f"Testing Base URL: {b_url}")
        try:
            # Try login
            lr = requests.post(f"{b_url}/auth/login", json=login_data, timeout=5)
            if lr.status_code == 200:
                print(f"  Login SUCCESS on {b_url}")
                token = lr.json()['token']
                headers = {"Authorization": f"Bearer {token}"}
                
                # Try orders
                # Note: OrderService uses sellerBaseUrl + /orders
                # SellerOrderService (Step 1904) uses: uri = Uri.parse('$_baseUrl/orders')
                # where _baseUrl is /api/seller
                
                # Test both /api/seller/orders and /api/seller/orders/
                for ep in ["/seller/orders", "/seller/orders/"]:
                    url = f"{b_url}{ep}"
                    or_resp = requests.get(url, headers=headers, timeout=5)
                    print(f"    GET {url} -> {or_resp.status_code}")
                    if or_resp.status_code == 200:
                        print(f"      SUCCESS! Data: {or_resp.text[:100]}")
            else:
                print(f"  Login FAILED on {b_url} -> {lr.status_code}")
        except Exception as e:
            print(f"  Error on {b_url}: {e}")

if __name__ == "__main__":
    diagnose()
