#!/usr/bin/env python3
"""
Apple Store Stock Monitor - Clean, API-based monitoring system
No hardcoded products or stores - everything discovered dynamically
"""

import json
import time
from datetime import datetime
from typing import Dict, List
from dynamic_apple_monitor import DynamicAppleMonitor
from restock_analyzer import RestockAnalyzer


class AppleStockMonitor:
    """Main Apple stock monitoring system - fully API-based."""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.monitor = DynamicAppleMonitor()
        self.analyzer = RestockAnalyzer()
        self.config = self._load_or_create_config()

    def _load_or_create_config(self) -> Dict:
        """Load configuration or create default."""
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Create minimal default config
            default_config = {
                "products_to_monitor": [],
                "stores_to_monitor": [],
                "check_interval_minutes": 10,
                "notifications": {"sms_gateway_url": "http://localhost:5000"},
            }
            self._save_config(default_config)
            return default_config

    def _save_config(self, config: Dict = None):
        """Save configuration."""
        if config is None:
            config = self.config

        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=2)

    def discover_products(self, search_term: str = None) -> List[Dict]:
        """Discover Apple products dynamically."""
        print("🔍 Discovering Apple products...")

        if search_term:
            products = self.monitor.search_products(search_term)
            print(f"📱 Found {len(products)} products matching '{search_term}'")
        else:
            # Discover all products
            all_products = self.monitor.discover_all_apple_products()
            products = []
            for category, category_products in all_products.items():
                products.extend(category_products)
            print(f"📱 Discovered {len(products)} total products")

        return products

    def discover_stores(self, zipcode: str = "10001") -> List[Dict]:
        """Discover Apple stores dynamically."""
        print(f"🏪 Discovering Apple stores near {zipcode}...")

        stores = self.monitor.discover_all_apple_stores(zipcode)
        print(f"🏪 Found {len(stores)} stores")

        return stores

    def add_product(self, product_code: str, product_name: str):
        """Add a product to monitoring."""
        product = {
            "product_code": product_code,
            "product_name": product_name,
            "category": self._detect_category(product_name),
        }

        if product not in self.config["products_to_monitor"]:
            self.config["products_to_monitor"].append(product)
            self._save_config()
            print(f"✅ Added product: {product_name}")
        else:
            print(f"⚠️  Product already being monitored: {product_name}")

    def add_store(
        self, store_code: str, store_name: str, city: str = "", state: str = ""
    ):
        """Add a store to monitoring."""
        store = {
            "store_code": store_code,
            "store_name": store_name,
            "city": city,
            "state": state,
        }

        if store not in self.config["stores_to_monitor"]:
            self.config["stores_to_monitor"].append(store)
            self._save_config()
            print(f"✅ Added store: {store_name}")
        else:
            print(f"⚠️  Store already being monitored: {store_name}")

    def _detect_category(self, product_name: str) -> str:
        """Detect product category."""
        name_lower = product_name.lower()
        if "iphone" in name_lower:
            return "iphone"
        elif "ipad" in name_lower:
            return "ipad"
        elif "mac" in name_lower:
            return "mac"
        elif "watch" in name_lower:
            return "watch"
        elif "airpods" in name_lower:
            return "airpods"
        return "unknown"

    def check_stock(self) -> Dict:
        """Check stock for all configured products and stores."""
        if not self.config["products_to_monitor"]:
            print("❌ No products configured for monitoring")
            return {"error": "No products configured"}

        if not self.config["stores_to_monitor"]:
            print("❌ No stores configured for monitoring")
            return {"error": "No stores configured"}

        print(
            f"🔄 Checking {len(self.config['products_to_monitor'])} products at {len(self.config['stores_to_monitor'])} stores..."
        )

        results = {
            "timestamp": datetime.now().isoformat(),
            "available_items": [],
            "individual_results": {},
        }

        for product in self.config["products_to_monitor"]:
            for store in self.config["stores_to_monitor"]:
                try:
                    result = self.monitor.check_product_availability(
                        product["product_code"], store["store_code"]
                    )

                    key = f"{product['product_code']}_{store['store_code']}"
                    results["individual_results"][key] = {
                        "product_name": product["product_name"],
                        "store_name": store["store_name"],
                        "available": result.get("available", False),
                        "status": result.get("status", "unknown"),
                        "timestamp": result.get(
                            "timestamp", datetime.now().isoformat()
                        ),
                    }

                    if result.get("available", False):
                        results["available_items"].append(
                            {
                                "product": product["product_name"],
                                "store": store["store_name"],
                                "product_code": product["product_code"],
                                "store_code": store["store_code"],
                            }
                        )

                        print(
                            f"✅ {product['product_name']} available at {store['store_name']}"
                        )

                    # Record for pattern analysis
                    self.analyzer.record_stock_check(
                        store["store_code"],
                        product["product_code"],
                        result.get("available", False),
                    )

                except Exception as e:
                    print(
                        f"❌ Error checking {product['product_name']} at {store['store_name']}: {e}"
                    )

                time.sleep(1)  # Rate limiting

        total_available = len(results["available_items"])
        print(f"📊 Check complete: {total_available} items available")

        return results

    def run_continuous_monitoring(self):
        """Run continuous monitoring."""
        interval_minutes = self.config.get("check_interval_minutes", 10)
        interval_seconds = interval_minutes * 60

        print(f"🚀 Starting continuous monitoring (every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop")

        try:
            cycle = 0
            while True:
                cycle += 1
                print(f"\n{'='*50}")
                print(f"MONITORING CYCLE #{cycle}")
                print(f"{'='*50}")

                results = self.check_stock()

                if results.get("available_items"):
                    print(
                        f"🎉 Found {len(results['available_items'])} available items!"
                    )
                else:
                    print("😴 No items currently available")

                print(f"⏰ Next check in {interval_minutes} minutes...")
                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            print(f"\n🛑 Monitoring stopped")

    def show_status(self):
        """Show current configuration and status."""
        print("📊 Apple Stock Monitor Status")
        print("=" * 40)

        print(f"\n📱 Products ({len(self.config['products_to_monitor'])}):")
        for product in self.config["products_to_monitor"]:
            print(f"   • {product['product_name']} ({product['product_code']})")

        print(f"\n🏪 Stores ({len(self.config['stores_to_monitor'])}):")
        for store in self.config["stores_to_monitor"]:
            print(f"   • {store['store_name']} ({store['store_code']})")

        print(
            f"\n⚙️  Check interval: {self.config.get('check_interval_minutes', 10)} minutes"
        )


