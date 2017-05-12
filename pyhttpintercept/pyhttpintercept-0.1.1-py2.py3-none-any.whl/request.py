
from BaseHTTPServer import BaseHTTPRequestHandler
import logging_helper
from .methods.get import GetHandler
from .methods.post import PostHandler


logging = logging_helper.setup_logging()


class HTTPRequestHandler(BaseHTTPRequestHandler):

    BaseHTTPRequestHandler.protocol_version = u"HTTP/1.1"

    #  Override base class logging function
    def log_message(self,
                    fmt,
                    *args):
        logging.info(u"{addr} - {fmt}".format(addr=self.client_address[0],
                                              fmt=fmt % args))

    # Request handlers
    def do_GET(self):
        GetHandler(self,
                   scenarios=self.server.scenarios).handle()

    def do_POST(self):
        PostHandler(self,
                    scenarios=self.server.scenarios).handle()
