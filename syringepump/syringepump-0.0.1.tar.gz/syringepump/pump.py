#!/usr/bin/env python

import time

from . import commands
from . import protocols


class Pump(object):
    def __init__(self, conn, protocol=None):
        self.conn = conn
        if protocol is None:
            self.protocol = protocols.Basic()

    def send_command(self, cmd):
        msg = self.protocol.format_message(cmd)
        print("write -> %s" % msg)
        self.conn.write(msg)
        return self.get_response()

    def get_response(self):
        # TODO timeouts, polling, etc...
        msg = self.conn.read_until('\x03')
        print("read <- %s" % msg)
        return self.protocol.parse_response(msg)

    # TODO setup commands as properties

    def ping(self):
        self.send_command("")

    def set_diameter(self, diameter):
        return self.send_command(commands.set_diameter(diameter))

    def set_phase(self, phase):
        return self.send_command(commands.set_phase(phase))

    def set_function(self, function):
        return self.send_command(commands.set_function(function))

    def set_rate(self, rate, units='MM', mode=None):
        return self.send_command(commands.set_rate(rate, units, mode))

    def set_volume_units(self, units):
        return self.send_command(commands.set_volume_units(units))

    def set_volume(self, volume):
        return self.send_command(commands.set_volume(volume))

    def set_direction(self, direction):
        return self.send_command(commands.set_direction(direction))

    def run(self, phase=None):
        return self.send_command(commands.run(phase))

    def set_buzzer(self, state, repeats=None):
        return self.send_command(commands.set_buzzer(state, repeats))

    def buzz(self, duration=0.05):
        self.set_buzzer(True)
        time.sleep(duration)
        self.set_buzzer(False)
