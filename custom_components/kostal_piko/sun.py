"""Sunrise/sunset calculation for the night-pause feature.

Ported from Sun.cs in the C# project TK.HA.Kostal. Kept self-contained so the
integration has no extra dependencies. Returns local-time sunrise/sunset for
the given location, with the same +/-60 min PV margin as the original
``CalculatePvTime``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class SunValues:
    """Sunrise/sunset timestamps in local time."""

    sunrise: datetime
    sunset: datetime


def _calculate(latitude: float, longitude: float, year: int, month: int, day: int) -> SunValues:
    """Faithful port of Sun.Calculate(lat, lon, year, month, day)."""
    pi = math.pi
    dr = pi / 180
    rd = 1 / dr
    b5 = latitude
    l5 = longitude
    h = 0  # timezone UTC
    now = datetime.now()
    m = month
    d = day
    b5 = dr * b5
    n = 275 * m // 9 - 2 * ((m + 9) // 12) + d - 30
    l0 = 4.8771 + 0.0172 * (n + 0.5 - l5 / 360)
    c = 0.03342 * math.sin(l0 + 1.345)
    c2 = rd * (
        math.atan(math.tan(l0 + c))
        - math.atan(0.9175 * math.tan(l0 + c))
        - c
    )
    sd = 0.3978 * math.sin(l0 + c)
    cd = math.sqrt(1 - sd * sd)
    sc = (sd * math.sin(b5) + 0.0145) / (math.cos(b5) * cd)

    sunrise = datetime.min.replace(tzinfo=timezone.utc)
    sunset = datetime.min.replace(tzinfo=timezone.utc)

    if abs(sc) <= 1:
        # sunrise
        c3 = rd * math.atan(sc / math.sqrt(1 - sc * sc))
        r1 = 6 - h - (l5 + c2 + c3) / 15
        hr = int(r1)
        mr = int((r1 - hr) * 60)
        sunrise = datetime(year, month, day, hr, mr, 0, tzinfo=timezone.utc)
        # sunset
        s1 = 18 - h - (l5 + c2 - c3) / 15
        hs = int(s1)
        ms = int((s1 - hs) * 60)
        sunset = datetime(year, month, day, hs, ms, 0, tzinfo=timezone.utc)
    elif sc > 1:
        # sun is up all day
        sunset = datetime(now.year + 1, now.month, now.day, now.hour, now.minute, now.second, tzinfo=timezone.utc)
        sunrise = datetime(now.year - 1, now.month, now.day, now.hour, max(now.minute - 1, 0), now.second, tzinfo=timezone.utc)
    else:  # sc < -1
        # sun is down all day -> both in the future
        sunrise = datetime(now.year + 1, now.month, now.day, now.hour, now.minute, now.second, tzinfo=timezone.utc)
        sunset = datetime(now.year + 1, now.month, now.day, now.hour, now.minute, now.second, tzinfo=timezone.utc)

    return SunValues(sunrise=sunrise.astimezone(), sunset=sunset.astimezone())


def calculate_pv_time(latitude: float, longitude: float) -> SunValues:
    """Like Sun.CalculatePvTime: sunrise -60 min, sunset +60 min."""
    today = datetime.now()
    values = _calculate(latitude, longitude, today.year, today.month, today.day)
    values.sunrise = values.sunrise - timedelta(minutes=60)
    values.sunset = values.sunset + timedelta(minutes=60)
    return values


def has_the_sun_gone_down(latitude: float, longitude: float) -> bool:
    """Mirror of HasTheSunGoneDown(): compares the current hour to the PV window."""
    now = datetime.now()
    values = calculate_pv_time(latitude, longitude)
    return now.hour > values.sunset.hour or now.hour < values.sunrise.hour
