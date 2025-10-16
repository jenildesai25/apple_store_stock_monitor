"""Config flow for Apple Store Notifier integration."""

import logging
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
    CONF_ZIPCODE,
    CONF_PRIMARY_STORE,
    DEFAULT_CHECK_INTERVAL,
    DEFAULT_SMS_GATEWAY_URL,
    APPLE_STORES,
    APPLE_STORES_DATA,
    IPHONE_MODELS,
)
from .zipcode_utils import find_nearby_stores

_LOGGER = logging.getLogger(__name__)


class AppleStoreNotifierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Apple Store Notifier."""

    VERSION = 1

    def __init__(self):
        """Initialize config flow."""
        self.zipcode = None
        self.nearby_stores_map = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step - zipcode entry."""
        errors = {}

        if user_input is not None:
            # Store zipcode and move to store selection
            self.zipcode = user_input[CONF_ZIPCODE]
            return await self.async_step_stores()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ZIPCODE, default="97223"): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_stores(self, user_input=None):
        """Handle store and product selection based on zipcode."""
        errors = {}

        if user_input is not None:
            # Process the store selections and clean up display names
            processed_data = {
                CONF_ZIPCODE: self.zipcode,
                CONF_SMS_GATEWAY_URL: user_input[CONF_SMS_GATEWAY_URL],
                CONF_CHECK_INTERVAL: user_input[CONF_CHECK_INTERVAL],
                CONF_PRODUCTS: user_input[CONF_PRODUCTS],
                CONF_PHONE_NUMBERS: user_input.get(CONF_PHONE_NUMBERS, ""),
            }

            # Clean up store names (remove distance info)
            if self.nearby_stores_map:
                # Map display names back to clean store names
                primary_store_display = user_input[CONF_PRIMARY_STORE]
                primary_store_clean = self.nearby_stores_map.get(
                    primary_store_display, primary_store_display
                )

                stores_display = user_input[CONF_STORES]
                stores_clean = [
                    self.nearby_stores_map.get(store, store) for store in stores_display
                ]

                processed_data[CONF_PRIMARY_STORE] = primary_store_clean
                processed_data[CONF_STORES] = stores_clean
            else:
                processed_data[CONF_PRIMARY_STORE] = user_input[CONF_PRIMARY_STORE]
                processed_data[CONF_STORES] = user_input[CONF_STORES]

            return self.async_create_entry(
                title=f"Apple Store Monitor ({self.zipcode})", data=processed_data
            )

        # Find nearby stores
        try:
            nearby_stores = await self.hass.async_add_executor_job(
                find_nearby_stores, self.zipcode, APPLE_STORES_DATA, 50.0
            )
        except Exception as e:
            _LOGGER.error(f"Error finding stores for zipcode {self.zipcode}: {e}")
            nearby_stores = []

        if not nearby_stores:
            errors["base"] = "no_stores_found"
            # Fallback to all stores
            store_options = list(APPLE_STORES.keys())[:10]
            self.nearby_stores_map = {}
        else:
            # Create store options with distance info
            store_options = []
            self.nearby_stores_map = {}

            for store in nearby_stores[:10]:  # Limit to 10 closest
                display_name = f"{store['name']} ({store['distance']} mi)"
                store_options.append(display_name)
                self.nearby_stores_map[display_name] = store["name"]

        product_options = list(IPHONE_MODELS.keys())

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SMS_GATEWAY_URL, default=DEFAULT_SMS_GATEWAY_URL
                ): str,
                vol.Required(
                    CONF_CHECK_INTERVAL, default=DEFAULT_CHECK_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                vol.Required(
                    CONF_PRIMARY_STORE,
                    default=store_options[0] if store_options else "",
                ): vol.In(store_options),
                vol.Required(CONF_STORES, default=store_options[:3]): cv.multi_select(
                    store_options
                ),
                vol.Required(
                    CONF_PRODUCTS,
                    default=product_options[:1],  # Default to first iPhone
                ): cv.multi_select(product_options),
                vol.Optional(CONF_PHONE_NUMBERS, default=""): str,
            }
        )

        return self.async_show_form(
            step_id="stores", data_schema=data_schema, errors=errors
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
