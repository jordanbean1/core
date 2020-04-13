"""Config flow for Skydrop."""
import json
import logging

import requests
from skydroppy import SkydropClient
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN

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

    async def async_step_user(self, user_input=None):
        """Configure user login page."""
        errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            self._username = user_input["username"]
            self._password = user_input["password"]

            error = await self.hass.async_add_executor_job(
                self.try_login, self._username, self._password
            )

            if error:
                errors["base"] = error
            else:
                return await self.async_step_create_entry(user_input=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
            ),
            description_placeholders={"docs_url": DOCS_URL},
            errors=errors,
        )

    async def async_step_create_entry(self, user_input=None):
        """Create Entry."""

        return self.async_create_entry(
            title=user_input[CONF_USERNAME],
            data=user_input,
            description_placeholders={"docs_url": DOCS_URL},
        )

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    @staticmethod
    def try_login(username, password):
        """Try logging in to device and return any errors."""

        params = {"email": username, "password": password}

        try:
            response = requests.get(
                url="https://api.skydrop.com/index/auth", params=params
            )
        except requests.HTTPError:
            _LOGGER.error(
                "Unable to login to Skydrop API: Error Code: %s, Error Reason: %s",
                response.status_code,
                response.reason,
            )
            return f"{response.status_code}: {response.reason}"

        # Skydrop sends a 200, even if error occurs, have to parse the response
        if response.status_code == 200:
            response_content = json.loads(response.text)

            if response_content["error"]:
                _LOGGER.error(
                    "Unable to login to Skydrop API: Error Message: %s",
                    response_content["messages"],
                )
                return f"Error: {response_content['messages']}"

        return None

    @staticmethod
    def try_create_application(client_id, client_secret):
        """Try logging in to device and return any errors."""

        try:
            SkydropClient(client_id, client_secret)
        except SkydropClient.BadRequest:
            return "BadRequest"
        except SkydropClient.Unauthorized:
            return "Unauthorized"
        except SkydropClient.Forbidden:
            return "Forbidden"
        except SkydropClient.TooManyRequests:
            return "TooManyRequests"
        except SkydropClient.InternalServerError:
            return "InternalServerError"
        except SkydropClient.ClientError:
            return "ClientError"

        return None

    @staticmethod
    def try_authenticate(client_id, client_secret):
        """Try logging in to device and return any errors."""

        try:
            SkydropClient(client_id, client_secret)
        except SkydropClient.BadRequest:
            return "BadRequest"
        except SkydropClient.Unauthorized:
            return "Unauthorized"
        except SkydropClient.Forbidden:
            return "Forbidden"
        except SkydropClient.TooManyRequests:
            return "TooManyRequests"
        except SkydropClient.InternalServerError:
            return "InternalServerError"
        except SkydropClient.ClientError:
            return "ClientError"

        return None
