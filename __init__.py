import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, VERSION

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Kia integration component."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    
    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Kia integration from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    _LOGGER.debug("Setting up Kia component version %s", VERSION)
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    
    return True
