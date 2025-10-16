"""Zipcode utilities for finding nearby Apple Stores."""

import math
import requests
import logging
from typing import Dict, List, Tuple, Optional

_LOGGER = logging.getLogger(__name__)


def get_zipcode_coordinates(zipcode: str) -> Optional[Tuple[float, float]]:
    """Get latitude and longitude for a zipcode using a free API."""
    try:
        # Using zippopotam.us - free zipcode API
        url = f"http://api.zippopotam.us/us/{zipcode}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            lat = float(data["places"][0]["latitude"])
            lon = float(data["places"][0]["longitude"])
            return (lat, lon)
        else:
            _LOGGER.warning(f"Could not find coordinates for zipcode {zipcode}")
            return None

    except Exception as e:
        _LOGGER.error(f"Error getting coordinates for zipcode {zipcode}: {e}")
        return None


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula."""
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in miles
    r = 3956

    return c * r


def find_nearby_stores(
    zipcode: str, stores_data: Dict, max_distance: float = 50.0
) -> List[Dict]:
    """Find Apple Stores within max_distance miles of zipcode."""
    coordinates = get_zipcode_coordinates(zipcode)
    if not coordinates:
        return []

    user_lat, user_lon = coordinates
    nearby_stores = []

    for store_name, store_info in stores_data.items():
        store_lat = store_info["lat"]
        store_lon = store_info["lon"]

        distance = calculate_distance(user_lat, user_lon, store_lat, store_lon)

        if distance <= max_distance:
            nearby_stores.append(
                {
                    "name": store_name,
                    "code": store_info["code"],
                    "state": store_info["state"],
                    "distance": round(distance, 1),
                    "lat": store_lat,
                    "lon": store_lon,
                }
            )

    # Sort by distance
    nearby_stores.sort(key=lambda x: x["distance"])

    return nearby_stores
