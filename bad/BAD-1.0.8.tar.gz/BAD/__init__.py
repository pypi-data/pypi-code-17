# coding=utf-8
import os
import re
from Device import Device
from Element import Element

__version__ = '1.0'
__author__ = 'bony'
# __all__ = ['BAndroidDriver', 'Element']
"""
BAD
"""


def get_device(_id=None, name=None):
    devices = get_devices()
    if len(devices) > 0:
        if _id is None:
            if name is None:
                return devices[0]
            else:
                device = devices[0]
                device._name = name
                return device
        else:
            if get_by_id_device(_id) is None:
                print(u"未找到匹配设备!")
                return None
            else:
                device = get_by_id_device(_id)
                if name is None:
                    return device
                else:
                    device._name = name
                    return device
    else:
        print(u"未连接设备!")
        return None


def existence_device(device):
    if device._id is None:
        return False
    else:
        return True


def get_by_id_device(_id):
    devices = get_devices()
    for device in devices:
        if device.Id == _id:
            return device
    return None


def get_devices():
    devices = []
    line = shell("adb devices -l").split("\n")
    for string in line:
        if "device" in string and "product" in string:
            devices_list = re.compile(r"((?:[a-zA-Z0-9\w]+))").findall(string)
            devices.append(Device(devices_list[0], devices_list[3]))
    return devices


def shell(script):
    return os.popen(script).read().strip()
