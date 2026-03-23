import requests
import json

# Mimic AppConfig
IMAGE_BASE_URL = "http://207.180.233.84"

def parse_image_url(value):
    if not value or str(value).strip() == "":
        return ""
    path = str(value)
    if path.startswith('http'):
        return path
    return f"{IMAGE_BASE_URL}{'' if path.startswith('/') else '/'}{path}"

def verify_images():
    # Test specific seller products
    seller_test_paths = [
        ("Phi lê cá ngừ", "https://example.com/item.jpg"),
        ("Lá cẩm", "http://207.180.233.84/uploads/ingredients/NL1831.jpg"),
        ("Ba rọi rút sườn (NL1455 - CONTROL)", "uploads/ingredients/NL1455.jpg")
    ]
    
    print(f"Final Verification Results:")
    for name, raw_url in seller_test_paths:
        parsed_url = parse_image_url(raw_url)
        try:
            resp = requests.head(parsed_url, timeout=5)
            status = resp.status_code
        except Exception as e:
            status = str(e)[:20]
        print(f"- {name}: {status} -> {parsed_url}")

if __name__ == "__main__":
    verify_images()
