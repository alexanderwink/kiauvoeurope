import logging
import asyncio
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, VERSION

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ("sensor",)


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
    hass.data[DOMAIN]["config"] = entry

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN] = {}

    return unload_ok
