from typing import Optional
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.typing import ConfigType
import voluptuous as vol
from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class KiaUvoEuropeConfigFlow(config_entries.ConfigFlow):
	"""Flow"""

	async def async_step_user(self, user_input: Optional[ConfigType] = None):
		"""Flow start"""

		entries = self.hass.config_entries.async_entries(DOMAIN)
		if entries:
        		return self.async_abort(reason="already_setup")

		errors = {}

		if user_input is not None:
			username = user_input[CONF_USERNAME]
			password = user_input[CONF_PASSWORD]

			try:
				return self.async_create_entry(title=username, data=user_input)
			except Exception:
				errors["base"] = "connection_failure"

		return self.async_show_form(
			step_id="user",
			data_schema=vol.Schema(
				{vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
			),
			errors=errors,
		)

	async def async_step_import(self, user_input: Optional[ConfigType] = None):
		"""Occurs when an entry is setup through config."""
		return await self.async_step_user(user_input)
