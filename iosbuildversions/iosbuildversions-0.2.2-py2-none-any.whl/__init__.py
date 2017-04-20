from __future__ import absolute_import

from iosbuildversions.builds import build_list as _builds


def get_builds():
    """Returns all builds in memory
    
    Returns:
        Dict of builds.

    """
    return _builds


def lookup_by_build(build):
    """Returns build information
    
    Args:
        build: iOS build number. (Ex. 12B435)

    Returns:
        (Dict):
            (string) name: The name of the release.
            (bool) beta: Flag if the release is a beta release.
            (bool) final: Flag is the release is a final release.
            (string) build: The iOS build number.

    """
    try:
        return _builds[build]
    except KeyError:
        return False
