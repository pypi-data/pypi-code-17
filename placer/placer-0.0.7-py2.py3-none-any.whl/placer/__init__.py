import sys

__project__ = "placer"
__version__ = "0.0.7"
__repo__ = "https://github.com/kootenpv/placer"


def print_version():
    sv = sys.version_info
    py_version = "{}.{}.{}".format(sv.major, sv.minor, sv.micro)
    s = ""
    s += "placer version: [{}], Python {}\n".format(__version__, py_version)
    version_parts = __version__.split(".")
    s += "major version: {}  (breaking changes)\n".format(version_parts[0])
    s += "minor version: {}  (extra feature)\n".format(version_parts[1])
    s += "micro version: {} (commit count)\n".format(version_parts[2])
    s += "Find out the most recent version at {}".format(__repo__)
    print(s)
    return s
