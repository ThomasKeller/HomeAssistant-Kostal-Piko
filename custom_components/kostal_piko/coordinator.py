"""Data update coordinator for the Kostal PIKO (TK) integration.

Replaces the polling loop in KostalPeriodicReader.cs / KostalChannelWriter.cs.
Home Assistant's DataUpdateCoordinator handles the periodic scheduling; this
class fetches + parses one sample per tick and honours the night-pause option.
"""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import KostalAuthError, KostalClient, KostalConnectionError
from .const import DOMAIN, STATUS_NIGHT
from .parser import KostalValues, parse
from .sun import has_the_sun_gone_down

_LOGGER = logging.getLogger(__name__)


class KostalCoordinator(DataUpdateCoordinator[KostalValues]):
    """Polls the inverter and exposes the latest KostalValues."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: KostalClient,
        scan_interval: int,
        stop_during_sunset: bool,
        latitude: float,
        longitude: float,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
            config_entry=entry,
        )
        self._client = client
        self._stop_during_sunset = stop_during_sunset
        self._latitude = latitude
        self._longitude = longitude

    async def _async_update_data(self) -> KostalValues:
        """Fetch one sample (mirrors one iteration of ReadFromKostalAsync)."""
        if self._stop_during_sunset and has_the_sun_gone_down(
            self._latitude, self._longitude
        ):
            _LOGGER.debug("Sun is down - skipping inverter request.")
            # Keep the previous reading but mark the inverter as asleep.
            night = KostalValues(status=STATUS_NIGHT)
            if self.data is not None:
                night.produced_energy_kwh = self.data.produced_energy_kwh
                night.daily_energy_kwh = self.data.daily_energy_kwh
            return night

        try:
            result = await self._client.read_page()
        except KostalAuthError as err:
            # Trigger HA's re-auth flow instead of just failing.
            raise ConfigEntryAuthFailed(str(err)) from err
        except KostalConnectionError as err:
            raise UpdateFailed(f"Error communicating with inverter: {err}") from err

        if not result.is_success:
            raise UpdateFailed(
                f"Inverter returned HTTP {result.status_code}"
            )

        values = parse(result.page, result.download_time_ms)
        _LOGGER.debug(
            "Current power: %s W, daily energy: %s kWh, download: %s ms",
            values.current_ac_power_w,
            values.daily_energy_kwh,
            values.download_time_ms,
        )
        return values
