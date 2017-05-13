import json
import os
import pwd
import socket
import socketserver
import struct
import sys

try:
    import requests
except ImportError:
    print("Error: Howler-monkey requires python-requests to be installed.")
    sys.exit(0)

try:
    import yaml
except ImportError:
    print("Error: Howler-monkey requires PyYAML to be installed.")
    sys.exit(0)


DEFAULT_CONF = "/etc/howler.yml"
DEFAULT_SOCK = "/tmp/howler"


def get_credentials(sock):
    credentials = sock.getsockopt(socket.SOL_SOCKET,
                                  socket.SO_PEERCRED,
                                  struct.calcsize(str('3i')))
    return struct.unpack('3i', credentials)


class HowlerHandler(socketserver.BaseRequestHandler):
    slack_url = None

    @classmethod
    def set_slack_url(cls, url):
        cls.slack_url = url

    def setup(self):
        self.file = self.request.makefile('rw', encoding="UTF-8")

    def handle(self):
        payload = json.load(self.file)

        pid, uid, gid = get_credentials(self.request)

        user = pwd.getpwuid(uid)[0]  # passwd[0] = Login Name

        if 'username' in payload:
            payload['username'] = "{}[{}]".format(payload['username'], user)
        else:
            payload['username'] = "Howler Monkey[{}]".format(user)

        req = requests.post(self.slack_url, json=payload)
        if req.status_code == 200:
            rsp = {'success': True}
        else:
            rsp = {'success': False, 'error': req.text}
        json.dump(rsp, self.file)

    def finish(self):
        self.file.close()


def main(conf_loc):
    with open(conf_loc, "r") as conf_file:
        conf = yaml.safe_load(conf_file)

    if 'socket' in conf:
        sock = conf['socket']
    else:
        sock = DEFAULT_SOCK

    if 'slack' in conf:
        HowlerHandler.set_slack_url(conf['slack'])
    else:
        print("Error: Missing slack-url from config.")
        sys.exit(0)

    try:
        serv = socketserver.UnixStreamServer(sock, HowlerHandler)
        serv.serve_forever()
    except KeyboardInterrupt:
        os.unlink(sock)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            print("USAGE: {} [CONF-FILE]".format(sys.argv[0]))
        conf_loc = sys.argv[1]
    else:
        conf_loc = DEFAULT_CONF
    main(conf_loc)
