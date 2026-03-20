import requests
import json

def test_image_working():
    urls = [
        "http://207.180.233.84/uploads/ingredients/NL3018.jpg",
        "http://207.180.233.84:8000/uploads/ingredients/NL3018.jpg"
    ]
    
    results = {}
    for url in urls:
        print(f"Testing URL: {url}")
        try:
            response = requests.head(url, timeout=5)
            results[url] = response.status_code
        except Exception as e:
            results[url] = str(e)
            
    with open('image_working_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Saved to image_working_results.json")

if __name__ == "__main__":
    test_image_working()
