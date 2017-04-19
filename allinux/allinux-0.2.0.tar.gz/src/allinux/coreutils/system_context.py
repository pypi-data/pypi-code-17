#
# System context
#

import argparse
from collections import namedtuple
import platform


def uname(options):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', action='store_true', help='print all of information')
    # linux uname command will output the following 8 information
    parser.add_argument('-s', '--kernel-name', action='store_true', help='print kernel name')
    parser.add_argument('-n', '--nodename', action='store_true', help='print the network node hostname')
    parser.add_argument('-r', '--kernel-release', action='store_true', help='print kernel release')
    parser.add_argument('-v', '--kernel-version', action='store_true', help='print kernel version')
    parser.add_argument('-m', '--machine', action='store_true', help='print machine hardware name')
    parser.add_argument('-p', '--processor', action='store_true', help='print processor type')
    parser.add_argument('-i', '--hardware-platform', action='store_true', help='print hardware platform name')
    parser.add_argument('-o', '--operating-system', action='store_true', help='print name of operating system')
    
    try:
        args = parser.parse_args(options.split())
    except SystemExit:
        return

    uname_field_names = [
        'kernel_name',
        'nodename',
        'kernel_release',
        'kernel_version',
        'machine',
        'processor',
        'hardware_platform',
        'operating_system'
    ]
    Uname = namedtuple('Uname', uname_field_names)
    py_uname = platform.uname()
    new_uname = Uname(
        py_uname.system,
        py_uname.node,
        py_uname.release,
        py_uname.version,
        py_uname.machine,
        py_uname.processor,
        py_uname.machine,
        py_uname.system
    )
    
    if args.all:
        return new_uname

    field_names = []
    uname_dict = {}
    for name in uname_field_names:
        if getattr(args, name):
            field_names.append(name)
            uname_dict[name] = getattr(new_uname, name)

    Uname = namedtuple('Uname', field_names)
    new_uname = Uname(**uname_dict)
    return new_uname
