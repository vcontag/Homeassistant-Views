"""Einrichtungsdialog für Home Assistant Views."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .const import CONF_SIDEBAR, CONF_TOKEN, DEFAULT_SIDEBAR, DOMAIN, VIEWS


def _schema(options: Mapping[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Optional(
                CONF_SIDEBAR, default=list(options.get(CONF_SIDEBAR, DEFAULT_SIDEBAR))
            ): cv.multi_select({v.key: v.title for v in VIEWS}),
            vol.Optional(
                CONF_TOKEN, description={"suggested_value": options.get(CONF_TOKEN, "")}
            ): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD)),
        }
    )


class HaViewsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Einrichtung über die Oberfläche."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(title="Home Assistant Views", data={}, options=user_input)
        return self.async_show_form(step_id="user", data_schema=_schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return HaViewsOptionsFlow()


class HaViewsOptionsFlow(OptionsFlow):
    """Optionen: Seitenleiste und festes Token."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)
        return self.async_show_form(step_id="init", data_schema=_schema(self.config_entry.options))
