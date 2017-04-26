# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
<aljosha.friemann@gmail.com> wrote this file.  As long as you retain this
notice you can do whatever you want with this stuff. If we meet some day,
and you think this stuff is worth it, you can buy me a beer in return.
----------------------------------------------------------------------------

"""

import logging, json, subprocess, os, ruamel.yaml as yaml, copy, re

from simple_model import Model, Attribute

class Source(Model):
    url = Attribute(str)
    user = Attribute(str, optional=True)
    password = Attribute(str, optional=True)
    branch = Attribute(str, optional=True)

class Script(Model):
    path   = Attribute(str)
    source = Attribute(str, optional=True)
    command = Attribute(str, optional=True)

def parse_entries(t):
    def parse(d):
        result = {}
        for name, values in d.items():
            result.update({ name: t(**values) })
        return result

    return parse

class Config(Model):
    path       = Attribute(str)
    script_dir = Attribute(str)
    scripts    = Attribute(parse_entries(Script), fallback=[])
    sources    = Attribute(parse_entries(Source), fallback=[])

def parse_config(path, defaults):
    data = copy.deepcopy(defaults)
    data.update({'path': path})

    with open(path, 'r') as stream:
        data.update(yaml.safe_load(stream))

    return Config(**data)

def pretty_print(config):
    def represent_model(t):
        def represent_subclass(dumper, data):
            return dumper.represent_mapping(data.__class__.__name__, dict(data))
        return represent_subclass

    yaml.add_representer(Source, represent_model(Source))
    yaml.add_representer(Script, represent_model(Script))

    # ugly..
    dump = yaml.dump(dict(config), indent=2, default_flow_style=False)
    dump = re.sub(r'!<.*>', '', dump)
    dump = re.sub(r'.*: null\n', '', dump)

    print(dump.strip())

def edit(config):
    editor = os.environ.get('EDITOR')

    if editor is None:
        raise RuntimeError('Environment variable EDITOR is not set.')

    return subprocess.call([editor, config.path])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
