from .kiauvoeurope import kiauvoeurope
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import dt
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, UNIT_PERCENTAGE
from datetime import timedelta
from typing import List, Dict, Callable, Any
from .const import DOMAIN
import requests, json, time, re
import logging

SCAN_INTERVAL = timedelta(seconds=180)
_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "batteryStatus": {
        "path": "evStatus.batteryStatus",
        "attrs": [],
        "unit": None,
        "icon": "mdi:battery",
    },
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Kia sensor."""
    config = hass.data[DOMAIN]["config"]
    
    sensors = []
        
    for key in SENSOR_TYPES:
        sensors.append(
            UVOSensor(DOMAIN + "_" + key, None, config.data[CONF_USERNAME], config.data[CONF_PASSWORD])
        )

    async_add_entities(sensors)


class UVOSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name, state, username, password):
        """Initialize the sensor."""
        self._state = state
        self._sensor_name = name
        self.username = username
        self.password = password

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._sensor_name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return UNIT_PERCENTAGE

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """

        mykia = kiauvoeurope()
        mykia.get_session()
        mykia.set_language()
        resp = mykia.login(self.username, self.password)
        if "redirectUrl" not in resp:
            _LOGGER.error("Failed to sign into UVO service")
            return
        m = re.search('code=([^&]*)', resp["redirectUrl"])
        refreshToken = m.group(1)
        resp = mykia.register()
        deviceId = resp["resMsg"]["deviceId"]
        resp = mykia.get_token(refreshToken)
        accessToken = resp["access_token"]
        resp = mykia.get_vehicles(accessToken, deviceId)
        vehicleId = resp["resMsg"]["vehicles"][0]["vehicleId"]
        resp = mykia.get_vehicle_status(accessToken, deviceId, vehicleId)
        batteryLevel = resp["resMsg"]["evStatus"]["batteryStatus"]

        self._state = batteryLevel

    @property
    def device_info(self):
        """Return the device information."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": "Kia UVO Europe",
            "manufacturer": "Kia",
            "model": "Kia UVO Europe",
        }
