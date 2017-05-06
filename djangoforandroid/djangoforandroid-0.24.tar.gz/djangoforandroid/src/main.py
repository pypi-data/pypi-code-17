#Generated with django-for-android

""" Start Django in multithreaded mode

It allows for debugging Django while serving multiple requests at once in
multi-threaded mode.

"""

import sys
import os

if not '--nodebug' in sys.argv:


    paths = [
        '/storage/emulated/0',
        '/storage/emulated/legacy',
        '/sdcard',
        '.',
    ]

    APP_DIR = None
    for path in paths:
        if os.path.exists(path):
            APP_DIR = "{}/{}".format(path, 'Piton')
            break

    APP_DIR = os.path.abspath(APP_DIR)
    if APP_DIR:
        os.makedirs(APP_DIR, exist_ok=True)

    #log_path = "logs"
    log_path = APP_DIR

    if not os.path.exists(log_path):
        os.mkdir(log_path)

    print("Logs in {}".format(log_path))
    sys.stdout = open(os.path.join(log_path, "stdout.log"), "w")
    sys.stderr = open(os.path.join(log_path, "stderr.log"), "w")

print("Starting Django Server")
from wsgiref import simple_server
from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.join(os.path.dirname(__file__), "{{NAME}}"))

os.environ['LD_LIBRARY_PATH'] = ":".join(filter(None, [os.environ.get('LD_LIBRARY_PATH', ''),
                                                       '.',
                                                       '../lib'
                                                       ]))

#----------------------------------------------------------------------
def django_wsgi_application():
    """"""
    print("Creating WSGI application...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{NAME}}.settings")
    application = get_wsgi_application()
    return application


#----------------------------------------------------------------------
def main():
    """"""
    if {{APP_MULTITHREAD}}:
        import socketserver
        class ThreadedWSGIServer(socketserver.ThreadingMixIn, simple_server.WSGIServer):
            pass
        httpd = simple_server.make_server('{{IP}}' , {{PORT}}, django_wsgi_application(), server_class=ThreadedWSGIServer)
    else:
        httpd = simple_server.make_server('{{IP}}' , {{PORT}}, django_wsgi_application())

    httpd.serve_forever()
    print("Django for Android serving on {}:{}".format(*httpd.server_address))


main()
