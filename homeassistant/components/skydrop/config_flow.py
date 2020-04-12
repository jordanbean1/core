"""Config flow for Skydrop."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle Skydrop OAuth2 authentication."""

    DOMAIN = DOMAIN
    # TODO Pick one from config_entries.CONN_CLASS_*
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None):
        """Configure user login page."""

        # Specify items in the order they are to be displayed in the UI
        data_schema = {
            vol.Required("username"): str,
            vol.Required("password"): str,
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(data_schema))

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)
