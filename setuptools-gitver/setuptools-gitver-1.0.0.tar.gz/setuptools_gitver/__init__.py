import subprocess

import pkg_resources
from setuptools.command.egg_info import egg_info


def get_version(name):
    try:
        return pkg_resources.get_distribution(name).version
    except pkg_resources.DistributionNotFound:
        return None


__version__ = get_version(__name__)


class EggInfoCommand(egg_info):
    command_name = 'egg_info'

    def tagged_version(self):
        version = egg_info.tagged_version(self)
        if version.lower().endswith('+gitver'):
            parsed_ver = pkg_resources.parse_version(version)
            (count, suffix) = do_git_describe(parsed_ver.base_version)
            return parsed_ver.public + '.dev' + str(count) + '+' + suffix
        return version


def do_git_describe(base_version):
    cmd = 'git describe --dirty --always --long --match'.split()
    for ver in ['v' + base_version, base_version]:
        pipe = subprocess.Popen(cmd + [ver], stdout=subprocess.PIPE)
        (output, _) = pipe.communicate()
        decoded = output.decode('utf-8', errors='ignore').strip()
        if decoded and decoded.startswith(ver):
            (count, rest) = decoded[len(ver):].lstrip('-').split('-', 1)
            return (count, rest)
    return ('0', decoded)
