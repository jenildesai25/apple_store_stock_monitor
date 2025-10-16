#!/usr/bin/env python3
"""Debug Apple Store API response format."""

import requests
import json


def debug_apple_api():
    """Debug the actual Apple Store API response."""

    # Test with Washington Square, Tigard
    store_code = "R090"
    product_code = "MG7Q4LL/A"  # iPhone 17 Pro 512GB Deep Blue

    url = "https://www.apple.com/shop/retail/pickup-message"
    params = {
        "pl": "true",
        "mts.0": "regular",
        "mts.1": "compact",
        "cppart": "UNLOCKED/US",
        "parts.0": product_code,
        "location": store_code,
    }

    print(f"🔍 Testing Apple API with:")
    print(f"   Store: {store_code}")
    print(f"   Product: {product_code}")
    print(f"   URL: {url}")
    print(f"   Params: {params}")

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"📡 Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\n📄 Response JSON Structure:")
                print(
                    json.dumps(data, indent=2)[:1000] + "..."
                    if len(str(data)) > 1000
                    else json.dumps(data, indent=2)
                )
            except:
                print(f"\n📄 Response Text (not JSON):")
                print(
                    response.text[:500] + "..."
                    if len(response.text) > 500
                    else response.text
                )
        else:
            print(f"\n❌ Error Response: {response.text}")

    except Exception as e:
        print(f"\n❌ Exception: {e}")


if __name__ == "__main__":
    debug_apple_api()
