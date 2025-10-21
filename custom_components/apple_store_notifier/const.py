"""Constants for Apple Store Notifier."""

DOMAIN = "apple_store_notifier"
PLATFORMS = ["sensor", "binary_sensor"]

# Configuration keys
CONF_STORES = "stores"
CONF_PRODUCTS = "products"
CONF_SMS_GATEWAY_URL = "sms_gateway_url"
CONF_CHECK_INTERVAL = "check_interval"
CONF_PHONE_NUMBERS = "phone_numbers"

# Default values
DEFAULT_CHECK_INTERVAL = 10  # 10 minutes for less frequent checks
DEFAULT_SMS_GATEWAY_URL = "http://192.168.1.100:5000"

# API Configuration
APPLE_PICKUP_API_URL = "https://www.apple.com/shop/retail/pickup-message"
APPLE_STORE_DISCOVERY_ZIPCODE = "10001"  # Default zipcode for store discovery

# Database paths
PRODUCTS_DB_PATH = "apple_products.db"
RESTOCK_DB_PATH = "restock_history.db"
