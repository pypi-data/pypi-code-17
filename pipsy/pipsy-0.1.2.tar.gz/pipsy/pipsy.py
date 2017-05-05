import collections
import sys
import pip
import json
import changelogs
import urllib.request
from packaging import version
from urllib.error import HTTPError, URLError
from distutils.version import LooseVersion


SECURITY_NOTICE_KEYWORDS = [
    'security', 'vulnerability', 'cve', 'xss', 'sql injection',
]

DISPLAY_TABLE_LABELS = {
    'status': 'Status',
    'package': 'Package',
    'installed': 'Installed',
    'latest': 'Latest',
    'versions': 'Available Updates',
    'notices': 'Security Notices',
}


class PackageVersion(LooseVersion):
    def _cmp(self, other):
        try:
            v1 = version.parse(self.vstring)
            v2 = version.parse(str(other))
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
            else:
                return 0
        except:
            return super(PackageVersion, self)._cmp(other)


def get_pkg_info(package):
    f = urllib.request.urlopen(
        'https://pypi.python.org/pypi/%s/json' % package)
    return json.loads(f.readall().decode('utf-8'))


def get_versions(package):
    return [(version, package) for version, package in sorted(
        package['releases'].items(), key=lambda k: PackageVersion(k[0]), reverse=True)]


def get_version_range(package, installed_version):
    compare_version = LooseVersion(installed_version)
    return [(version, package) for version, package in get_versions(package)
            if PackageVersion(version) > compare_version]


def get_latest_version(package):
    versions = get_versions(package)
    return versions[0][0] if len(versions) else None


def get_version_diff(package, version_range):
    logs = get_changelogs(package.project_name)
    versions = []
    for version, version_package in version_range:
        for release_version, changelog in logs:
            if release_version == version and PackageVersion(package.version) < PackageVersion(version):
                versions.append((version, changelog))
    return versions if len(versions) else []


def get_pkg_security_releases(version_diff):
    versions = []
    for version, changelog in version_diff:
        if _string_contains_security_keywords(changelog):
            versions.append((version, changelog))
    return versions if len(versions) else None


def get_changelogs(package_name):
    versions = changelogs.get(package_name, vendor='pypi')
    ret = [(v, versions[v])
           for v in sorted(versions.keys(), key=PackageVersion, reverse=True)]
    return ret


def get_updates(package, changelog_scan=True):
    ret = {
        'package': package.project_name,
        'installed': package.version,
        'latest': None,
    }
    try:
        pkg = get_pkg_info(package.project_name)
        latest = get_latest_version(pkg)
        if latest:
            ret['latest'] = latest
            if latest > package.version:

                version_range = get_version_range(pkg, package.version)
                for version, version_info in version_range:
                    ret['versions'] = ', '.join(
                        [version for version, version_info in version_range])

                if changelog_scan:
                    ret['changelogs'] = {}
                    version_diff = get_version_diff(package, version_range)
                    for diff_version, diff_changelog in version_diff:
                        ret['changelogs'][diff_version] = [line.strip() for line in diff_changelog.strip(
                        ).split("\n") if len(line.replace('-', '').strip()) > 0]

                    sec_releases = get_pkg_security_releases(version_diff)
                    if sec_releases is not None:
                        ret['notices'] = ', '.join(
                            ['<%s' % sec_version for sec_version, sec_changelog in sec_releases])
    except (HTTPError, URLError) as e:
        ret['error'] = str(e)
    return ret


def show_updates(changelog_scan=True, all_packages=False, json_out=False, filter_packages=[]):
    packages = sorted(pip.get_installed_distributions(),
                      key=lambda pkg: pkg.project_name.lower())

    packages_total = len(packages)
    if filter_packages:
        packages = filter(
            lambda pkg: pkg.project_name in filter_packages, packages)
        packages_total = len(filter_packages)
    packages_progress = 0

    updates = []

    if not json_out:
        _display_progress(packages_total)

    for p in packages:
        updates.append(get_updates(p, changelog_scan=changelog_scan))
        packages_progress += 1
        if not json_out:
            _display_progress(packages_total, packages_progress)

    if json_out:
        sys.stdout.write(json.dumps(updates, indent=4))
    else:
        _display_table(updates, show_notices=changelog_scan, show_all_packages=all_packages)


def _string_contains_security_keywords(string):
    lower = string.lower()
    for keyword in SECURITY_NOTICE_KEYWORDS:
        if keyword in lower:
            return True
    return False


def _get_column_lengths(rows, labels):
    lens = {k: len(labels[k]) for k in labels.keys()}
    for r in range(0, len(rows)):
        for k, v in rows[r].items():
            if k in labels.keys():
                l = len(str(v))
                if l > lens[k]:
                    lens[k] = l
    return lens


def _display_table(rows, show_notices=False, show_all_packages=False):
    lens = _get_column_lengths(rows, DISPLAY_TABLE_LABELS)

    columns = ['package', 'installed', 'latest', 'versions', ]
    if show_notices:
        columns.append('notices')

    row_format = " | ".join(["{:<%s}" % lens[column]
                             for column in columns]) + "\n"
    labels = row_format.format(
        *(DISPLAY_TABLE_LABELS[column] for column in columns))

    sys.stdout.write("-" * len(labels) + "\n")
    sys.stdout.write(labels)
    sys.stdout.write("-" * len(labels) + "\n")

    for row in rows:
        row['versions'] = row['versions'] if 'versions' in row else ''
        row['notices'] = row['notices'] if 'notices' in row else ''
        row['latest'] = row['latest'] if 'latest' in row and row['latest'] is not None else 'unknown'
        if show_all_packages or len(row['versions']) > 0:
            sys.stdout.write(row_format.format(
                *(row[column] for column in columns)))
    sys.stdout.write('\n')


def _display_progress(total, i=0):
    percent = ("{0:.1f}").format(100 * (i / float(total)))
    sys.stdout.write('\rFetching package information... %s%%\r' % percent)
    if i < total:
        sys.stdout.write('\rFetching package information... %s%%' % percent)
    else:
        sys.stdout.write('\r%s\r' % (' ' * 100))
