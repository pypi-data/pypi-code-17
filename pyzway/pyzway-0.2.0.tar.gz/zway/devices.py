"""Python module for ZWay Devices"""

import logging
from typing import Tuple
from requests import Session


_LOGGER = logging.getLogger(__name__)


class GenericDevice(object):
    def __init__(self, data: dict, session: Session, prefix: str) -> None:
        self._session = session
        self._prefix = prefix
        self._update_attrs(data)

    def update(self) -> None:
        """Update object with data from ZWay"""
        data = self._session.get(self._prefix + "/devices/" + self.id).json().get('data')
        self._update_attrs(data)

    def _update_attrs(self, data: dict) -> None:
        """Update attributes given data from ZWay"""
        self._data = data
        self.id = self._data['id']
        self.title = self._data['metrics'].get('title')
        self.visible = self._data['visibility']
        self.devicetype = self._data['deviceType']

    def is_tagged(self, tag: str=None) -> bool:
        """Return True if device has specified tag"""
        if tag is not None:
            return tag in self._data.get('tags', [])
        else:
            return True


class GenericBinaryDevice(GenericDevice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update_attrs(self, data: dict):
        super()._update_attrs(data)
        if data['metrics']['level'] == 'on':
            self._on = True
        elif data['metrics']['level'] == 'off':
            self._on = False
        else:
            self._on = None

    @property
    def on(self) -> bool:
        return self._on


class GenericMultiLevelDevice(GenericDevice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update_attrs(self, data: dict) -> None:
        super()._update_attrs(data)
        self._level = data['metrics']['level']

    @property
    def on(self) -> bool:
        return self._level > 0

    @property
    def level(self) -> int:
        return self._level


class SwitchBinary(GenericBinaryDevice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def on(self) -> bool:
        return self._on

    @on.setter
    def on(self, value: bool) -> None:
        if value:
            command = "on"
        else:
            command = "off"
        self._session.get(self._prefix + "/devices/{}/command/{}".format(self.id, command))


class SwitchMultilevel(GenericMultiLevelDevice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def on(self) -> bool:
        return self._level > 0

    @on.setter
    def on(self, value: bool) -> None:
        if value:
            self.level = 255
        else:
            self.level = 0

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        self._session.get(self._prefix + "/devices/{}/command/exact?level={}".format(self.id, value))


class SwitchRGBW(SwitchBinary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update_attrs(self, data: dict) -> None:
        super()._update_attrs(data)
        self._red = data['metrics']['color']['r']
        self._green = data['metrics']['color']['g']
        self._blue = data['metrics']['color']['b']

    @property
    def rgb(self) -> Tuple[int, int, int]:
        return (self._red, self._green, self._blue)

    @rgb.setter
    def rgb(self, color: Tuple[int, int, int]) -> None:
        (red, green, blue) = color
        self._session.get(self._prefix + "/devices/{}/command/exact?red={}&green={}&blue={}".format(self.id, red, green, blue))


class SensorBinary(GenericBinaryDevice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SensorMultilevel(GenericMultiLevelDevice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update_attrs(self, data: dict) -> None:
        super()._update_attrs(data)
        self._unit = data['metrics']['scaleTitle']

    @property
    def unit(self) -> int:
        return self._unit


def create_device(device_dict: dict, session: Session, prefix: str) -> GenericDevice:
    """Create ZWay device from device data dictionary"""
    device_class_map = {
        'switchBinary': SwitchBinary,
        'switchMultilevel': SwitchMultilevel,
        'switchRGBW': SwitchRGBW,
        'sensorBinary': SensorBinary,
        'sensorMultilevel': SensorMultilevel,
    }
    device_type = device_dict['deviceType']
    cls = device_class_map.get(device_type, GenericDevice)
    return cls(device_dict, session, prefix)
