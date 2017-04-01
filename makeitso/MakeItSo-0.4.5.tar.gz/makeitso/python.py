#!/usr/bin/env python

"""
python package templates for makeitso

Several components are included.
[TODO] You may use these subtemplates in any combination.

* README.txt : a README in restructured text
* examples : examples for your package
* setup.py : setup utility for the full package
* ./main.py : CLI handler for your webapp
* ./model.py : model of a persisted object
* ./template.py : a MakeItSo template for project creation
* ./tests : doctest suite for the package
* ./web.py : a webob web handler
"""

# TODO: console_scripts for all of these

import os
import shutil
import string
import sys
from cli import MakeItSoCLI
from makeitso import ContentTemplate
from optparse import OptionParser
from template import MakeItSoTemplate
from template import Variable


class SetupPy(MakeItSoTemplate):
    """template for setup.py"""
    templates = [('python_package', 'setup.py')]


class Unittest(MakeItSoTemplate):
    """template for python unittest"""
    templates = [('python_package', 'tests', 'test_{{package}}.py')]
    def pre(self, variables, output):
        if output and 'package' not in variables:
            package = os.path.splitext(os.path.basename(output.rstrip(os.path.sep)))[0]
            indicator = 'test_'
            if package.startswith(indicator):
                package = package[len(indicator):]
            variables['package'] = package


class PythonTemplate(MakeItSoTemplate):
    """abstract base class for python-type templates"""
    vars = [Variable('description'),
            Variable('author', 'author of the package'),
            Variable('email', "author's email"),
            Variable('url', 'project url'),
            Variable('repo', 'project repository'),
        ]

    def output2name(self, path):
        return os.path.splitext(os.path.basename(path.rstrip(os.path.sep)))[0]


class PythonScriptTemplate(PythonTemplate):
    """template for a single python script"""
    templates = [('python_package', '{{package}}', '{{main}}.py')]
    vars = [Variable('description')]


class PythonModuleTemplate(PythonTemplate):
    """single module python package"""

    templates = ['python_module',
                 ('python_package', '{{package}}', '{{main}}.py')]
    vars = [Variable('description')]
    look = False

    def pre(self, variables, output):
        variables['project'] = variables['module'] = variables['main'] = self.output2name(output)

    def post(self, variables, output):
        shutil.move(os.path.join(output, '{{main}}.py'),
                    os.path.join(output, '{}.py'.format(variables['main'])))


class PythonPackageTemplate(PythonTemplate):
    """
    python package template
    """
    # TODO: get the templates you actually care about [maybe from the CLI?]

    name = 'python-package'
    templates = ['python_package']
    vars = [Variable('description'),
            Variable('author', 'author of the package'),
            Variable('email', "author's email"),
            Variable('url', 'project url'),
            Variable('repo', 'project repository'),
        ]
    look = False

    # things that go in setup.py
    dependencies = {'web.py': ['webob'],
                    'template.py': ['MakeItSo']}
    console_scripts = {'main.py': '{{project}} = {{package}}.{{main}}:main',
                       'template.py': '{{package}}-template = {{package}}.template:main'
                   }

    def pre(self, variables, output):
        """
        sanitize some variables
        """

        # get project from output directory
        variables['project'] = self.output2name(output)

        # get package name from project
        allowable = set(string.letters + string.digits + '_')
        package = variables['project'].lower()
        package = ''.join([c for c in package
                           if c in allowable])
        # TODO better: translation matrix
        variables['package'] = package

        # name of CLI main file
        variables['main'] = 'main'

        # package dependencies
        dependencies = set([])
        for template, dependency in self.dependencies.items():
            dependencies.update(dependency)
        variables['dependencies'] = list(dependencies)

        # console_scripts
        console_scripts = []
        for template, console_script in self.console_scripts.items():
            console_scripts.append(console_script)
        if console_scripts:
            s = 'setup(' # placeholder string
            script_strings = ['[console_scripts]']
            for console_script in console_scripts:
                template = ContentTemplate(console_script)
                output = template.substitute(project=variables['project'],
                                             package=variables['package'],
                                             main=variables['main'])
                script_strings.append(output)
            variables['console_scripts'] = '\n'.join([' ' * len(s) + i
                                                    for i in script_strings])
        else:
            variables['console_scripts'] = ''


class PythonPackageCLI(MakeItSoCLI):
    """
    CLI front end for the python package template
    """
    usage = '%prog [options] project'


def main(args=sys.argv[1:]):
    """CLI"""
    cli = PythonPackageCLI(PythonPackageTemplate)
    cli(*args)


if __name__ == '__main__':
    main()
