"""Python module for ZWay Controller"""

import logging
from typing import List
from requests import Session
from zway.devices import GenericDevice, create_device


_LOGGER = logging.getLogger(__name__)


class Controller(object):
    """Z-Way Controller"""

    def __init__(self,
                 baseurl: str,
                 username: str=None,
                 password: str=None) -> None:
        self._session = Session()
        self._session.auth = (username, password)
        self._prefix = baseurl + "/ZAutomation/api/v1"

    @property
    def devices(self) -> List[GenericDevice]:
        """Return all known devices (except those permanently hidden)"""
        return self.get_all_devices()

    def get_all_devices(self) -> List[GenericDevice]:
        """Return all known devices (except those permanently hidden)"""
        response = self._session.get(self._prefix + "/devices")
        all_devices = []
        for device_dict in response.json().get('data').get('devices'):
            if device_dict['permanently_hidden']:
                continue
            all_devices.append(create_device(device_dict, self._session, self._prefix))
        return all_devices

    def get_device(self, device_id: str) -> GenericDevice:
        """Return single device by ID"""
        response = self._session.get(self._prefix + "/devices/" + device_id)
        device_dict = response.json().get('data')
        return create_device(device_dict, self._session, self._prefix)
