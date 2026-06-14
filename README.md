# Kostal PIKO (TK) — Home Assistant Integration

A Home Assistant custom integration that reads measurement values from a
**Kostal PIKO** solar inverter by polling its built-in HTML status page.

Ported from the C# project `TK.HA.Kostal`.

## Features

- Polls the inverter every 30 s (configurable, minimum 5 s).
- Exposes every value parsed from the inverter page as a sensor entity:
  - Current AC power, total / daily energy, status
  - String 1 / String 2: voltage, current, power
  - Computed total string power and efficiency
  - L1 / L2 / L3 voltage and power
  - Page download time (diagnostic, disabled by default)
- Optional **night pause** — stops polling between sunset and sunrise to spare
  the inverter when it's offline anyway. Sunrise/sunset are computed locally
  from the configured latitude / longitude (same algorithm as the C# version).
- UI-based setup with a re-auth flow when credentials become invalid.

## Installation

### Via HACS (recommended)

1. In HACS, add this repository as a *custom repository* of type *Integration*.
2. Install **Kostal PIKO (TK)**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration** and search for
   *Kostal PIKO (TK)*.

### Manual

Copy `custom_components/tk_kostal` into your Home Assistant
`config/custom_components/` directory and restart Home Assistant.

## Configuration

You will be asked for:

| Field | Default | Notes |
|-|-|-|
| Host or IP | — | e.g. `192.168.111.4` |
| Username | `pvserver` | Kostal default |
| Password | — | as configured on the inverter |
| Scan interval | `30 s` | minimum `5 s` |
| Pause at night | on | skips polling when the sun is down |
| Latitude / longitude | from HA settings | only used for the night pause |

Scan interval and night-pause settings can be changed later via the
integration's **Configure** dialog.

## Entities

All entities are grouped under one device (`Kostal PIKO`). Energy sensors use
`total_increasing` so they integrate cleanly with the Home Assistant Energy
dashboard.

## Credits

Based on [`TK.HA.Kostal`](https://github.com/) by the same author. HTML
parsing logic and sunrise calculation are direct ports from the original C#
implementation.
