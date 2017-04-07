"""LimitlessLED Version 4 Module

From what I can gather on http://www.limitlessled.com/dev
this should also be compatible with a version 5 wifi bridge.
"""
import socket
import math
from mookfist_lled_controller.exceptions import NoBridgeFound
from mookfist_lled_controller.exceptions import InvalidGroup

def get_bridge():
    """Get first available bridge"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    sock.bind(('', 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    counter = 0
    max_tries = 5

    while counter < max_tries:
        try:
            sock.sendto('Link_Wi-Fi', ('255.255.255.255', 48899))
            data = sock.recv(1024)
            if data:
                host, mac = data.split(',')[:2]
                return (host, mac)
        except socket.timeout:
            counter = counter + 1

    raise NoBridgeFound()


class Command(object):
    """A LimitlessLED Command"""

    def __init__(self, cmd, value=0x00, suffix=None):
        """
        cmd: command to send
        value: value of command, if any (defaults to 0x00)
        suffix: suffix value at the end of the command if any
        """
        self.cmd = cmd
        self.value = value
        self.suffix = suffix

    def message(self):
        """Get an array representation of the message"""
        if self.suffix != None:
            return [self.cmd, self.value, self.suffix]
        else:
            return [self.cmd, self.value]


class Group(object):
    """Represents a group of lights"""

    def __init__(self, group):
        """
        group: group number (1-4)
        """
        self.group = group

    def on(self):
        """
        get the On command for this group
        """
        if self.group == 1:
            cmd = 0x45
        elif self.group == 2:
            cmd = 0x47
        elif self.group == 3:
            cmd = 0x49
        elif self.group == 4:
            cmd = 0x4B
        else:
            raise InvalidGroup() 

        return Command(cmd)

    def off(self):
        """
        get the Off command for this group
        """
        if self.group == 1:
            cmd = 0x46
        elif self.group == 2:
            cmd = 0x48
        elif self.group == 3:
            cmd = 0x4A
        elif self.group == 4:
            cmd = 0x4C
        else:
            raise InvalidGroup()

        return Command(cmd)

    def color(self, color):
        """get the Color command for this group and color (0-255)"""
        color = color + 176
        if color > 255:
            color = color - 255
        return Command(0x40, color)

    def brightness(self, brightness):
        """"get the brightness command for this group and brightness (0-100%)
        
            LimitlessLED only supports values 2 to 27 for brightness, so this percentage
            is actually a percentage of the value 25
        
        """
        target_brightness = int(math.ceil(25 * (brightness / 100.0)) + 2)

        """get the Brightness command for this group and brightnes (2-27)"""
        return Command(0x4E, target_brightness)

