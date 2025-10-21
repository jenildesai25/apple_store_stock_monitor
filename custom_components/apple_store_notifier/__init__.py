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

    # Service registration removed to fix services.yaml error

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

        # Create the monitor instance once and reuse it
        stores = entry.data.get("stores", [])
        products = entry.data.get("products", [])
        sms_gateway_url = entry.data.get("sms_gateway_url")

        from .apple_monitor import AppleStoreMonitor

        self._monitor = AppleStoreMonitor(stores, products, sms_gateway_url)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=entry.data.get("check_interval", 10)),
        )

    async def _async_update_data(self):
        """Fetch data from Apple Store with individual product tracking."""
        stores = self.entry.data.get("stores", [])
        products = self.entry.data.get("products", [])

        _LOGGER.info(
            f"🍎 Starting stock check: {len(stores)} stores, {len(products)} products"
        )

        result = await self.hass.async_add_executor_job(self._monitor.check_stock)

        available_count = result.get("total_available", 0)
        individual_results = result.get("individual_results", {})

        if available_count > 0:
            _LOGGER.warning(f"🎉 STOCK FOUND! {available_count} items available!")
            for item in result.get("available_items", []):
                _LOGGER.warning(f"📱 {item['product']} at {item['store']}")
        else:
            _LOGGER.info(f"✅ Check complete: No stock found")

        # Log individual product status for debugging
        _LOGGER.debug(
            f"📊 Individual results: {len(individual_results)} product/store combinations checked"
        )
        for key, individual_result in individual_results.items():
            status = (
                "✅ Available" if individual_result["available"] else "❌ Out of stock"
            )
            _LOGGER.debug(
                f"   {individual_result['product_name']} at {individual_result['store_name']}: {status}"
            )

        return result
