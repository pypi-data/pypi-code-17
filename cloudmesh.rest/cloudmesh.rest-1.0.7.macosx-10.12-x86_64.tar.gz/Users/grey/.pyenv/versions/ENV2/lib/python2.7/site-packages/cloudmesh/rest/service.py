#!/usr/bin/env python
"""
The EVE REST service management 
"""

import os
import sys
from pprint import pprint

from cloudmesh.common.console import Console
from eve import Eve


# for now load eve_settings from source


# EVE=cd $(ROOT_DIR); $(pyenv); python service.py

class RestService(object):
    """
    The REST service methods
    """

    def __init__(self, settings=None):
        self.name = "eve"
        self.settings = settings
        self.app = None
        # TODO: reads the OBJECT.settings.py file and sets up the eve service with it
        # config_dir = path_expand("~/.cloudmesh/db/")
        '''
        if settings is None:
            settings = path_expand("~/.cloudmesh/db/settings.py")

        else:

          config_dir = path_expand("~/.cloudmesh/db/")
          config_file = path_expand("~/.cloudmesh/db/settings.py")

          if filename is not in config
              cp filename config
          path, filename = use basedir to separate path and filename
          
          if filename ends in ".json":
             r = Shell.execute("evegenie",config_dir + filename)
             # make sure evegenie creates the settings.py in the same dir, 
             # if not we need to do this differently or change evegenie
          # we assume that we now have ~/.cloudmesh/db/settings.py
           
        '''
        # self.eve_settings = eve_settings
        # parameters = {
        #    "settings": config_dir
        # }

    def info(self):
        return self.parameters

    def run(self):
        """
        start the REST service
        :return: 
        """
        # TODO: implement

        Console.ok("loading eve_settings ...")

        sys.path.append('~/.cloudmesh/eve')
        from settings import eve_settings

        Console.ok("loaded.")
        pprint(eve_settings)

        app = Eve(settings=eve_settings)
        app.run()

    def start(self):
        os.system("cms admin rest run &")

    def stop(self):
        """
        stop the rest service
        :return: 
        """
        # TODO: implement
        print("NOT YET IMPLEMENTED")

    def status(self):
        """
        return the status of the rest service
        :return: 
        """
        # TODO: implement
        print("NOT YET IMPLEMENTED")

    def reset(self, settings=None):
        """
        reset the restservice by deleting the database, initialising the settings.py and restart the service
        :param settings: 
        :return: 
        """
        # TODO: implement
        print("NOT YET IMPLEMENTED")
        # re-initializes eve with a new settings



def main():
    """
    TODO: a simple example, which should actully be in a nosetest
    :return: 
    """
    app = Eve(settings=eve_settings)
    app.run()


if __name__ == '__main__':
    main()
