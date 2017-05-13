import json
import socket


DEFAULT_SOCKET = "/tmp/howler"


class HowlerMonkeyException(Exception):
    def __init__(self, message):
        self.message = message


def send(text,
         srv=DEFAULT_SOCKET,
         username=None,
         channel=None,
         icon_url=None,
         icon_emoji=None):
    # Gather all method arguments
    payload = locals()

    # Except srv, it should not be sent to the server
    del payload['srv']

    # Prune all the null entries
    payload = {k: v for k, v in payload.items() if v is not None}

    with socket.socket(socket.AF_UNIX) as sock:
        sock.connect(srv)
        with sock.makefile("rw", encoding="UTF-8") as file:
            json.dump(payload, file)
            file.flush()
            # Close the write side of the socket to
            # signal that we have ceased transmitting
            sock.shutdown(socket.SHUT_WR)
            rsp = json.load(file)

    if not rsp['success']:
        raise HowlerMonkeyException(rsp['error'])
