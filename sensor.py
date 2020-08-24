#from voluptuous.error import Error

from homeassistant.helpers import device_registry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import dt
from homeassistant.const import UNIT_PERCENTAGE

from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=180)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Kia sensor."""
#    config = hass.data[DOMAIN]["config"]

    sensors = []

    sensors.append(
        ChargerSensor(DOMAIN + "_battery_level", None)
    )

    async_track_time_interval(hass, chargers_data.async_refresh, SCAN_INTERVAL)
    async_add_entities(sensors)


class ChargerSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name, state):
        """Initialize the sensor."""
        self._state = state
        self._sensor_name = name

    @property
    def name(self):
        """Return the name of the sensor."""
#        return 'Battery Level'
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
        self._state = 13