def main():
    """Main entry point."""
    import sys

    monitor = AppleStockMonitor()

    if len(sys.argv) < 2:
        print("🍎 Apple Store Stock Monitor")
        print("Usage:")
        print("  python apple_monitor.py discover <search_term>  - Find products")
        print("  python apple_monitor.py stores <zipcode>        - Find stores")
        print("  python apple_monitor.py add-product <code> <name> - Add product")
        print("  python apple_monitor.py add-store <code> <name>   - Add store")
        print("  python apple_monitor.py check                   - Check stock once")
        print(
            "  python apple_monitor.py run                     - Continuous monitoring"
        )
        print("  python apple_monitor.py status                  - Show configuration")
        return

    command = sys.argv[1]

    if command == "discover":
        search_term = sys.argv[2] if len(sys.argv) > 2 else None
        products = monitor.discover_products(search_term)

        print("\n📱 Found products:")
        for product in products[:10]:  # Show first 10
            print(f"   {product['product_code']} - {product['product_name']}")

        if len(products) > 10:
            print(f"   ... and {len(products) - 10} more")

    elif command == "stores":
        zipcode = sys.argv[2] if len(sys.argv) > 2 else "10001"
        stores = monitor.discover_stores(zipcode)

        print("\n🏪 Found stores:")
        for store in stores:
            print(
                f"   {store['store_code']} - {store['store_name']} ({store['city']}, {store['state']})"
            )

    elif command == "add-product":
        if len(sys.argv) < 4:
            print("Usage: python apple_monitor.py add-product <code> <name>")
            return

        product_code = sys.argv[2]
        product_name = " ".join(sys.argv[3:])
        monitor.add_product(product_code, product_name)

    elif command == "add-store":
        if len(sys.argv) < 4:
            print("Usage: python apple_monitor.py add-store <code> <name>")
            return

        store_code = sys.argv[2]
        store_name = " ".join(sys.argv[3:])
        monitor.add_store(store_code, store_name)

    elif command == "check":
        monitor.check_stock()

    elif command == "run":
        monitor.run_continuous_monitoring()

    elif command == "status":
        monitor.show_status()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
