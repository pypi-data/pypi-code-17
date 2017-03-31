# coding=utf-8
import os
import re
from Device import Device
from Element import Element

__version__ = '1.0'
__author__ = 'bony' 
# __all__ = ['BAndroidDriver', 'Element']
'''
BAndroidDriver
'''
def getDevice(Id=None, Name=None):
	devices = getDevices()
	if len(devices)>0:
		if Id == None:
			if Name == None:
				return devices[0]
			else:
				device = devices[0]
				device.Name = Name
				return device
		else:
			if getByIdDevice(Id) == None:
				print(u"未找到匹配设备!")
				return None
			else:
				device = getByIdDevice(Id)
				if Name == None:
					return device
				else:
					device.Name = Name
					return device
	else:
		print(u"未连接设备!")
		return None

def existenceDevice(Device):
	device = getByIdDevice(Device.Id)
	if device == None:
		return False
	else:
		return True

def getByIdDevice(Id):
	devices = getDevices()
	for device in devices:
		if device.Id == Id:
			return device
	return None


def getDevices():
	devices=[]
	line=shell("adb devices -l").split("\n")
	for string in line:
		if "device" in string and "product" in string:
			devices_list = re.compile(r"((?:[a-zA-Z0-9\w]+))").findall(string)
			devices.append(Device(devices_list[0],devices_list[7]))
	return devices

def shell(script):
	return os.popen(script).read().strip()

