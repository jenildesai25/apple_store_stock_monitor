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
    "Washington Square, Tigard": "R090",
    "Pioneer Place, Portland": "R191",
    "Bridgeport Village, Tigard": "R447",
    "Clackamas Town Center": "R342",
    "Lloyd Center, Portland": "R298",
    "Woodburn Premium Outlets": "R445",
    "Alderwood Mall, Lynnwood": "R234",
    "Bellevue Square": "R008",
    "University Village, Seattle": "R280",
}

IPHONE_MODELS = {
    # iPhone 17 Pro - Deep Blue
    "iPhone 17 Pro 128GB Deep Blue": "MG7P4LL/A",
    "iPhone 17 Pro 256GB Deep Blue": "MG7R4LL/A",
    "iPhone 17 Pro 512GB Deep Blue": "MG7Q4LL/A",
    "iPhone 17 Pro 1TB Deep Blue": "MG7S4LL/A",
    # iPhone 17 Pro - Natural Titanium
    "iPhone 17 Pro 128GB Natural Titanium": "MG7T4LL/A",
    "iPhone 17 Pro 256GB Natural Titanium": "MG7U4LL/A",
    "iPhone 17 Pro 512GB Natural Titanium": "MG7V4LL/A",
    "iPhone 17 Pro 1TB Natural Titanium": "MG7W4LL/A",
    # iPhone 17 Pro - White Titanium
    "iPhone 17 Pro 128GB White Titanium": "MG7X4LL/A",
    "iPhone 17 Pro 256GB White Titanium": "MG7Y4LL/A",
    "iPhone 17 Pro 512GB White Titanium": "MG7Z4LL/A",
    "iPhone 17 Pro 1TB White Titanium": "MG8A4LL/A",
    # iPhone 17 Pro - Black Titanium
    "iPhone 17 Pro 128GB Black Titanium": "MG8B4LL/A",
    "iPhone 17 Pro 256GB Black Titanium": "MG8C4LL/A",
    "iPhone 17 Pro 512GB Black Titanium": "MG8D4LL/A",
    "iPhone 17 Pro 1TB Black Titanium": "MG8E4LL/A",
    # iPhone 17 Pro Max - Deep Blue
    "iPhone 17 Pro Max 256GB Deep Blue": "MG8F4LL/A",
    "iPhone 17 Pro Max 512GB Deep Blue": "MG8G4LL/A",
    "iPhone 17 Pro Max 1TB Deep Blue": "MG8H4LL/A",
    # iPhone 17 Pro Max - Natural Titanium
    "iPhone 17 Pro Max 256GB Natural Titanium": "MG8J4LL/A",
    "iPhone 17 Pro Max 512GB Natural Titanium": "MG8K4LL/A",
    "iPhone 17 Pro Max 1TB Natural Titanium": "MG8L4LL/A",
    # iPhone 17 Pro Max - White Titanium
    "iPhone 17 Pro Max 256GB White Titanium": "MG8M4LL/A",
    "iPhone 17 Pro Max 512GB White Titanium": "MG8N4LL/A",
    "iPhone 17 Pro Max 1TB White Titanium": "MG8P4LL/A",
    # iPhone 17 Pro Max - Black Titanium
    "iPhone 17 Pro Max 256GB Black Titanium": "MG8Q4LL/A",
    "iPhone 17 Pro Max 512GB Black Titanium": "MG8R4LL/A",
    "iPhone 17 Pro Max 1TB Black Titanium": "MG8S4LL/A",
}
