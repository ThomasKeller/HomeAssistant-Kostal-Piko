"""Constants for the Kostal PIKO (TK) integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "kostal_piko"

# Configuration keys
CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_STOP_DURING_SUNSET = "stop_during_sunset"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"

# Defaults (mirrors KostalReadParameter.cs)
DEFAULT_NAME = "Kostal PIKO"
DEFAULT_USERNAME = "pvserver"
DEFAULT_SCAN_INTERVAL = 30  # seconds
DEFAULT_STOP_DURING_SUNSET = True

MIN_SCAN_INTERVAL = 5  # seconds

# The inverter HTML status page is served at the web root.
PAGE_PATH = "/"

# Manufacturer / model info shown on the HA device page.
MANUFACTURER = "Kostal"
MODEL = "PIKO"

# Status value used while polling is paused at night.
STATUS_NIGHT = "Nacht"

REQUEST_TIMEOUT = timedelta(seconds=15)
