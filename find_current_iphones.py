#!/usr/bin/env python3
"""Find current iPhone models available on Apple's website."""

import requests
from bs4 import BeautifulSoup
import re


def find_current_iphones():
    """Scrape Apple's iPhone page to find current models."""

    print("🔍 Checking Apple's iPhone page for current models...")

    try:
        # Check iPhone page
        url = "https://www.apple.com/iphone/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        print(f"📡 Status: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Look for iPhone model names
            iphone_links = soup.find_all("a", href=re.compile(r"/iphone-\d+"))

            print("\n📱 Current iPhone Models Found:")
            for link in iphone_links[:10]:  # Limit to first 10
                href = link.get("href", "")
                text = link.get_text(strip=True)
                if text and "iPhone" in text:
                    print(f"   • {text} -> {href}")

        # Also try the store page
        print(f"\n🏪 Checking Apple Store page...")
        store_url = "https://www.apple.com/shop/buy-iphone"
        response = requests.get(store_url, headers=headers, timeout=10)
        print(f"📡 Store Status: {response.status_code}")

        if response.status_code == 200:
            # Look for model numbers in the page
            model_pattern = r"[A-Z]{2}[0-9A-Z]{2}[0-9]LL/A"
            models = re.findall(model_pattern, response.text)

            if models:
                print(f"\n🔢 Model Numbers Found:")
                for model in set(models)[:10]:  # Unique models, limit 10
                    print(f"   • {model}")
            else:
                print("   No model numbers found in page source")

    except Exception as e:
        print(f"❌ Error: {e}")


def test_simple_api():
    """Test Apple API with minimal parameters."""

    print(f"\n🧪 Testing simplified API call...")

    # Try just getting store info without specific product
    url = "https://www.apple.com/shop/retail/pickup-message"
    params = {"location": "R409"}  # Fifth Avenue - known store

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"📡 Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"📄 Response keys: {list(data.keys())}")
            if "body" in data:
                print(f"📄 Body keys: {list(data['body'].keys())}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    find_current_iphones()
    test_simple_api()
