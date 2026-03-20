import requests
import json

def test_nominatim():
    query = "Nguyễn Văn Linh, Đà Nẵng"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5&addressdetails=1&accept-language=vi"
    # Try a more browser-like User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"Testing Nominatim API with query: {query}")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} results.")
            for i, result in enumerate(data):
                print(f"{i+1}. {result.get('display_name')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_nominatim()
