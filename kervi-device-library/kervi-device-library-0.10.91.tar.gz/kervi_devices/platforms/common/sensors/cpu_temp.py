# Copyright (c) 2016, Tim Wentzlau
# Licensed under MIT

""" Module that defines core cpu sensors """

from kervi.hal import SensorDeviceDriver
import psutil
from pyspectator.processor import Processor

class CPUTempSensorDeviceDriver(SensorDeviceDriver):
    """ Sensor that mesures cpu temp on host """
    def __init__(self):
        try:
            self.cpu = Processor(monitoring_latency=1)
        except:
            self.cpu = None

    def read_value(self):
        return 0
        # try:
        #     print("cptu",psutil.sensors_temperatures())
        #     if self.cpu:
        #         print("cpt:", self.cpu.temperature)
        #     return 0
        # except:
        #     return 0

    @property
    def max(self):
        return 150

    @property
    def min(self):
        return 0

    @property
    def type(self):
        return "temperature"

    @property
    def unit(self):
        return "C"
