"""Apple Store stock monitoring logic - API-based, no hardcoded data."""

import logging
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# Add the project root to the path to import our dynamic modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from dynamic_apple_monitor import DynamicAppleMonitor

    DYNAMIC_FEATURES_AVAILABLE = True
except ImportError:
    DYNAMIC_FEATURES_AVAILABLE = False

_LOGGER = logging.getLogger(__name__)


class AppleStoreMonitor:
    """Monitor Apple Store stock availability using API-based discovery."""

    def __init__(
        self,
        stores: List[str],
        products: List[str],
        sms_gateway_url: Optional[str] = None,
    ):
        """Initialize the monitor."""
        self.stores = stores
        self.products = products
        self.sms_gateway_url = sms_gateway_url

        # Initialize dynamic monitor for API-based operations
        if DYNAMIC_FEATURES_AVAILABLE:
            self.dynamic_monitor = DynamicAppleMonitor()
            _LOGGER.info("Dynamic API-based monitoring enabled")
        else:
            self.dynamic_monitor = None
            _LOGGER.error(
                "Dynamic monitoring not available - system will not work properly"
            )

    def check_stock(self) -> Dict:
        """Check stock for all configured stores and products with individual tracking."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "stores_checked": len(self.stores),
            "products_checked": len(self.products),
            "available_items": [],
            "total_available": 0,
            "individual_results": {},  # Individual product/store tracking
            "last_check_times": {},  # Last check time for each product
            "product_details": {},  # Product information for each item
        }

        if not self.dynamic_monitor:
            _LOGGER.error("Dynamic monitor not available - cannot check stock")
            return results

        for store_name in self.stores:
            # Get store code dynamically
            store_code = self._get_store_code(store_name)
            if not store_code:
                _LOGGER.warning(f"Could not find store code for: {store_name}")
                continue

            for product_name in self.products:
                # Get product code dynamically
                product_code = self._get_product_code(product_name)
                if not product_code:
                    _LOGGER.warning(f"Could not find product code for: {product_name}")
                    continue

                # Create unique key for this product/store combination
                product_store_key = f"{product_code}_{store_code}"
                check_timestamp = datetime.now().isoformat()

                try:
                    # Use dynamic monitor for availability check
                    availability_result = (
                        self.dynamic_monitor.check_product_availability(
                            product_code, store_code
                        )
                    )

                    # Individual tracking for each product/store combination
                    individual_result = {
                        "product_name": product_name,
                        "product_code": product_code,
                        "store_name": store_name,
                        "store_code": store_code,
                        "available": availability_result.get("available", False),
                        "status": availability_result.get("status", "unknown"),
                        "last_checked": check_timestamp,
                        "pickup_available": availability_result.get("available", False),
                        "api_response": availability_result,
                    }

                    results["individual_results"][product_store_key] = individual_result
                    results["last_check_times"][product_code] = check_timestamp
                    results["product_details"][product_code] = {
                        "name": product_name,
                        "code": product_code,
                        "category": self._detect_product_category(product_name),
                    }

                    if availability_result.get("available", False):
                        item = {
                            "store": store_name,
                            "product": product_name,
                            "product_code": product_code,
                            "store_code": store_code,
                            "available": True,
                            "pickup_available": True,
                            "last_checked": check_timestamp,
                        }
                        results["available_items"].append(item)
                        results["total_available"] += 1

                        # Send notification if SMS gateway is configured
                        if self.sms_gateway_url:
                            self._send_sms_notification(store_name, product_name)

                        _LOGGER.info(f"Stock available: {product_name} at {store_name}")

                except Exception as e:
                    _LOGGER.error(f"Error checking {product_name} at {store_name}: {e}")

                    # Still record the failed check for individual tracking
                    individual_result = {
                        "product_name": product_name,
                        "product_code": product_code,
                        "store_name": store_name,
                        "store_code": store_code,
                        "available": False,
                        "status": "error",
                        "last_checked": check_timestamp,
                        "error": str(e),
                        "pickup_available": False,
                    }
                    results["individual_results"][product_store_key] = individual_result

                # Rate limiting
                time.sleep(1)

        return results

    def _get_store_code(self, store_name: str) -> Optional[str]:
        """Get store code dynamically from database or API."""
        if not self.dynamic_monitor:
            return None

        try:
            # First try to get from database
            stores = self.dynamic_monitor.get_stores_by_location()
            for store in stores:
                if store["store_name"].lower() == store_name.lower():
                    return store["store_code"]

            # If not found, try to discover stores and search again
            _LOGGER.info(
                f"Store '{store_name}' not in database, attempting discovery..."
            )

            # Try to discover stores near common zipcodes
            test_zipcodes = [
                "10001",
                "90210",
                "97223",
                "60601",
                "33101",
            ]  # Major cities

            for zipcode in test_zipcodes:
                discovered_stores = self.dynamic_monitor.discover_all_apple_stores(
                    zipcode
                )
                for store in discovered_stores:
                    if store["store_name"].lower() == store_name.lower():
                        return store["store_code"]

            _LOGGER.warning(f"Could not find store code for: {store_name}")
            return None

        except Exception as e:
            _LOGGER.error(f"Error getting store code for {store_name}: {e}")
            return None

    def _get_product_code(self, product_name: str) -> Optional[str]:
        """Get product code dynamically from database or API."""
        if not self.dynamic_monitor:
            return None

        try:
            # First try exact search in database
            products = self.dynamic_monitor.search_products(product_name)
            if products:
                # Return the first exact match
                for product in products:
                    if product["product_name"].lower() == product_name.lower():
                        return product["product_code"]
                # If no exact match, return first partial match
                return products[0]["product_code"]

            # If not found, try to discover products
            _LOGGER.info(
                f"Product '{product_name}' not in database, attempting discovery..."
            )

            # Try to discover products by category
            category = self._detect_product_category(product_name)
            if category:
                self.dynamic_monitor.discover_all_apple_products()

                # Search again after discovery
                products = self.dynamic_monitor.search_products(product_name)
                if products:
                    return products[0]["product_code"]

            _LOGGER.warning(f"Could not find product code for: {product_name}")
            return None

        except Exception as e:
            _LOGGER.error(f"Error getting product code for {product_name}: {e}")
            return None

    def _detect_product_category(self, product_name: str) -> str:
        """Detect product category from name."""
        product_lower = product_name.lower()

        if "iphone" in product_lower:
            return "iphone"
        elif "ipad" in product_lower:
            return "ipad"
        elif (
            "macbook" in product_lower
            or "imac" in product_lower
            or "mac" in product_lower
        ):
            return "mac"
        elif "watch" in product_lower:
            return "watch"
        elif "airpods" in product_lower:
            return "airpods"
        else:
            return "unknown"

    def _send_sms_notification(self, store_name: str, product_name: str):
        """Send SMS notification via the SMS gateway."""
        if not self.sms_gateway_url:
            return

        message = f"🍎 STOCK ALERT: {product_name} is available for pickup at Apple {store_name}!"

        try:
            response = requests.post(
                f"{self.sms_gateway_url}/send_sms",
                json={"message": message},
                timeout=10,
            )

            if response.status_code == 200:
                _LOGGER.info(f"SMS notification sent: {message}")
            else:
                _LOGGER.error(f"Failed to send SMS: {response.status_code}")

        except Exception as e:
            _LOGGER.error(f"Error sending SMS notification: {e}")

    def get_restock_predictions(self) -> Dict:
        """Get restock predictions for all monitored products."""
        if not self.dynamic_monitor:
            return {"error": "Dynamic monitoring not available"}

        predictions = {"timestamp": datetime.now().isoformat(), "predictions": []}

        for store_name in self.stores:
            store_code = self._get_store_code(store_name)
            if not store_code:
                continue

            for product_name in self.products:
                product_code = self._get_product_code(product_name)
                if not product_code:
                    continue

                try:
                    # Use the restock analyzer if available
                    if hasattr(self.dynamic_monitor, "analyzer"):
                        patterns = self.dynamic_monitor.analyzer.get_restock_patterns(
                            store_code, product_code
                        )
                        prediction = self.dynamic_monitor.analyzer.predict_next_restock(
                            store_code, product_code
                        )
                    else:
                        patterns = {"message": "Pattern analysis not available"}
                        prediction = {"prediction": "Prediction not available"}

                    prediction_summary = {
                        "store": store_name,
                        "product": product_name,
                        "store_code": store_code,
                        "product_code": product_code,
                        "patterns": patterns,
                        "prediction": prediction,
                    }

                    predictions["predictions"].append(prediction_summary)

                except Exception as e:
                    _LOGGER.error(
                        f"Error getting prediction for {product_name} at {store_name}: {e}"
                    )

        return predictions
