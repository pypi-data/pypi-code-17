"""
"""
import os
import sys
import socket
import cherrypy
from os.path import join, exists, dirname, abspath
from quickweb import startup, controller
from pprint import pprint


def run(app_directory=None):
    """
    When an application is run, the following is performed:

    - Identify application root
        - Check for qwstart.py on
            - Startup script directory
            - Current working directory

    - Setup port number, if $PORT is not set, use a random port
    """

    # Check if beeing run from gunicorn
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
    if is_gunicorn:
        sys.stderr.write("Quickweb provides it's own HTTP server module.\n"\
            "Running from another HTTP server is not supported at this time\n")
        sys.exit(1)


    # Identify the application root directory
    startup_script_dir = dirname(sys.argv[0])
    app_root_directory = app_directory
    if app_root_directory is None:
        possible_entries = (startup_script_dir, os.getcwd())
        for check_directory in possible_entries:
            startup_script = join(abspath(check_directory), 'qwstart.py')
            if exists(startup_script):
                app_root_directory = abspath(check_directory)
                break
        if app_root_directory is None:
            sys.stderr.write('Unable to find qwstart.py!\n')
            sys.exit(2)

    startup.init_app('app_name', app_root_directory)

    # Determine the HTTP listener port
    listener_port = int(os.getenv('PORT', 0))
    if listener_port == 0:  # Get a random port
        print('Using a random port')
        test_socket = socket.socket()
        test_socket.bind(('', 0))
        listener_port = test_socket.getsockname()[1]
        test_socket.close()

    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': listener_port})
    cherrypy.engine.start()
    cherrypy.engine.block()
