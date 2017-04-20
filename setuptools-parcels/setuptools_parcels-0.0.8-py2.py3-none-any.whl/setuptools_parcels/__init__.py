import os
import fnmatch
import logging

LOG = logging.getLogger(__name__)

DEFAULT_EXCLUDE_DIRS = ["__pycache__"]


def setup_keywords_entry_point(dist, attr, value):
    package_data = dist.package_data or {}
    exclude_dirs = value.get("exclude_dirs", DEFAULT_EXCLUDE_DIRS)
    _merge_all_package_data(dist.packages, package_data, exclude_dirs)
    dist.package_data = package_data


def _merge_all_package_data(package_list, package_data, exclude_dirs):
    """ find all package_data files, and merge that into package_data. """
    for p in reversed(package_list):
        package_dirs = set()
        root = os.path.join(*p.split("."))
        for sub_root, dir_list, _ in os.walk(root):
            for d in dir_list:
                if any(map(lambda exclude: fnmatch.fnmatch(d, exclude), exclude_dirs)):
                    continue
                relative_path = sub_root[len(root) + 1:]
                match = os.path.join(relative_path, d, "*")
                package_dirs.add(match)
        for previously_declared_d in package_data.get(p, []):
            package_dirs.add(previously_declared_d)
        package_data[p] = list(package_dirs)
