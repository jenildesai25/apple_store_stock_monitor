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
            # Add default stores and products if not provided
            if CONF_STORES not in user_input:
                user_input[CONF_STORES] = ["Fifth Avenue", "SoHo"]
            if CONF_PRODUCTS not in user_input:
                user_input[CONF_PRODUCTS] = [
                    "iPhone 15 Pro 128GB Natural Titanium",
                    "iPhone 15 Pro 256GB Natural Titanium",
                ]

            return self.async_create_entry(
                title="Apple Store Notifier", data=user_input
            )

        # Convert dict_keys to lists to avoid JSON serialization issues
        store_options = list(APPLE_STORES.keys())
        product_options = list(IPHONE_MODELS.keys())

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SMS_GATEWAY_URL, default=DEFAULT_SMS_GATEWAY_URL
                ): str,
                vol.Required(
                    CONF_CHECK_INTERVAL, default=DEFAULT_CHECK_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                vol.Required(CONF_STORES, default=store_options[:3]): cv.multi_select(
                    store_options
                ),
                vol.Required(
                    CONF_PRODUCTS, default=product_options[:3]
                ): cv.multi_select(product_options),
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
            # Update the config entry data with new options
            new_data = {**self.config_entry.data, **user_input}
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=new_data
            )
            return self.async_create_entry(title="", data=user_input)

        # Get current values from config entry
        current_stores = self.config_entry.data.get(CONF_STORES, [])
        current_products = self.config_entry.data.get(CONF_PRODUCTS, [])
        current_interval = self.config_entry.data.get(
            CONF_CHECK_INTERVAL, DEFAULT_CHECK_INTERVAL
        )
        current_sms_url = self.config_entry.data.get(
            CONF_SMS_GATEWAY_URL, DEFAULT_SMS_GATEWAY_URL
        )

        # Convert dict_keys to lists
        store_options = list(APPLE_STORES.keys())
        product_options = list(IPHONE_MODELS.keys())

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_CHECK_INTERVAL,
                    default=current_interval,
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                vol.Required(
                    CONF_SMS_GATEWAY_URL,
                    default=current_sms_url,
                ): str,
                vol.Required(
                    CONF_STORES,
                    default=current_stores,
                ): cv.multi_select(store_options),
                vol.Required(
                    CONF_PRODUCTS,
                    default=current_products,
                ): cv.multi_select(product_options),
                vol.Optional(
                    CONF_PHONE_NUMBERS,
                    default=self.config_entry.data.get(CONF_PHONE_NUMBERS, ""),
                ): str,
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)
