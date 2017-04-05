"""Simple tool to convert IPv4 address to hex.

Useful for PXE booting config and whatever other use
case you can come up with.

MIT License

Copyright (c) 2017 Theuns Alberts
"""

def validate_ip4(iplist):
    """IPv4 integer list as input with boolean as output."""
    return all([(v>=0 and v<=255) for v in iplist])


def ip4_to_hex(ipstr):
    """IPv4 string as input with hex string as output.

    Note:
    Can throw all kinds of Exceptions so be sure to
    catch them.
    """

    iplist = [int(v) for v in ipstr.split('.')]
    if not validate_ip4(iplist):
        raise AttributeError("Not valid IPv4 address.")
    hexip = "%0.2X%0.2X%0.2X%0.2X" % tuple(iplist)
    return hexip
