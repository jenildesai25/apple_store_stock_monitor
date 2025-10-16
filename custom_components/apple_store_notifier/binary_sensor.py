"""Binary sensor platform for Apple Store Notifier."""

from homeassistant.components.binary_sensor import BinarySensorEntity
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
    """Set up Apple Store Notifier binary sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = [
        AppleStoreAvailabilityBinarySensor(coordinator, config_entry),
    ]

    async_add_entities(entities)


class AppleStoreAvailabilityBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for Apple Store stock availability."""

    def __init__(self, coordinator, config_entry):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_name = "Apple Store Stock Available"
        self._attr_unique_id = f"{config_entry.entry_id}_stock_binary"
        self._attr_icon = "mdi:apple"
        self._attr_device_class = "connectivity"

    @property
    def is_on(self):
        """Return true if stock is available."""
        if self.coordinator.data:
            return self.coordinator.data.get("total_available", 0) > 0
        return False

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        available_items = self.coordinator.data.get("available_items", [])

        return {
            "available_count": len(available_items),
            "available_products": [item["product"] for item in available_items],
            "available_stores": [item["store"] for item in available_items],
            "last_check": self.coordinator.data.get("timestamp"),
        }
