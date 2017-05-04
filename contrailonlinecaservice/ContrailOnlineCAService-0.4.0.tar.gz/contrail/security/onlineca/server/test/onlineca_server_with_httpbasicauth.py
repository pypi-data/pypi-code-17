#!/usr/bin/env python
"""Test script to run Online CA service with HTTP Basic Auth in the Paster web
application server.
"""
__author__ = "P J Kershaw"
__date__ = "03/08/12"
__copyright__ = "(C) 2012 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
logging.basicConfig(level=logging.DEBUG)
from os import path

THIS_DIR = path.abspath(path.dirname(__file__))
INI_FILENAME = 'onlineca-server-with-httpbasicauth.ini'
ini_filepath = path.join(THIS_DIR, INI_FILENAME)

try:
    from waitress import serve
    from paste.deploy import loadapp

    app = loadapp('config:{}'.format(INI_FILENAME), relative_to=THIS_DIR)
    serve(app, host='0.0.0.0', port=10443)

except ImportError as e:
    from warnings import warn
    warn("Defaulting to use Paste, waitress not available.  "
         "Error is: {}".format(e))

    from paste.script.serve import ServeCommand

    # def application(environ, start_response):
    #     environ['HTTP_AUTHORIZATION'] = 'True'
    ServeCommand("serve").run([ini_filepath])
