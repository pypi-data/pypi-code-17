# -*- coding: utf-8 -*-
"""
    This module provides the local data providers.
    It can be used from both templates and controllers to
    for data fetching.
"""
from __future__ import print_function
from future.moves.urllib.parse import urlparse, urlencode
from os.path import abspath, splitext, isfile, join, dirname
import cherrypy
import sys
import yaml
import json

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

this.data_path = None

def get(provider_url):
    """ Return an iterable object with data contents.
    """
    parsed_url = urlparse(provider_url)
    print(parsed_url)
    if parsed_url.scheme != '':  # Schemes are note supported at this time
        return
    if parsed_url.path.startswith('/'):  # Absolute paths are not allowed
        return 
    resource_path = abspath(join(this.data_path, parsed_url.path))
    filename, file_extension = splitext(resource_path)
    if file_extension is '':    # Attempt with all supported file type extentions
        search_path = []
        for extension in ['.yaml', '.json']:
            search_path.append(resource_path + extension)
    else:
        search_path = [resource_path]


    found_resource_path = None
    for path in search_path:
        print(path)
        if isfile(path):
            found_resource_path = path
            break

    if found_resource_path is None:
        raise cherrypy.HTTPError(404, "Unable to find data for provider \'%s\'" % provider_url)
    filename, file_extension = splitext(found_resource_path)

    with open(found_resource_path) as data_file:
        if file_extension == '.yaml':
            data = [x for x in yaml.load_all(data_file)]
        if file_extension == '.json':
            data = json.load(data_file)
    return data

def set_directory(data_path):
    this.data_path = data_path
