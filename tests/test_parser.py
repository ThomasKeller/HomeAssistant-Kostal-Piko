"""Smoke test: feed the C# fixture HTML through the Python parser.

The expected values come from KostalTests.cs:
    CurrentACPower_W == 2389
    DailyEnergy_kWh  == 13.49
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "custom_components" / "kostal_piko"))

from parser import parse  # noqa: E402  (sys.path tweak)


PAGE = """<!DOCTYPE html PUBLIC "-//W3C//Dtd HTML 4.0 Transitional//EN">
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<meta name="Generator" content="ChrisB">
<title>PV Webserver</title>
<link href="..." rel="stylesheet" type="text/css"></head>
<body>
<form method="post" action="">
<table cellspacing="0" cellpadding="0" width="770" nof="ly">
<tbody><tr><td height="5"></td></tr>
<tr><td width="190" height="55"></td>
<td width="400">
  <font>PIKO 8.3<br><font>Keller_PV  (255)</font></font>
</td>
<td><img alt="Logo"></td>
</tr>
</tbody></table>
<table border="0" width="100%"><tbody><tr>
<td width="150"></td>
<td> <hr> </td>
</tr></tbody></table>
<table cellspacing="0" cellpadding="0" width="770">
<tbody><tr><td></td></tr>
<tr>
<td width="190"></td>
<td colspan="2"><b>AC-Leistung</b></td>
<td>&nbsp;</td>
<td><b>Energie</b></td></tr>
<tr><td height="10"></td></tr>
<tr>
<td width="190"></td>
<td width="100">aktuell</td>
<td width="70" align="right" bgcolor="#FFFFFF">2389</td>
<td width="140">&nbsp; W</td>
<td width="100">Gesamtenergie</td>
<td width="70" align="right" bgcolor="#FFFFFF">88938</td>
<td width="50">&nbsp; kWh</td>
<td>&nbsp;</td></tr>
<tr height="2"><td></td></tr>
<tr>
<td width="190"></td>
<td width="100">&nbsp;</td>
<td width="70" align="right">&nbsp;</td>
<td width="140">&nbsp;</td>
<td width="100">Tagesenergie</td>
<td width="70" align="right" bgcolor="#FFFFFF">13.49</td>
<td width="50">&nbsp; kWh</td>
<td>&nbsp;</td></tr>
<tr height="5"><td></td></tr>
<tr>
<td width="190"></td>
<td width="100">Status</td>
<td colspan="4">Einspeisen (MPP)</td>
<td>&nbsp;</td></tr>
<tr height="8"><td></td></tr>
<tr><td colspan="7">
<table align="top" width="100%"><tbody><tr>
<td width="182"></td>
<td><hr size="1"></td></tr>
<tr><td height="5"></td></tr></tbody></table>
</td></tr>
<tr>
<td width="190"></td>
<td colspan="2"><b>PV-Generator</b></td>
<td width="140">&nbsp;</td>
<td colspan="2"><b>Ausgangsleistung</b></td>
<td width="30">&nbsp;</td>
<td>&nbsp;</td></tr>
<tr><td height="10"></td></tr>
<tr>
<td width="190"></td>
<td width="100"><u>String 1</u></td>
<td width="70">&nbsp;</td>
<td width="140">&nbsp;</td>
<td width="95"><u>L1</u></td>
<td width="70">&nbsp;</td>
<td width="30">&nbsp;</td>
<td>&nbsp;</td></tr>
<tr>
<td width="190"></td>
<td width="100">Spannung</td>
<td width="70" align="right" bgcolor="#FFFFFF">480</td>
<td width="140">&nbsp; V</td>
<td width="100">Spannung</td>
<td width="70" align="right" bgcolor="#FFFFFF">238</td>
<td width="30">&nbsp; V</td>
<td>&nbsp;</td></tr>
<tr height="2"><td></td></tr>
<tr valign="top" align="left">
<td width="190">&nbsp;</td>
<td width="100">Strom</td>
<td width="70" align="right" bgcolor="#FFFFFF">4.69</td>
<td width="140">&nbsp; A</td>
<td width="100">Leistung</td>
<td width="70" align="right" bgcolor="#FFFFFF">789</td>
<td width="30">&nbsp; W</td>
<td>&nbsp;</td></tr>
<tr height="22"><td></td></tr>
<tr>
<td width="190"></td>
<td width="100"><u>String 2</u></td>
<td width="70">&nbsp;</td>
<td width="140">&nbsp;</td>
<td width="100"><u>L2</u></td>
<td width="70">&nbsp;</td>
<td width="30">&nbsp;</td>
<td>&nbsp;</td></tr>
<tr>
<td width="190"></td>
<td width="100">Spannung</td>
<td width="70" align="right" bgcolor="#FFFFFF">573</td>
<td width="140">&nbsp; V</td>
<td width="100">Spannung</td>
<td width="70" align="right" bgcolor="#FFFFFF">231</td>
<td width="30">&nbsp; V</td>
<td>&nbsp;</td></tr>
<tr height="2"><td></td></tr>
<tr valign="top" align="left">
<td width="190">&nbsp;</td>
<td width="100">Strom</td>
<td width="70" align="right" bgcolor="#FFFFFF">0.47</td>
<td width="140">&nbsp; A</td>
<td width="100">Leistung</td>
<td width="70" align="right" bgcolor="#FFFFFF">798</td>
<td width="30">&nbsp; W</td>
<td>&nbsp;</td></tr>
<tr height="22"><td></td></tr>
<tr>
<td width="190"></td>
<td width="100"><u> </u></td>
<td width="70">&nbsp;</td>
<td width="140">&nbsp;</td>
<td width="100"><u>L3</u></td>
<td width="70">&nbsp;</td>
<td width="30">&nbsp;</td>
<td>&nbsp;</td></tr>
<tr>
<td width="190"></td>
<td width="100"> </td>
<td width="70" align="right" bgcolor="#EAF7F7"> </td>
<td width="140">&nbsp; </td>
<td width="95">Spannung</td>
<td width="70" align="right" bgcolor="#FFFFFF">232</td>
<td width="30">&nbsp; V</td>
<td>&nbsp;</td></tr>
<tr height="2"><td></td></tr>
<tr valign="top" align="left">
<td width="190">&nbsp;</td>
<td width="95"> </td>
<td width="70" align="right" bgcolor="#EAF7F7"> </td>
<td width="140">&nbsp; </td>
<td width="95">Leistung</td>
<td width="70" align="right" bgcolor="#FFFFFF">802</td>
<td width="30">&nbsp; W</td>
<td>&nbsp;</td></tr>
</tbody></table>
</body></html>"""


def main() -> int:
    v = parse(PAGE, download_time_ms=101)
    print(f"current_ac_power_w = {v.current_ac_power_w}")
    print(f"produced_energy_kwh = {v.produced_energy_kwh}")
    print(f"daily_energy_kwh = {v.daily_energy_kwh}")
    print(f"status = {v.status!r}")
    print(f"string1: {v.string1_voltage_v}V {v.string1_current_a}A -> {v.string1_power_w}W")
    print(f"string2: {v.string2_voltage_v}V {v.string2_current_a}A -> {v.string2_power_w}W")
    print(f"L1: {v.l1_voltage_v}V {v.l1_power_w}W")
    print(f"L2: {v.l2_voltage_v}V {v.l2_power_w}W")
    print(f"L3: {v.l3_voltage_v}V {v.l3_power_w}W")
    print(f"string_power_w = {v.string_power_w}")
    print(f"efficiency = {v.efficiency}")
    print(f"download_time_ms = {v.download_time_ms}")

    failures: list[str] = []
    if v.current_ac_power_w != 2389:
        failures.append(f"current_ac_power_w expected 2389, got {v.current_ac_power_w}")
    if v.daily_energy_kwh != 13.49:
        failures.append(f"daily_energy_kwh expected 13.49, got {v.daily_energy_kwh}")
    if v.download_time_ms != 101:
        failures.append(f"download_time_ms expected 101, got {v.download_time_ms}")
    if v.status != "Einspeisen":
        failures.append(f"status expected 'Einspeisen', got {v.status!r}")
    if v.produced_energy_kwh != 88938:
        failures.append(f"produced_energy_kwh expected 88938, got {v.produced_energy_kwh}")

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nOK - all assertions pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
