"""Apple Store stock monitoring logic."""

import logging
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional

_LOGGER = logging.getLogger(__name__)


class AppleStoreMonitor:
    """Monitor Apple Store stock availability."""

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
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )

    def check_stock(self) -> Dict:
        """Check stock for all configured stores and products."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "stores_checked": len(self.stores),
            "products_checked": len(self.products),
            "available_items": [],
            "total_available": 0,
        }

        from .const import APPLE_STORES, IPHONE_MODELS

        for store_name in self.stores:
            store_code = APPLE_STORES.get(store_name)
            if not store_code:
                continue

            for product_name in self.products:
                product_code = IPHONE_MODELS.get(product_name)
                if not product_code:
                    continue

                try:
                    availability = self._check_product_availability(
                        store_code, product_code
                    )

                    if availability:
                        item = {
                            "store": store_name,
                            "product": product_name,
                            "available": True,
                            "pickup_available": availability.get(
                                "pickup_available", False
                            ),
                        }
                        results["available_items"].append(item)
                        results["total_available"] += 1

                        # Send notification if SMS gateway is configured
                        if self.sms_gateway_url:
                            self._send_sms_notification(store_name, product_name)

                        _LOGGER.info(f"Stock available: {product_name} at {store_name}")

                except Exception as e:
                    _LOGGER.error(f"Error checking {product_name} at {store_name}: {e}")

                # Rate limiting
                time.sleep(1)

        return results

    def _check_product_availability(
        self, store_code: str, product_code: str
    ) -> Optional[Dict]:
        """Check if a specific product is available at a specific store."""
        url = f"https://www.apple.com/shop/retail/pickup-message"

        params = {
            "pl": "true",
            "mts.0": "regular",
            "mts.1": "compact",
            "cppart": "UNLOCKED/US",
            "parts.0": product_code,
            "location": store_code,
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Parse Apple's response format
            if "body" in data and "stores" in data["body"]:
                for store in data["body"]["stores"]:
                    if store.get("storeNumber") == store_code:
                        parts_availability = store.get("partsAvailability", {})
                        if product_code in parts_availability:
                            part_info = parts_availability[product_code]
                            if part_info.get("pickupDisplay") == "available":
                                return {"pickup_available": True, "store_info": store}

            return None

        except Exception as e:
            _LOGGER.error(f"Error checking availability: {e}")
            return None

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
