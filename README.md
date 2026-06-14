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

Copy `custom_components/kostal_piko` into your Home Assistant
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

## Companion Dashboards

Two ready-made Lovelace dashboards ship with the integration. Pick whichever
matches the look you want.

### Option B — Standard ([`dashboards/kostal.yaml`](dashboards/kostal.yaml))

Built from stock Lovelace cards plus a single HACS plugin. Shows live AC
power and efficiency as gauges, the daily power curve, both PV strings and
the three AC phases as charts, and a 30-day energy history.

Prerequisite:
- [`apexcharts-card`](https://github.com/RomRider/apexcharts-card)

### Option C — Mushroom ([`dashboards/kostal-mushroom.yaml`](dashboards/kostal-mushroom.yaml))

Modern look using Mushroom cards, with a 3-column DC → Inverter → AC flow
visualisation and an optional commented-out section for
`power-flow-card-plus` if you also have grid/consumption sensors.

Prerequisites:
- [`apexcharts-card`](https://github.com/RomRider/apexcharts-card)
- [`mushroom`](https://github.com/piitaya/lovelace-mushroom)
- [`power-flow-card-plus`](https://github.com/flixlix/power-flow-card-plus)
  (optional, only for the bottom flow section)

### Installation (both)

Paste the YAML into a new dashboard
(*Settings → Dashboards → Add Dashboard → from YAML*) or merge the views
into an existing one via raw configuration editor. If you renamed the
inverter device, search/replace `sensor.kostal_piko_` with your prefix and
adjust the AC-power gauge maximum to match your inverter's peak power.

## Credits

Based on [`TK.HA.Kostal`](https://github.com/) by the same author. HTML
parsing logic and sunrise calculation are direct ports from the original C#
implementation.
