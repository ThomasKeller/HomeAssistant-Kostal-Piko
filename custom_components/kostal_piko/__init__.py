"""The Kostal PIKO (TK) integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_PASSWORD,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import KostalClient
from .const import (
    CONF_SCAN_INTERVAL,
    CONF_STOP_DURING_SUNSET,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_STOP_DURING_SUNSET,
)
from .coordinator import KostalCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

type KostalConfigEntry = ConfigEntry[KostalCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: KostalConfigEntry) -> bool:
    """Set up Kostal PIKO from a config entry."""
    session = async_get_clientsession(hass)
    client = KostalClient(
        session,
        entry.data[CONF_HOST],
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
    )

    coordinator = KostalCoordinator(
        hass,
        entry,
        client,
        scan_interval=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        stop_during_sunset=entry.options.get(
            CONF_STOP_DURING_SUNSET, DEFAULT_STOP_DURING_SUNSET
        ),
        latitude=entry.options.get(CONF_LATITUDE, hass.config.latitude),
        longitude=entry.options.get(CONF_LONGITUDE, hass.config.longitude),
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: KostalConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(
    hass: HomeAssistant, entry: KostalConfigEntry
) -> None:
    """Reload the entry when options change (e.g. new scan interval)."""
    await hass.config_entries.async_reload(entry.entry_id)
