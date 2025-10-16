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
# Apple Stores with coordinates for distance calculation
APPLE_STORES_DATA = {
    # Oregon
    "Washington Square, Tigard": {
        "code": "R090",
        "lat": 45.4515,
        "lon": -122.7645,
        "state": "OR",
    },
    "Pioneer Place, Portland": {
        "code": "R191",
        "lat": 45.5152,
        "lon": -122.6784,
        "state": "OR",
    },
    "Clackamas Town Center": {
        "code": "R342",
        "lat": 45.4373,
        "lon": -122.5706,
        "state": "OR",
    },
    # Washington
    "Alderwood Mall, Lynnwood": {
        "code": "R234",
        "lat": 47.8301,
        "lon": -122.2715,
        "state": "WA",
    },
    "Bellevue Square": {
        "code": "R008",
        "lat": 47.6162,
        "lon": -122.2054,
        "state": "WA",
    },
    "University Village, Seattle": {
        "code": "R280",
        "lat": 47.6606,
        "lon": -122.3045,
        "state": "WA",
    },
    "Southcenter, Tukwila": {
        "code": "R126",
        "lat": 47.4598,
        "lon": -122.2615,
        "state": "WA",
    },
    # California - Bay Area
    "Stonestown, San Francisco": {
        "code": "R191",
        "lat": 37.7281,
        "lon": -122.4661,
        "state": "CA",
    },
    "Union Square, San Francisco": {
        "code": "R081",
        "lat": 37.7879,
        "lon": -122.4075,
        "state": "CA",
    },
    "Walnut Creek": {"code": "R112", "lat": 37.9063, "lon": -122.0653, "state": "CA"},
    "Valley Fair, Santa Clara": {
        "code": "R200",
        "lat": 37.3255,
        "lon": -121.9456,
        "state": "CA",
    },
    "Stanford Shopping Center": {
        "code": "R028",
        "lat": 37.4419,
        "lon": -122.1430,
        "state": "CA",
    },
    # California - LA Area
    "Beverly Center": {"code": "R006", "lat": 34.0759, "lon": -118.3777, "state": "CA"},
    "Century City": {"code": "R018", "lat": 34.0522, "lon": -118.4161, "state": "CA"},
    "The Grove": {"code": "R094", "lat": 34.0719, "lon": -118.3560, "state": "CA"},
    "Santa Monica": {"code": "R123", "lat": 34.0195, "lon": -118.4912, "state": "CA"},
    "Pasadena": {"code": "R098", "lat": 34.1478, "lon": -118.1445, "state": "CA"},
    # New York
    "Fifth Avenue": {"code": "R409", "lat": 40.7648, "lon": -73.9731, "state": "NY"},
    "SoHo": {"code": "R014", "lat": 40.7230, "lon": -74.0020, "state": "NY"},
    "Upper West Side": {"code": "R018", "lat": 40.7812, "lon": -73.9665, "state": "NY"},
    "Brooklyn": {"code": "R447", "lat": 40.6892, "lon": -73.9442, "state": "NY"},
    "Staten Island": {"code": "R117", "lat": 40.5795, "lon": -74.1502, "state": "NY"},
    "Queens Center": {"code": "R015", "lat": 40.7342, "lon": -73.8648, "state": "NY"},
    # Texas
    "Domain, Austin": {"code": "R115", "lat": 30.4003, "lon": -97.7278, "state": "TX"},
    "Barton Creek, Austin": {
        "code": "R005",
        "lat": 30.3072,
        "lon": -97.8081,
        "state": "TX",
    },
    "NorthPark, Dallas": {
        "code": "R097",
        "lat": 32.8688,
        "lon": -96.7706,
        "state": "TX",
    },
    "Knox Street, Dallas": {
        "code": "R071",
        "lat": 32.8151,
        "lon": -96.7933,
        "state": "TX",
    },
    "Highland Village": {
        "code": "R058",
        "lat": 32.9979,
        "lon": -97.0453,
        "state": "TX",
    },
    # Florida
    "Aventura": {"code": "R003", "lat": 25.9564, "lon": -80.1426, "state": "FL"},
    "Brickell City Centre": {
        "code": "R447",
        "lat": 25.7663,
        "lon": -80.1918,
        "state": "FL",
    },
    "Town Center, Boca Raton": {
        "code": "R133",
        "lat": 26.3683,
        "lon": -80.1289,
        "state": "FL",
    },
}

# Backward compatibility - simple store name to code mapping
APPLE_STORES = {name: data["code"] for name, data in APPLE_STORES_DATA.items()}

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
    # Keep old iPhone 15 Pro options for existing configs
    "iPhone 15 Pro 128GB Natural Titanium": "MU2F3LL/A",
    "iPhone 15 Pro 256GB Natural Titanium": "MU2G3LL/A",
    "iPhone 15 Pro 512GB Natural Titanium": "MU2H3LL/A",
    "iPhone 15 Pro 1TB Natural Titanium": "MU2J3LL/A",
    "iPhone 15 Pro Max 256GB Natural Titanium": "MU2T3LL/A",
    "iPhone 15 Pro Max 512GB Natural Titanium": "MU2U3LL/A",
    "iPhone 15 Pro Max 1TB Natural Titanium": "MU2V3LL/A",
}
