# -*- coding: utf-8 -*-
import json
import os
import re
import base64
import hashlib

import pipfile
import toml

import delegator
from requests.compat import OrderedDict

from .utils import (format_toml, mkdir_p, convert_deps_from_pip,
    proper_case, pep426_name, is_vcs, recase_file)
from .environments import PIPENV_MAX_DEPTH, PIPENV_VENV_IN_PROJECT


class Project(object):
    """docstring for Project"""
    def __init__(self):
        super(Project, self).__init__()
        self._name = None
        self._virtualenv_location = None
        self._download_location = None
        self._proper_names_location = None
        self._pipfile_location = None

    @property
    def name(self):
        if self._name is None:
            self._name = self.pipfile_location.split(os.sep)[-2]
        return self._name

    @property
    def pipfile_exists(self):
        return bool(self.pipfile_location)

    @property
    def virtualenv_exists(self):
        # TODO: Decouple project from existence of Pipfile.
        if self.pipfile_exists:
            return os.path.isdir(self.virtualenv_location)
        return False

    @property
    def virtualenv_name(self):
        # Replace dangerous characters into '_'. The length of the sanitized
        # project name is limited as 42 because of the limit of linux kernel
        #
        # 42 = 127 - len('/home//.local/share/virtualenvs//bin/python2') - 32 - len('-HASHHASH')
        #
        #      127 : BINPRM_BUF_SIZE - 1
        #       32 : Maxmimum length of username
        #
        # References:
        #   https://www.gnu.org/software/bash/manual/html_node/Double-Quotes.html
        #   http://www.tldp.org/LDP/abs/html/special-chars.html#FIELDREF
        #   https://github.com/torvalds/linux/blob/2bfe01ef/include/uapi/linux/binfmts.h#L18
        sanitized = re.sub(r'[ $`!*@"\\\r\n\t]', '_', self.name)[0:42]

        # Hash the full path of the pipfile
        hash = hashlib.sha256(self.pipfile_location.encode()).digest()[:6]
        encoded_hash = base64.urlsafe_b64encode(hash).decode()

        # If the pipfile was located at '/home/user/MY_PROJECT/Pipfile',
        # the name of its virtualenv will be 'my-project-wyUfYPqE'
        return sanitized + '-' + encoded_hash

    @property
    def virtualenv_location(self):

        # Use cached version, if available.
        if self._virtualenv_location:
            return self._virtualenv_location

        # The user wants the virtualenv in the project.
        if not PIPENV_VENV_IN_PROJECT:
            c = delegator.run('pew dir "{0}"'.format(self.virtualenv_name))
            loc = c.out.strip()
        # Default mode.
        else:
            loc = os.sep.join(self.pipfile_location.split(os.sep)[:-1] + ['.venv'])

        self._virtualenv_location = loc
        return loc

    @property
    def download_location(self):
        if self._download_location is None:
            loc = os.sep.join([self.virtualenv_location, 'downloads'])
            self._download_location = loc

        # Create the directory, if it doesn't exist.
        mkdir_p(self._download_location)

        return self._download_location

    @property
    def proper_names_location(self):
        if self._proper_names_location is None:
            loc = os.sep.join([self.virtualenv_location, 'pipenev-proper-names.txt'])
            self._proper_names_location = loc

        # Create the database, if it doesn't exist.
        open(self._proper_names_location, 'a').close()

        return self._proper_names_location

    @property
    def proper_names(self):
        with open(self.proper_names_location) as f:
            return f.read().splitlines()

    def register_proper_name(self, name):
        """Registers a proper name to the database."""
        with open(self.proper_names_location, 'a') as f:
            f.write('{0}\n'.format(name))

    @property
    def pipfile_location(self):
        if self._pipfile_location is None:
            try:
                loc = pipfile.Pipfile.find(max_depth=PIPENV_MAX_DEPTH)
            except RuntimeError:
                loc = None
            self._pipfile_location = loc

        return self._pipfile_location

    @property
    def parsed_pipfile(self):
        with open(self.pipfile_location) as f:
            return toml.load(f, _dict=OrderedDict)

    @property
    def _pipfile(self):
        """Pipfile divided by PyPI and external dependencies."""
        pfile = self.parsed_pipfile
        for section in ('packages', 'dev-packages'):
            p_section = pfile.get(section, {})

            for key in list(p_section.keys()):
                # Normalize key name to pep426.
                norm_key = pep426_name(key)
                p_section[norm_key] = p_section.pop(key)

        return pfile

    @property
    def _lockfile(self):
        """Pipfile.lock divided by PyPI and external dependencies."""
        pfile = pipfile.load(self.pipfile_location)
        lockfile = json.loads(pfile.lock())

        for section in ('default', 'develop'):
            lock_section = lockfile.get(section, {})

            for key in list(lock_section.keys()):
                norm_key = pep426_name(key)
                lockfile[section][norm_key] = lock_section.pop(key)

        return lockfile

    @property
    def lockfile_location(self):
        return '{0}.lock'.format(self.pipfile_location)

    @property
    def lockfile_exists(self):
        return os.path.isfile(self.lockfile_location)

    @property
    def lockfile_content(self):
        with open(self.lockfile_location) as lock:
            return json.load(lock)

    def create_pipfile(self):
        data = {u'source': [{u'url': u'https://pypi.python.org/simple', u'verify_ssl': True}], u'packages': {}, 'dev-packages': {}}
        self.write_toml(data, 'Pipfile')

    def write_toml(self, data, path=None):
        if path is None:
            path = self.pipfile_location

        formatted_data = format_toml(toml.dumps(data))
        with open(path, 'w') as f:
            f.write(formatted_data)

    @property
    def sources(self):
        if self.lockfile_exists:
            meta_ = self.lockfile_content['_meta']
            sources_ = meta_.get('sources')
            if sources_:
                return sources_
        if 'source' in self.parsed_pipfile:
            return self.parsed_pipfile['source']
        else:
            return [{u'url': u'https://pypi.python.org/simple', u'verify_ssl': True}]

    def remove_package_from_pipfile(self, package_name, dev=False):

        # Read and append Pipfile.
        p = self._pipfile

        package_name = pep426_name(package_name)

        key = 'dev-packages' if dev else 'packages'

        if key in p and package_name in p[key]:
            del p[key][package_name]

        # Write Pipfile.
        self.write_toml(recase_file(p))

    def add_package_to_pipfile(self, package_name, dev=False):

        # Read and append Pipfile.
        p = self._pipfile

        key = 'dev-packages' if dev else 'packages'

        # Set empty group if it doesn't exist yet.
        if key not in p:
            p[key] = {}

        package = convert_deps_from_pip(package_name)
        package_name = [k for k in package.keys()][0]

        # Add the package to the group.
        p[key][package_name] = package[package_name]

        # Write Pipfile.
        self.write_toml(recase_file(p))
