"""Defines Skydrop views."""

from homeassistant import core
from homeassistant.components import http

AUTH_CALLBACK_NAME = "api:skydrop"
AUTH_CALLBACK_PATH = "/skydrop/oauth/setup"


class SkydropAuthCallbackView(http.HomeAssistantView):
    """Skydrop Authorization Callback View."""

    requires_auth = False
    url = AUTH_CALLBACK_PATH
    name = AUTH_CALLBACK_NAME

    def __init__(self):
        """Initialize the view."""

    @core.callback
    def get(self, request):
        """Handle the Skydrop OAuth callbacks."""

        code = request.query.get("code")

        return self.json_message(f"Skydrop OAuth code {code}")
