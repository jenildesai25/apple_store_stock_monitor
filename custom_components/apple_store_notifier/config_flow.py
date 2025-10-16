"""Config flow for Apple Store Notifier integration."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_STORES,
    CONF_PRODUCTS,
    CONF_SMS_GATEWAY_URL,
    CONF_CHECK_INTERVAL,
    CONF_PHONE_NUMBERS,
    DEFAULT_CHECK_INTERVAL,
    DEFAULT_SMS_GATEWAY_URL,
    APPLE_STORES,
    IPHONE_MODELS,
)


class AppleStoreNotifierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Apple Store Notifier."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Apple Store Notifier", data=user_input
            )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SMS_GATEWAY_URL, default=DEFAULT_SMS_GATEWAY_URL
                ): str,
                vol.Required(
                    CONF_CHECK_INTERVAL, default=DEFAULT_CHECK_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                vol.Required(
                    CONF_STORES, default=list(APPLE_STORES.keys())[:3]
                ): vol.All(cv.multi_select, vol.In(APPLE_STORES.keys())),
                vol.Required(
                    CONF_PRODUCTS, default=list(IPHONE_MODELS.keys())[:3]
                ): vol.All(cv.multi_select, vol.In(IPHONE_MODELS.keys())),
                vol.Optional(CONF_PHONE_NUMBERS, default=""): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return AppleStoreNotifierOptionsFlow(config_entry)


class AppleStoreNotifierOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Apple Store Notifier."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_CHECK_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_CHECK_INTERVAL, DEFAULT_CHECK_INTERVAL
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                vol.Required(
                    CONF_SMS_GATEWAY_URL,
                    default=self.config_entry.options.get(
                        CONF_SMS_GATEWAY_URL, DEFAULT_SMS_GATEWAY_URL
                    ),
                ): str,
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)
