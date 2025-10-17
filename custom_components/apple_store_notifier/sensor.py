"""Sensor platform for Apple Store Notifier."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Apple Store Notifier sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = [
        AppleStoreStockSensor(coordinator, config_entry),
        AppleStoreLastCheckSensor(coordinator, config_entry),
    ]

    async_add_entities(entities)


class AppleStoreStockSensor(CoordinatorEntity, SensorEntity):
    """Sensor for Apple Store stock availability."""

    def __init__(self, coordinator, config_entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_name = "Apple Store Stock Available"
        self._attr_unique_id = f"{config_entry.entry_id}_stock_available"
        self._attr_icon = "mdi:apple"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("total_available", 0)
        return 0

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        # Get configured stores and products from config entry
        configured_stores = self.config_entry.data.get("stores", [])
        configured_products = self.config_entry.data.get("products", [])

        # Create friendly display strings
        store_list = ", ".join(configured_stores[:2]) + (
            f" (+{len(configured_stores)-2} more)" if len(configured_stores) > 2 else ""
        )
        product_list = ", ".join(
            [
                p.replace("iPhone 17 Pro ", "").replace("iPhone 15 Pro ", "")
                for p in configured_products[:2]
            ]
        ) + (
            f" (+{len(configured_products)-2} more)"
            if len(configured_products) > 2
            else ""
        )

        return {
            "last_check": self.coordinator.data.get("timestamp"),
            "stores_checked": self.coordinator.data.get("stores_checked", 0),
            "products_checked": self.coordinator.data.get("products_checked", 0),
            "available_items": self.coordinator.data.get("available_items", []),
            "monitoring_stores": configured_stores,
            "monitoring_products": configured_products,
            "check_interval_minutes": self.config_entry.data.get("check_interval", 10),
            "stores_display": store_list,
            "products_display": product_list,
            "status_summary": f"Checking {product_list} at {store_list}",
        }

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "items"


class AppleStoreLastCheckSensor(CoordinatorEntity, SensorEntity):
    """Sensor for last check timestamp."""

    def __init__(self, coordinator, config_entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_name = "Apple Store Last Check"
        self._attr_unique_id = f"{config_entry.entry_id}_last_check"
        self._attr_icon = "mdi:clock-outline"
        self._attr_device_class = "timestamp"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("timestamp")
        return None
