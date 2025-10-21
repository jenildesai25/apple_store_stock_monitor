#!/usr/bin/env python3
"""
Dynamic Apple Product Monitor - Automatically discovers products and stores
"""

import requests
import json
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time
from datetime import datetime
import sqlite3


class DynamicAppleMonitor:
    """Dynamically discover and monitor any Apple product at any store."""

    def __init__(self, db_path: str = "apple_products.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )
        self._init_database()

    def _init_database(self):
        """Initialize database to store discovered products and stores."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Products table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_code TEXT UNIQUE NOT NULL,
                product_name TEXT,
                category TEXT,
                price TEXT,
                url TEXT,
                discovered_date TEXT,
                last_verified TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        """
        )

        # Stores table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_code TEXT UNIQUE NOT NULL,
                store_name TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                latitude REAL,
                longitude REAL,
                discovered_date TEXT,
                last_verified TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        """
        )

        # Stock checks table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                store_code TEXT NOT NULL,
                product_code TEXT NOT NULL,
                available BOOLEAN NOT NULL,
                pickup_display TEXT,
                raw_response TEXT,
                FOREIGN KEY (store_code) REFERENCES stores (store_code),
                FOREIGN KEY (product_code) REFERENCES products (product_code)
            )
        """
        )

        conn.commit()
        conn.close()

    def discover_all_apple_products(self) -> Dict[str, List[Dict]]:
        """Discover all current Apple products across categories."""

        print("🔍 Discovering All Apple Products...")

        # Apple product categories to scan
        categories = {
            "iphone": [
                "iphone-17-pro",
                "iphone-17",
                "iphone-air",
                "iphone-16",
                "iphone-16-pro",
                "iphone-15-pro",
                "iphone-15",
            ],
            "ipad": ["ipad-pro", "ipad-air", "ipad", "ipad-mini"],
            "mac": [
                "macbook-air",
                "macbook-pro",
                "imac",
                "mac-mini",
                "mac-studio",
                "mac-pro",
            ],
            "watch": ["apple-watch-series-10", "apple-watch-se", "apple-watch-ultra"],
            "airpods": ["airpods-pro", "airpods", "airpods-max"],
        }

        all_products = {}

        for category, models in categories.items():
            print(f"\n📱 Scanning {category.upper()} products...")
            category_products = []

            for model in models:
                try:
                    products = self._discover_product_variants(category, model)
                    if products:
                        category_products.extend(products)
                        print(f"   ✅ {model}: {len(products)} variants")
                    else:
                        print(f"   ❌ {model}: No variants found")

                    time.sleep(1)  # Rate limiting

                except Exception as e:
                    print(f"   ❌ {model}: Error - {e}")

            if category_products:
                all_products[category] = category_products
                self._save_products_to_db(category_products, category)

        return all_products

    def _discover_product_variants(self, category: str, model: str) -> List[Dict]:
        """Discover all variants of a specific product model."""

        url = f"https://www.apple.com/shop/buy-{category}/{model}"

        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return []

            # Extract model codes
            model_pattern = r"[A-Z]{2}[0-9A-Z]{2}[0-9]LL/A"
            codes = list(set(re.findall(model_pattern, response.text)))

            if not codes:
                return []

            # Try to extract product names and details
            soup = BeautifulSoup(response.text, "html.parser")

            products = []
            for code in codes:
                # Try to find product details near the model code
                product_info = self._extract_product_details(
                    soup, code, model, category
                )

                products.append(
                    {
                        "product_code": code,
                        "product_name": product_info.get("name", f"{model} ({code})"),
                        "category": category,
                        "model": model,
                        "price": product_info.get("price", "Unknown"),
                        "url": url,
                        "discovered_date": datetime.now().isoformat(),
                    }
                )

            return products

        except Exception as e:
            print(f"Error discovering {model}: {e}")
            return []

    def _extract_product_details(
        self, soup: BeautifulSoup, code: str, model: str, category: str
    ) -> Dict:
        """Extract product details from the page."""

        # This is a simplified extraction - could be enhanced with more sophisticated parsing
        details = {
            "name": f"{model.replace('-', ' ').title()} ({code})",
            "price": "Unknown",
        }

        # Look for price information
        price_selectors = [".price", "[data-price]", ".pricing", ".cost"]

        for selector in price_selectors:
            price_elements = soup.select(selector)
            if price_elements:
                price_text = price_elements[0].get_text(strip=True)
                if "$" in price_text:
                    details["price"] = price_text
                    break

        return details

    def discover_all_apple_stores(self, zipcode: str = "10001") -> List[Dict]:
        """Discover all Apple stores near a zipcode."""

        print(f"🏪 Discovering Apple Stores near {zipcode}...")

        url = "https://www.apple.com/shop/retail/pickup-message"
        params = {"location": zipcode}

        try:
            response = self.session.get(url, params=params, timeout=15)
            if response.status_code != 200:
                return []

            data = response.json()

            if "body" not in data or "availabilityStores" not in data["body"]:
                return []

            store_codes = data["body"]["availabilityStores"].split(",")
            stores = []

            print(f"   Found {len(store_codes)} stores")

            # Get detailed store information
            for store_code in store_codes:
                store_info = self._get_store_details(store_code, zipcode)
                if store_info:
                    stores.append(store_info)

            self._save_stores_to_db(stores)
            return stores

        except Exception as e:
            print(f"Error discovering stores: {e}")
            return []

    def _get_store_details(
        self, store_code: str, zipcode: str = "10001"
    ) -> Optional[Dict]:
        """Get detailed information about a specific store."""

        # Try to get store details by making a pickup request with zipcode
        url = "https://www.apple.com/shop/retail/pickup-message"
        params = {
            "parts.0": "MFXP4LL/A",  # Use a known working product code
            "location": zipcode,  # Use zipcode, not store code
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code != 200:
                return None

            data = response.json()

            if "body" in data and "stores" in data["body"]:
                for store in data["body"]["stores"]:
                    if store.get("storeNumber") == store_code:
                        return {
                            "store_code": store_code,
                            "store_name": store.get("storeName", "Unknown"),
                            "city": store.get("city", "Unknown"),
                            "state": store.get("state", "Unknown"),
                            "country": store.get("country", "US"),
                            "latitude": store.get("latitude"),
                            "longitude": store.get("longitude"),
                            "discovered_date": datetime.now().isoformat(),
                        }

            return None

        except Exception as e:
            print(f"Error getting details for store {store_code}: {e}")
            return None

    def _save_products_to_db(self, products: List[Dict], category: str):
        """Save discovered products to database."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for product in products:
            cursor.execute(
                """
                INSERT OR REPLACE INTO products 
                (product_code, product_name, category, price, url, discovered_date, last_verified, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    product["product_code"],
                    product["product_name"],
                    product["category"],
                    product["price"],
                    product["url"],
                    product["discovered_date"],
                    datetime.now().isoformat(),
                    1,
                ),
            )

        conn.commit()
        conn.close()

    def _save_stores_to_db(self, stores: List[Dict]):
        """Save discovered stores to database."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for store in stores:
            cursor.execute(
                """
                INSERT OR REPLACE INTO stores 
                (store_code, store_name, city, state, country, latitude, longitude, discovered_date, last_verified, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    store["store_code"],
                    store["store_name"],
                    store["city"],
                    store["state"],
                    store["country"],
                    store["latitude"],
                    store["longitude"],
                    store["discovered_date"],
                    datetime.now().isoformat(),
                    1,
                ),
            )

        conn.commit()
        conn.close()

    def get_products_by_category(self, category: str = None) -> List[Dict]:
        """Get products from database, optionally filtered by category."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute(
                """
                SELECT product_code, product_name, category, price, url, discovered_date
                FROM products 
                WHERE category = ? AND is_active = 1
                ORDER BY product_name
            """,
                (category,),
            )
        else:
            cursor.execute(
                """
                SELECT product_code, product_name, category, price, url, discovered_date
                FROM products 
                WHERE is_active = 1
                ORDER BY category, product_name
            """
            )

        products = []
        for row in cursor.fetchall():
            products.append(
                {
                    "product_code": row[0],
                    "product_name": row[1],
                    "category": row[2],
                    "price": row[3],
                    "url": row[4],
                    "discovered_date": row[5],
                }
            )

        conn.close()
        return products

    def get_stores_by_location(self, state: str = None) -> List[Dict]:
        """Get stores from database, optionally filtered by state."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if state:
            cursor.execute(
                """
                SELECT store_code, store_name, city, state, country, latitude, longitude
                FROM stores 
                WHERE state = ? AND is_active = 1
                ORDER BY store_name
            """,
                (state,),
            )
        else:
            cursor.execute(
                """
                SELECT store_code, store_name, city, state, country, latitude, longitude
                FROM stores 
                WHERE is_active = 1
                ORDER BY state, city, store_name
            """
            )

        stores = []
        for row in cursor.fetchall():
            stores.append(
                {
                    "store_code": row[0],
                    "store_name": row[1],
                    "city": row[2],
                    "state": row[3],
                    "country": row[4],
                    "latitude": row[5],
                    "longitude": row[6],
                }
            )

        conn.close()
        return stores

    def check_product_availability(self, product_code: str, store_code: str) -> Dict:
        """Check if a specific product is available at a specific store."""

        url = "https://www.apple.com/shop/retail/pickup-message"
        params = {
            "parts.0": product_code,
            "location": "10001",  # Use NYC zipcode to get all stores
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if "body" in data and "stores" in data["body"]:
                for store in data["body"]["stores"]:
                    if store.get("storeNumber") == store_code:
                        parts_availability = store.get("partsAvailability", {})
                        if product_code in parts_availability:
                            part_info = parts_availability[product_code]
                            pickup_display = part_info.get(
                                "pickupDisplay", "unavailable"
                            )

                            # Save to database
                            self._save_stock_check(
                                store_code,
                                product_code,
                                pickup_display == "available",
                                pickup_display,
                                json.dumps(data),
                            )

                            return {
                                "available": pickup_display == "available",
                                "status": pickup_display,
                                "store_name": store.get("storeName", ""),
                                "store_code": store_code,
                                "product_code": product_code,
                                "timestamp": datetime.now().isoformat(),
                            }

            return {
                "available": False,
                "status": "not_found",
                "store_code": store_code,
                "product_code": product_code,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "available": False,
                "status": "error",
                "error": str(e),
                "store_code": store_code,
                "product_code": product_code,
                "timestamp": datetime.now().isoformat(),
            }

    def _save_stock_check(
        self,
        store_code: str,
        product_code: str,
        available: bool,
        pickup_display: str,
        raw_response: str,
    ):
        """Save stock check result to database."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO stock_checks 
            (timestamp, store_code, product_code, available, pickup_display, raw_response)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                datetime.now().isoformat(),
                store_code,
                product_code,
                available,
                pickup_display,
                raw_response,
            ),
        )

        conn.commit()
        conn.close()

    def search_products(self, search_term: str) -> List[Dict]:
        """Search for products by name or model."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT product_code, product_name, category, price, url
            FROM products 
            WHERE (product_name LIKE ? OR product_code LIKE ?) AND is_active = 1
            ORDER BY product_name
        """,
            (f"%{search_term}%", f"%{search_term}%"),
        )

        products = []
        for row in cursor.fetchall():
            products.append(
                {
                    "product_code": row[0],
                    "product_name": row[1],
                    "category": row[2],
                    "price": row[3],
                    "url": row[4],
                }
            )

        conn.close()
        return products


def main():
    """Demonstrate the dynamic Apple monitor."""

    print("🍎 Dynamic Apple Product Monitor")
    print("=" * 50)

    monitor = DynamicAppleMonitor()

    # Discover all products
    print("\n1. Discovering all Apple products...")
    all_products = monitor.discover_all_apple_products()

    total_products = sum(len(products) for products in all_products.values())
    print(
        f"\n✅ Discovered {total_products} products across {len(all_products)} categories"
    )

    for category, products in all_products.items():
        print(f"   📱 {category}: {len(products)} products")

    # Discover stores
    print("\n2. Discovering Apple stores...")
    stores = monitor.discover_all_apple_stores("10001")  # NYC area
    print(f"✅ Discovered {len(stores)} stores")

    # Show some examples
    print("\n3. Example products:")
    iphone_products = monitor.get_products_by_category("iphone")
    for product in iphone_products[:5]:
        print(f"   📱 {product['product_name']} - {product['product_code']}")

    print("\n4. Example stores:")
    for store in stores[:5]:
        print(
            f"   🏪 {store['store_name']} ({store['store_code']}) - {store['city']}, {store['state']}"
        )

    # Test availability check
    if iphone_products and stores:
        print("\n5. Testing availability check...")
        test_product = iphone_products[0]
        test_store = stores[0]

        result = monitor.check_product_availability(
            test_product["product_code"], test_store["store_code"]
        )

        status_icon = "✅" if result["available"] else "❌"
        print(
            f"   {status_icon} {test_product['product_name']} at {test_store['store_name']}: {result['status']}"
        )

    print(f"\n💡 All data saved to database: {monitor.db_path}")
    print("🔄 Run this script regularly to keep product and store data updated")


if __name__ == "__main__":
    main()
