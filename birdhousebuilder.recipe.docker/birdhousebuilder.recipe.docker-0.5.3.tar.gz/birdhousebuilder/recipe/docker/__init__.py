# -*- coding: utf-8 -*-

"""Recipe docker"""

import os
import shutil
from mako.template import Template

import logging
logger = logging.getLogger(__name__)

file_dockerignore = os.path.join(os.path.dirname(__file__), "dot_dockerignore")
templ_dockerenv = Template(filename=os.path.join(os.path.dirname(__file__), "dot_env"))
templ_dockerfile = Template(filename=os.path.join(os.path.dirname(__file__), "Dockerfile"))


class Recipe(object):
    """Buildout recipe to generate a Dockerfile."""

    def __init__(self, buildout, name, options):
        self.buildout, self.options, self.name = buildout, options, name
        b_options = buildout['buildout']
        self.buildout_dir = b_options.get('directory')

        self.options['app'] = options.get('app', 'birdhouse')
        self.options['maintainer'] = options.get('maintainer', 'https://github.com/bird-house')
        self.options['description'] = options.get('description', self.options['app'] + ' application')
        self.options['vendor'] = options.get('vendor', 'Birdhouse')
        self.options['version'] = options.get('version', '1.0.0')
        self.options['hostname'] = options.get('hostname', 'localhost')
        self.options['supervisor_port'] = self.options['supervisor-port'] = options.get('supervisor-port', '9001')
        self.options['http_port'] = self.options['http-port'] = options.get('http-port', '8080')
        self.options['https_port'] = self.options['https-port'] = options.get('https-port', '8443')
        self.options['output_port'] = self.options['output-port'] = options.get('output-port', '8000')

    def install(self):
        installed = []
        installed += list(self.install_dockerignore())
        installed += list(self.install_dockerenv())
        installed += list(self.install_dockerfile())
        return installed

    def install_dockerignore(self):
        output = os.path.join(self.buildout_dir, '.dockerignore')
        shutil.copy2(file_dockerignore, output)
        return tuple()

    def install_dockerenv(self):
        result = templ_dockerenv.render(**self.options)
        output = os.path.join(self.buildout_dir, '.env')

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
            os.chmod(output, 0o644)
        return tuple()

    def install_dockerfile(self):
        result = templ_dockerfile.render(**self.options)
        output = os.path.join(self.buildout_dir, 'Dockerfile')

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
            os.chmod(output, 0o644)
        return tuple()

    update = install


def uninstall(name, options):
    pass
