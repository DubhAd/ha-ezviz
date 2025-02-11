"""Provides the ezviz_cloud DataUpdateCoordinator."""
from datetime import timedelta
import logging

from async_timeout import timeout
from pyezviz.camera import EzvizCamera
from pyezviz.client import EzvizClient
from requests import ConnectTimeout, HTTPError

from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class EzvizDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ezviz data."""

    def __init__(self, hass: HomeAssistantType, *, api: EzvizClient):
        """Initialize global Ezviz data updater."""
        self.EzvizClient = api
        self.EzvizCamera = EzvizCamera
        update_interval = timedelta(seconds=30)

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    def _update_data(self) -> dict:
        """Fetch data from Ezviz via camera load function."""
        cameras = self.EzvizClient.load_cameras()

        return cameras

    async def _async_update_data(self) -> dict:
        """Fetch data from Ezviz."""
        try:
            async with timeout(15):
                return await self.hass.async_add_executor_job(self._update_data)

        except (ConnectTimeout, HTTPError) as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error
