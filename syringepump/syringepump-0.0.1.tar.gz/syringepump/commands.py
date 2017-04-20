#!/usr/bin/env python
"""
response parsing
00S  (address 0, status = stopped)
"""


def ftos(v):
    """
    maximum of 4 digits decimal point
    minimum of 3 digits to right of decimal
    """
    if v > 9999 or v < 0.:
        raise ValueError("Invalid float[out of range: 0, 9999]: %s" % v)
    return ('%.4f' % v)[:5]


def verify_phase(phase):
    if phase < 1 or phase > 41:
        raise ValueError("Invalid phase[out of range: 1, 41]: %s" % phase)
    return phase


def get_diameter():
    return "DIA"


def set_diameter(diameter):
    return "DIA %s" % ftos(diameter)


def get_phase():
    return "PHN"


def set_phase(phase):
    return "PHN %i" % verify_phase(phase)


def get_function():
    return "FUN"


def set_function(function):
    # TODO verify function
    return "FUN %s" % function


def get_rate():
    # TODO mode and units?
    return "RAT"


def set_rate(rate, units=None, mode=None):
    if mode is None:
        msg = "RAT %s" % ftos(rate)
    else:
        # TODO verify mode
        msg = "RAT %s" % (mode, ftos(rate))
    if units is None:
        return msg
    # TODO verify units
    return "%s %s" % (msg, units)


def get_volume():
    return "VOL"


def set_volume(volume, units=None):
    return "VOL %s" % ftos(volume)


def set_volume_units(units):
    # TODO verify units
    return "VOL %s" % units


def get_direction():
    return "DIR"


def set_direction(direction):
    # TODO verify direction: INF, WDR, REV, STK
    return "DIR %s" % direction


def run(phase=None):
    if phase is None:
        return "RUN"
    else:
        return "RUN %s" % verify_phase(phase)

# E event
# PUR purge


def stop():
    return "STP"


def get_volume_dispensed():
    return "DIS"


def clear_volume_dispensed(mode):
    # TODO verify mode: INF, WDR
    return "CLD %s" % mode


# LN low motor noise
# AL alarm setup
# PF power fail
# TRG trigger setup
# DIN ttl direction
# ROM
# LOC
# BP
# OUT
# IN
# BUZ

def get_buzzer():
    return "BUZ"


def set_buzzer(state, repeats=None):
    if state:
        if repeats is None:
            return "BUZ 1"
        else:
            return "BUZ 1 %i" % repeats
    else:
        return "BUZ 0"

# ADR
# SAF


def get_version():
    return "VER"


def reset():
    return "RESET"
