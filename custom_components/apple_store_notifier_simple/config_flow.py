"""Config flow for Apple Store Notifier Simple."""

import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "apple_store_notifier_simple"


class AppleStoreNotifierSimpleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Apple Store Notifier Simple."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title="Apple Store Notifier Simple", data={"test": "success"}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("test_field", default="test"): str,
                }
            ),
        )
