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

# Apple Store URLs and data
APPLE_STORES = {
    "Fifth Avenue": "R409",
    "SoHo": "R014",
    "Upper West Side": "R018",
    "Brooklyn": "R447",
    "Staten Island": "R117",
    "Queens Center": "R015",
}

IPHONE_MODELS = {
    "iPhone 15 Pro 128GB Natural Titanium": "MU2F3LL/A",
    "iPhone 15 Pro 256GB Natural Titanium": "MU2G3LL/A",
    "iPhone 15 Pro 512GB Natural Titanium": "MU2H3LL/A",
    "iPhone 15 Pro 1TB Natural Titanium": "MU2J3LL/A",
    "iPhone 15 Pro Max 256GB Natural Titanium": "MU2T3LL/A",
    "iPhone 15 Pro Max 512GB Natural Titanium": "MU2U3LL/A",
    "iPhone 15 Pro Max 1TB Natural Titanium": "MU2V3LL/A",
}
