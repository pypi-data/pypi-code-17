"""Python module for ZWay Controller"""

import logging
from typing import List
from zway.session import ZWaySession
import zway.devices


_LOGGER = logging.getLogger(__name__)


class Controller(object):
    """Z-Way Controller"""

    def __init__(self,
                 baseurl: str,
                 username: str=None,
                 password: str=None):
        self._zsession = ZWaySession(baseurl=baseurl)
        self._zsession.auth = (username, password)

    @property
    def devices(self) -> List[zway.devices.GenericDevice]:
        """Return all known devices (except those permanently hidden)"""
        return self.get_all_devices()

    def get_all_devices(self) -> List[zway.devices.GenericDevice]:
        """Return all known devices (except those permanently hidden)"""
        response = self._zsession.get("/devices")
        all_devices = []
        for device_dict in response.json().get('data').get('devices'):
            if device_dict['permanently_hidden']:
                continue
            all_devices.append(self._get_device_object(device_dict))
        return all_devices

    def get_device(self, device_id: str) -> zway.devices.GenericDevice:
        """Return single device by ID"""
        response = self._zsession.get("/devices/" + device_id)
        return self._get_device_object(response.json().get('data'))

    def _get_device_object(self, device_dict) -> zway.devices.GenericDevice:
        """Build device object from device data dictionary"""
        device_type = device_dict['deviceType']
        if device_type == 'switchBinary':
            return zway.devices.SwitchBinary(device_dict, self._zsession)
        elif device_type == 'switchMultilevel':
            return zway.devices.SwitchMultilevel(device_dict, self._zsession)
        elif device_type == 'switchRGBW':
            return zway.devices.SwitchRGBW(device_dict, self._zsession)
        elif device_type == 'sensorBinary':
            return zway.devices.SensorBinary(device_dict, self._zsession)
        elif device_type == 'sensorMultilevel':
            return zway.devices.SensorMultilevel(device_dict, self._zsession)
        else:
            return zway.devices.GenericDevice(device_dict, self._zsession)
