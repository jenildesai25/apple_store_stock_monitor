"""Apple Store Notifier sensors for Home Assistant."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .apple_monitor import AppleStoreMonitor

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Apple Store Notifier sensors."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    # Create individual sensors for each product/store combination
    entities = []

    # Main summary sensor
    entities.append(AppleStoreNotifierSensor(coordinator, config_entry))

    # Individual product sensors
    if coordinator.data and "individual_results" in coordinator.data:
        for product_store_key, result in coordinator.data["individual_results"].items():
            entities.append(
                AppleProductSensor(coordinator, config_entry, product_store_key, result)
            )

    async_add_entities(entities, True)


class AppleStoreNotifierSensor(CoordinatorEntity, SensorEntity):
    """Main Apple Store Notifier sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator, config_entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "Apple Store Stock Monitor"
        self._attr_unique_id = f"{DOMAIN}_main"
        self._attr_icon = "mdi:apple"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return "unknown"

        total_available = self.coordinator.data.get("total_available", 0)
        return str(total_available)

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        data = self.coordinator.data

        attributes = {
            "total_available": data.get("total_available", 0),
            "products_checked": data.get("products_checked", 0),
            "stores_checked": data.get("stores_checked", 0),
            "last_update": data.get("timestamp"),
            "available_items": data.get("available_items", []),
        }

        # Add individual product status summary
        if "individual_results" in data:
            product_summary = {}
            for key, result in data["individual_results"].items():
                product_code = result["product_code"]
                if product_code not in product_summary:
                    product_summary[product_code] = {
                        "name": result["product_name"],
                        "available_stores": 0,
                        "total_stores": 0,
                        "last_checked": result["last_checked"],
                    }

                product_summary[product_code]["total_stores"] += 1
                if result["available"]:
                    product_summary[product_code]["available_stores"] += 1

            attributes["product_summary"] = product_summary

        return attributes

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "items"


class AppleProductSensor(CoordinatorEntity, SensorEntity):
    """Individual Apple product sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        config_entry: ConfigEntry,
        product_store_key: str,
        initial_result: Dict[str, Any],
    ):
        """Initialize the product sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._product_store_key = product_store_key
        self._product_code = initial_result["product_code"]
        self._store_code = initial_result["store_code"]

        # Create friendly names
        product_name = initial_result["product_name"]
        store_name = initial_result["store_name"]

        self._attr_name = f"{product_name} at {store_name}"
        self._attr_unique_id = f"{DOMAIN}_{self._product_store_key}"
        self._attr_icon = (
            "mdi:cellphone" if "iphone" in product_name.lower() else "mdi:apple"
        )

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if (
            not self.coordinator.data
            or "individual_results" not in self.coordinator.data
        ):
            return "unknown"

        result = self.coordinator.data["individual_results"].get(
            self._product_store_key
        )
        if not result:
            return "unknown"

        if result["status"] == "error":
            return "error"
        elif result["available"]:
            return "available"
        else:
            return "unavailable"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes."""
        if (
            not self.coordinator.data
            or "individual_results" not in self.coordinator.data
        ):
            return {}

        result = self.coordinator.data["individual_results"].get(
            self._product_store_key
        )
        if not result:
            return {}

        attributes = {
            "product_name": result["product_name"],
            "product_code": result["product_code"],
            "store_name": result["store_name"],
            "store_code": result["store_code"],
            "available": result["available"],
            "pickup_available": result.get("pickup_available", False),
            "last_checked": result["last_checked"],
            "status": result["status"],
        }

        # Add error information if present
        if "error" in result:
            attributes["error"] = result["error"]

        # Add store information if available
        if "store_info" in result and result["store_info"]:
            attributes["store_info"] = result["store_info"]

        # Add restock prediction if enhanced monitoring is available
        if hasattr(self.coordinator, "_monitor") and hasattr(
            self.coordinator._monitor, "enhanced_monitor"
        ):
            try:
                if self.coordinator._monitor.enhanced_monitor:
                    prediction = self.coordinator._monitor.enhanced_monitor.analyzer.predict_next_restock(
                        self._store_code, self._product_code
                    )
                    if prediction and "prediction" not in prediction:
                        attributes["restock_prediction"] = prediction
            except Exception as e:
                _LOGGER.debug(f"Could not get restock prediction: {e}")

        return attributes

    @property
    def device_class(self) -> str:
        """Return the device class."""
        return "enum"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.data is not None
            and "individual_results" in self.coordinator.data
            and self._product_store_key in self.coordinator.data["individual_results"]
        )


class AppleStoreDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Apple Store data."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        monitor: AppleStoreMonitor,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        self._monitor = monitor
        super().__init__(
            hass,
            logger,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data via library."""
        try:
            # Run the stock check in executor to avoid blocking
            data = await self.hass.async_add_executor_job(self._monitor.check_stock)
            return data
        except Exception as exception:
            raise UpdateFailed(f"Error communicating with Apple Store API: {exception}")
