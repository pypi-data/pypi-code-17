# coding: utf-8
# !/usr/bin/python

"""
Project: simulator
Wed Jul 20 00:07:48 2016
"""

from simulator.models.Model import Model
from simulator.miscs.Table import Table
from simulator.errors.ModelError import ModelError

# Author
__author__ = 'Jason Xing Zhang'
__email__ = 'xingz@uvic.ca'


class ResistorForBattery(Model):
    """
    model of a resistor for lion battery
    """
    def __init__(self, soc, resistor, atemp, thermal_mass, cp=521, ele_mod=6):
        """
        initialization

        Args:
            soc (list): soc list (Table axis)
            resistor (list): resistor value list (Table values)
            atemp (float): ambient temp
            thermal_mass (float): equivalent thermal mass
            cp (float): heat capacitor, default to the li-on battery
            ele_mod (int): number of series elements per module
        """
        super(ResistorForBattery, self).__init__()
        self.set_parameters('mass', thermal_mass)
        self.set_parameters('cp', cp)
        self.set_parameters('rmap', Table(soc, resistor))
        self.current = 0
        self.voltage = 0
        self.r = resistor[0]
        self.temp = atemp
        self.old_heat = 0
        self.ele_mod = ele_mod

    def _calculate_temp(self, step):
        """
        calculate temp
        """
        heat = self.current ** 2 * self.r / self.parameters.mass \
                / self.parameters.cp * self.ele_mod
        self.temp += (self.old_heat + heat) / 2 * step
        self.old_heat = heat

    def rule(self, inputs):
        """
        define the relation between inputs and outputs

        Args:
            inputs(dict): {input_name: input_value}
        """
        if 'soc' in inputs.keys():
            self.r = self.parameters.rmap[inputs['soc']]
            if 'current' in inputs.keys():
                self.current = inputs['current']
                self.voltage = self.r * inputs['current']
                output = self.voltage
            elif 'voltage' in inputs.keys():
                self.voltage = inputs['voltage']
                self.current = inputs['voltage'] / self.parameters.r
                output = self.current
            else:
                raise ModelError("Input current or voltage")
            self._calculate_temp(inputs['step'])
            return output
        else:
            raise ModelError("Input soc")
