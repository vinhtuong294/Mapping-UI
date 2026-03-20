import requests
import json

def test_image_ports():
    urls = [
        "http://207.180.233.84/uploads/ingredients/NL1831.jpg",
        "http://207.180.233.84:8000/uploads/ingredients/NL1831.jpg"
    ]
    
    results = {}
    for url in urls:
        print(f"Testing URL: {url}")
        try:
            response = requests.head(url, timeout=5)
            results[url] = response.status_code
        except Exception as e:
            results[url] = str(e)
            
    with open('image_ports_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Done. Saved to image_ports_results.json")

if __name__ == "__main__":
    test_image_ports()
