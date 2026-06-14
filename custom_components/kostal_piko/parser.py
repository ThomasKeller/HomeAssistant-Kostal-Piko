"""Parser for the Kostal PIKO inverter HTML status page.

Ported from the C# project TK.HA.Kostal (KostalParser.cs / KostalValues.cs).
The inverter serves a fixed-layout HTML table; values are read by the
positional index of their ``<td>`` cell, exactly like the original.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

# Mirrors m_ColumnPattern in KostalParser.cs:
#   <td\b[^>]*?>(?<V>[\s\S]*?)</\s*td>   (IgnoreCase)
_COLUMN_PATTERN = re.compile(r"<td\b[^>]*?>(?P<V>[\s\S]*?)</\s*td>", re.IGNORECASE)


@dataclass
class KostalValues:
    """Parsed values from the inverter page (mirrors KostalValues.cs)."""

    measure_time: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    download_time_ms: int = 0
    current_ac_power_w: int = 0
    produced_energy_kwh: int | None = None
    daily_energy_kwh: float = 0.0
    status: str = "Fehler"
    string1_voltage_v: int = 0
    string1_current_a: float = 0.0
    string1_power_w: float = 0.0
    string2_voltage_v: int = 0
    string2_current_a: float = 0.0
    string2_power_w: float = 0.0
    string_power_w: float = 0.0
    efficiency: float = 0.0
    l1_voltage_v: int = 0
    l1_power_w: int = 0
    l2_voltage_v: int = 0
    l2_power_w: int = 0
    l3_voltage_v: int = 0
    l3_power_w: int = 0


def _to_int(value: str) -> int | None:
    """Parse an integer the way C# int.TryParse(NumberStyles.Number) would."""
    text = value.strip().replace(",", "")
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        try:
            # Tolerate values like "1234.0".
            return int(float(text))
        except ValueError:
            return None


def _to_int_default(value: str, default: int) -> int:
    result = _to_int(value)
    return result if result is not None else default


def _to_float(value: str) -> float | None:
    """Parse a float using invariant ('.' decimal) culture."""
    text = value.strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _to_float_default(value: str, default: float) -> float:
    result = _to_float(value)
    return result if result is not None else default


def parse(html_page: str | None, download_time_ms: int = 0) -> KostalValues:
    """Parse the inverter HTML page into KostalValues.

    Faithful port of KostalParser.Parse. Cell indices are 1-based and match
    the fixed layout of the Kostal PIKO web server page.
    """
    result = KostalValues(download_time_ms=download_time_ms)
    if not html_page:
        return result

    line = 1
    for match in _COLUMN_PATTERN.finditer(html_page):
        value = match.group("V")
        if line == 15:
            result.current_ac_power_w = _to_int_default(value, 0)
        elif line == 18:
            result.produced_energy_kwh = _to_int(value)
        elif line == 27:
            result.daily_energy_kwh = _to_float_default(value, 0.0)
        elif line == 33:
            result.status = value.replace("(MPP)", "").strip()
        elif line == 56:
            result.string1_voltage_v = _to_int_default(value, 0)
        elif line == 59:
            result.l1_voltage_v = _to_int_default(value, 0)
        elif line == 65:
            result.string1_current_a = _to_float_default(value, 0.0)
        elif line == 68:
            result.l1_power_w = _to_int_default(value, 0)
        elif line == 82:
            result.string2_voltage_v = _to_int_default(value, 0)
        elif line == 85:
            result.l2_voltage_v = _to_int_default(value, 0)
        elif line == 91:
            result.string2_current_a = _to_float_default(value, 0.0)
        elif line == 94:
            result.l2_power_w = _to_int_default(value, 0)
        elif line == 111:
            result.l3_voltage_v = _to_int_default(value, 0)
        elif line == 120:
            result.l3_power_w = _to_int_default(value, 0)
        line += 1

    result.string1_power_w = round(
        result.string1_current_a * result.string1_voltage_v, 0
    )
    result.string2_power_w = round(
        result.string2_current_a * result.string2_voltage_v, 0
    )
    result.string_power_w = round(
        result.string1_power_w + result.string2_power_w, 0
    )
    result.efficiency = (
        round(result.current_ac_power_w / result.string_power_w * 100, 2)
        if result.string_power_w > 0
        else 0.0
    )
    return result
