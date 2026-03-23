import requests
import json

def test_nominatim():
    query = "Nguyễn Văn Linh, Đà Nẵng"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5&addressdetails=1&accept-language=vi"
    headers = {
        'User-Agent': 'DNGO-App/1.0.0 (vinh.tranh@example.com)'
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
                print(f"   Coords: {result.get('lat')}, {result.get('lon')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_nominatim()
