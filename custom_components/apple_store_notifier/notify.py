"""Notification platform for Apple Store Stock Notifier."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
from homeassistant.components.notify import BaseNotificationService
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, CONF_SMS_GATEWAY_URL

_LOGGER = logging.getLogger(__name__)


async def async_get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> AppleStoreSMSNotificationService | None:
    """Get the notification service."""
    if discovery_info is None:
        return None

    config_entry_id = discovery_info["config_entry_id"]
    config_entry = hass.config_entries.async_get_entry(config_entry_id)

    if config_entry is None:
        return None

    return AppleStoreSMSNotificationService(hass, config_entry)


class AppleStoreSMSNotificationService(BaseNotificationService):
    """SMS notification service for Apple Store stock alerts."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the service."""
        self.hass = hass
        self.config_entry = config_entry
        self._sms_gateway_url = config_entry.data.get(CONF_SMS_GATEWAY_URL)

    async def async_send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send a message via SMS."""
        targets = kwargs.get("target")
        if not targets:
            _LOGGER.error("No target phone numbers specified")
            return

        if isinstance(targets, str):
            targets = [targets]

        for phone_number in targets:
            await self._send_sms(phone_number, message)

    async def _send_sms(self, phone_number: str, message: str) -> None:
        """Send SMS to a specific phone number."""
        try:
            async with aiohttp.ClientSession() as session:
                data = {
                    "phone_number": phone_number,
                    "message": message,
                }

                async with session.post(
                    f"{self._sms_gateway_url}/send_sms",
                    json=data,
                    timeout=10,
                ) as response:
                    if response.status == 200:
                        _LOGGER.info("SMS sent successfully to %s", phone_number)
                    else:
                        _LOGGER.error(
                            "Failed to send SMS to %s: %s",
                            phone_number,
                            response.status,
                        )
        except Exception as err:
            _LOGGER.error("Error sending SMS to %s: %s", phone_number, err)
