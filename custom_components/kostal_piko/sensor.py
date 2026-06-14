"""Sensor platform for the Kostal PIKO (TK) integration.

Exposes every field of KostalValues as a Home Assistant sensor entity.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_HOST,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import KostalConfigEntry
from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import KostalCoordinator
from .parser import KostalValues


@dataclass(frozen=True, kw_only=True)
class KostalSensorDescription(SensorEntityDescription):
    """Describes a Kostal sensor and how to read its value."""

    value_fn: Callable[[KostalValues], float | int | str | None]


SENSORS: tuple[KostalSensorDescription, ...] = (
    KostalSensorDescription(
        key="current_ac_power_w",
        translation_key="current_ac_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.current_ac_power_w,
    ),
    KostalSensorDescription(
        key="produced_energy_kwh",
        translation_key="produced_energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda v: v.produced_energy_kwh,
    ),
    KostalSensorDescription(
        key="daily_energy_kwh",
        translation_key="daily_energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda v: v.daily_energy_kwh,
    ),
    KostalSensorDescription(
        key="status",
        translation_key="status",
        value_fn=lambda v: v.status,
    ),
    KostalSensorDescription(
        key="efficiency",
        translation_key="efficiency",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.efficiency,
    ),
    KostalSensorDescription(
        key="string_power_w",
        translation_key="string_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.string_power_w,
    ),
    # --- String 1 ---
    KostalSensorDescription(
        key="string1_voltage_v",
        translation_key="string1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.string1_voltage_v,
    ),
    KostalSensorDescription(
        key="string1_current_a",
        translation_key="string1_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.string1_current_a,
    ),
    KostalSensorDescription(
        key="string1_power_w",
        translation_key="string1_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.string1_power_w,
    ),
    # --- String 2 ---
    KostalSensorDescription(
        key="string2_voltage_v",
        translation_key="string2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.string2_voltage_v,
    ),
    KostalSensorDescription(
        key="string2_current_a",
        translation_key="string2_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.string2_current_a,
    ),
    KostalSensorDescription(
        key="string2_power_w",
        translation_key="string2_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.string2_power_w,
    ),
    # --- L1 ---
    KostalSensorDescription(
        key="l1_voltage_v",
        translation_key="l1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.l1_voltage_v,
    ),
    KostalSensorDescription(
        key="l1_power_w",
        translation_key="l1_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.l1_power_w,
    ),
    # --- L2 ---
    KostalSensorDescription(
        key="l2_voltage_v",
        translation_key="l2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.l2_voltage_v,
    ),
    KostalSensorDescription(
        key="l2_power_w",
        translation_key="l2_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.l2_power_w,
    ),
    # --- L3 ---
    KostalSensorDescription(
        key="l3_voltage_v",
        translation_key="l3_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.l3_voltage_v,
    ),
    KostalSensorDescription(
        key="l3_power_w",
        translation_key="l3_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda v: v.l3_power_w,
    ),
    # --- Diagnostics ---
    KostalSensorDescription(
        key="download_time_ms",
        translation_key="download_time",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda v: v.download_time_ms,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: KostalConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Kostal sensors from a config entry."""
    coordinator = entry.runtime_data
    host = entry.data[CONF_HOST]
    async_add_entities(
        KostalSensor(coordinator, entry.entry_id, host, description)
        for description in SENSORS
    )


class KostalSensor(CoordinatorEntity[KostalCoordinator], SensorEntity):
    """A single value read from the Kostal inverter."""

    entity_description: KostalSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: KostalCoordinator,
        entry_id: str,
        host: str,
        description: KostalSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=f"{MANUFACTURER} {MODEL}",
            manufacturer=MANUFACTURER,
            model=MODEL,
            configuration_url=f"http://{host}/",
        )

    @property
    def native_value(self) -> float | int | str | None:
        """Return the current value of this sensor."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
