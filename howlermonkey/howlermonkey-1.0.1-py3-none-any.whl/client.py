import json
import socket


DEFAULT_SOCKET = "/tmp/howler"


class HowlerMonkeyException(Exception):
    def __init__(self, message):
        self.message = message


class Client(object):
    def __init__(self,
                 srv=DEFAULT_SOCKET,
                 username=None,
                 channel=None,
                 icon_url=None,
                 icon_emoji=None):
        self.args = {'srv': srv,
                     'username': username,
                     'channel': channel,
                     'icon_url': icon_url,
                     'icon_emoji': icon_emoji}

    def send(self, txt):
        send(txt, **self.args)


def send(txt,
         srv=DEFAULT_SOCKET,
         username=None,
         channel=None,
         icon_url=None,
         icon_emoji=None):
    payload = {'text': txt,
               'username': username,
               'channel': channel,
               'icon_url': icon_url,
               'icon_emoji': icon_emoji}

    # Prune all the null entries
    payload = {k: v for k, v in payload.items() if v is not None}

    with socket.socket(socket.AF_UNIX) as sock:
        sock.connect(srv)
        with sock.makefile("rw", encoding="UTF-8") as file:
            json.dump(payload, file)
            file.flush()
            sock.shutdown(socket.SHUT_WR)
            rsp = json.load(file)
    if not rsp['success']:
        raise HowlerMonkeyException(rsp['error'])
