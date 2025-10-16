"""Simple Apple Store Stock Notifier integration for testing."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "apple_store_notifier_simple"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Apple Store Notifier from a config entry."""
    _LOGGER.info("Apple Store Notifier Simple: Setup started")

    # Just store the config, don't do anything complex
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    _LOGGER.info("Apple Store Notifier Simple: Setup completed successfully")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
