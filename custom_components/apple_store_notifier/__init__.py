"""Apple Store Stock Notifier integration for Home Assistant."""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Apple Store Notifier from a config entry."""

    coordinator = AppleStoreCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class AppleStoreCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Apple Store stock data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize."""
        self.entry = entry

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=entry.data.get("check_interval", 10)),
        )

    async def _async_update_data(self):
        """Fetch data from Apple Store."""
        _LOGGER.info("Starting Apple Store stock check...")

        from .apple_monitor import AppleStoreMonitor

        monitor = AppleStoreMonitor(
            stores=self.entry.data.get("stores", []),
            products=self.entry.data.get("products", []),
            sms_gateway_url=self.entry.data.get("sms_gateway_url"),
        )

        result = await self.hass.async_add_executor_job(monitor.check_stock)
        _LOGGER.info(
            f"Stock check completed. Found {result.get('total_available', 0)} items available"
        )

        return result
