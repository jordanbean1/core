"""Config flow for Skydrop."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow

from . import views
from .const import DOMAIN, OAUTH2_AUTHORIZE

DOCS_URL = "https://www.home-assistant.io/integrations/skydrop"

_LOGGER = logging.getLogger(__name__)


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle Skydrop."""

    VERSION = 1
    DOMAIN = DOMAIN
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._username = vol.UNDEFINED
        self._password = vol.UNDEFINED
        self._api_key = vol.UNDEFINED
        self._api_secret = vol.UNDEFINED
        self._redirect_uri = vol.UNDEFINED

    async def async_step_user(self, user_input=None):
        """Configure user login page."""
        errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input:
            self._api_key = user_input["api_key"]
            self._api_secret = user_input["api_secret"]
            self._redirect_uri = user_input["redirect_uri"]

            return await self.async_step_authenticate()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key"): str,
                    vol.Required("api_secret"): str,
                    vol.Required("redirect_uri"): str,
                }
            ),
            description_placeholders={"docs_url": DOCS_URL},
            errors=errors,
        )

    async def async_step_authenticate(self):
        """Initiate authentication step."""

        self._create_oauth_view()

        return self.async_external_step(
            step_id="user",
            url=f"{OAUTH2_AUTHORIZE}?response_type=code&client_id={self._api_key}&redirect_uri={self._redirect_uri}&config_flow_id={self.flow_id}",
        )

        return self.async_external_step_done(next_step_id="finish")

    def _create_oauth_view(self):
        """Create oauth view."""
        self.hass.http.register_view(views.SkydropAuthCallbackView())

    async def async_step_finish(self, user_input=None):
        """Finalize authentication step."""

        return self.async_create_entry(
            title=self.data["title"],
            data={
                "api_key": self._api_key,
                "api_secret": self._api_secret,
                "redirect_uri": self._redirect_uri,
            },
        )

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)
