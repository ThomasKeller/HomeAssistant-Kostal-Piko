"""Config and options flow for the Kostal PIKO (TK) integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import KostalAuthError, KostalClient, KostalConnectionError
from .const import (
    CONF_SCAN_INTERVAL,
    CONF_STOP_DURING_SUNSET,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_STOP_DURING_SUNSET,
    DEFAULT_USERNAME,
    DOMAIN,
    MIN_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


async def _validate(hass, host: str, username: str, password: str) -> None:
    """Try to reach the inverter; raise on failure."""
    session = async_get_clientsession(hass)
    client = KostalClient(session, host, username, password)
    result = await client.read_page()
    if not result.is_success:
        raise KostalConnectionError(f"HTTP {result.status_code}")


class KostalConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the initial setup and re-authentication."""

    VERSION = 1

    def __init__(self) -> None:
        self._reauth_entry: ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Initial step: ask for host and credentials."""
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()
            try:
                await _validate(
                    self.hass,
                    host,
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                )
            except KostalAuthError:
                errors["base"] = "invalid_auth"
            except KostalConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error validating Kostal inverter")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=f"{DEFAULT_NAME} ({host})",
                    data={
                        CONF_HOST: host,
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                    },
                    options={
                        CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                        CONF_STOP_DURING_SUNSET: user_input[
                            CONF_STOP_DURING_SUNSET
                        ],
                        CONF_LATITUDE: user_input[CONF_LATITUDE],
                        CONF_LONGITUDE: user_input[CONF_LONGITUDE],
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME, default=DEFAULT_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(int, vol.Range(min=MIN_SCAN_INTERVAL)),
                vol.Required(
                    CONF_STOP_DURING_SUNSET,
                    default=DEFAULT_STOP_DURING_SUNSET,
                ): bool,
                vol.Required(
                    CONF_LATITUDE, default=self.hass.config.latitude
                ): vol.Coerce(float),
                vol.Required(
                    CONF_LONGITUDE, default=self.hass.config.longitude
                ): vol.Coerce(float),
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_reauth(
        self, entry_data: dict[str, Any]
    ) -> ConfigFlowResult:
        """Start re-auth when credentials become invalid."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask for new credentials and update the entry."""
        errors: dict[str, str] = {}
        assert self._reauth_entry is not None
        if user_input is not None:
            host = self._reauth_entry.data[CONF_HOST]
            try:
                await _validate(
                    self.hass,
                    host,
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                )
            except KostalAuthError:
                errors["base"] = "invalid_auth"
            except KostalConnectionError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(
                    self._reauth_entry,
                    data={
                        **self._reauth_entry.data,
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                    },
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=self._reauth_entry.data.get(CONF_USERNAME),
                    ): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> KostalOptionsFlow:
        """Return the options flow."""
        return KostalOptionsFlow()


class KostalOptionsFlow(OptionsFlow):
    """Allow changing the scan interval and night-pause settings later."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        options = self.config_entry.options
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=options.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                ): vol.All(int, vol.Range(min=MIN_SCAN_INTERVAL)),
                vol.Required(
                    CONF_STOP_DURING_SUNSET,
                    default=options.get(
                        CONF_STOP_DURING_SUNSET, DEFAULT_STOP_DURING_SUNSET
                    ),
                ): bool,
                vol.Required(
                    CONF_LATITUDE,
                    default=options.get(
                        CONF_LATITUDE, self.hass.config.latitude
                    ),
                ): vol.Coerce(float),
                vol.Required(
                    CONF_LONGITUDE,
                    default=options.get(
                        CONF_LONGITUDE, self.hass.config.longitude
                    ),
                ): vol.Coerce(float),
            }
        )
        return self.async_show_form(step_id="init", data_schema=data_schema)
