# coding: utf-8
# !/usr/bin/python

"""
Project: simulator
Sat Apr 22 16:34:34 2017
"""

import math

from simulator.models.Model import Model
from simulator.miscs import Table
from simulator.models.electrical import LionBattery, Ultracapacitor
from simulator.errors.ModelError import ModelError

# Author
__author__ = 'Jason Xing Zhang'
__email__ = 'xingz@uvic.ca'


class HessActive(Model):
    """
    model of the active HESS (no dc-dc)
    """
    def __init__(self, b_resistor, b_soc, b_ocv, b_init_soc, b_thermal_mass,
             atemp, b_cap, c_resistor, capacitor, c_init_soc, c_max_voltage
            ):
        """
        initialization

        Args:
            b_resistor (list): resistor value
            b_soc (list): state of charge (table axis)
            b_ocv (list): open circuit voltage (table value)
            b_init_soc (float): initial soc
            b_thermal_mass (float): thermal mass
            atemp (float): ambient temp
            b_cap (float): capacity
            c_resistor (float): capacitor resistor
            capacitor (float): capacitor
            c_init_soc (float): capacitor initial soc
            c_max_voltage (float): capacitor max voltage
        """
        super(HessActive, self).__init__()
        self.battery = LionBattery.LionBattery(
            b_resistor, b_soc, b_ocv, b_init_soc, b_thermal_mass, atemp, b_cap
        )
        self.ucap = Ultracapacitor.Ultracapacitor(
            c_resistor, capacitor, c_init_soc, c_max_voltage
        )
        self.current = 0
        self.voltage = self.battery.voltage

    def rule(self, inputs):
        """
        define the relation between inputs and outputs
        """
        if all(k in inputs.keys() for k in ('battery_current', 'uc_current')):
            self.ucap(**inputs)
            inputs['battery_current'] = inputs['battery_current'] + \
                    inputs['uc_current'] - self.ucap.current
            self.voltage = self.battery(**inputs)
            self.current = self.ucap.current + self.battery.current
        else:
            raise ModelError('Input current loads for both devices')

