import typing

from aiolifx import aiolifx


class Bulbs():
    """ A simple class with a register and  unregister methods
    """
    def __init__(self):
        self.bulbs = []

    def register(self, bulb):
        bulb.get_label()
        bulb.get_location()
        bulb.get_version()
        bulb.get_group()
        bulb.get_wififirmware()
        bulb.get_hostfirmware()
        self.bulbs.append(bulb)
        self.bulbs.sort(key=lambda x: x.label or x.mac_addr)

    def unregister(self, bulb):
        idx = 0
        for x in list([y.mac_addr for y in self.bulbs]):
            if x == bulb.mac_addr:
                del(self.bulbs[idx])
                break
            idx += 1

    def filter_group(self, compiled_regex: typing.re) -> typing.Generator[aiolifx.Light, None, None]:

        for bulb in self.bulbs:
            if compiled_regex.match(bulb.get_group()):
                yield bulb
