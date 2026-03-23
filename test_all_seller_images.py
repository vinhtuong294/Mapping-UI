import requests
import json

def test_all_seller_images():
    try:
        with open('seller_products_output.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        products = data.get('data', [])
        print(f"Testing {len(products)} product images...")
        
        results = []
        for p in products:
            url = p.get('hinh_anh')
            name = p.get('ten_nguyen_lieu')
            ma = p.get('ma_nguyen_lieu')
            
            if not url:
                results.append({"id": ma, "name": name, "url": "NULL", "status": "MISSING"})
                continue
                
            try:
                resp = requests.head(url, timeout=5)
                results.append({"id": ma, "name": name, "url": url, "status": resp.status_code})
            except Exception as e:
                results.append({"id": ma, "name": name, "url": url, "status": str(e)})
                
        with open('seller_image_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("Done. Results saved to seller_image_test_results.json")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_all_seller_images()
