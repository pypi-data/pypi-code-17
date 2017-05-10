import logging
import os
import tempfile

from docopt import docopt as docoptinit
import requests
import socket
import sys

register_kong_doc = """
Usage:
    register_kong [options]
    
Options:
    --name=<name>
    --uris=<uris>
    --port=<port>
"""


def register_kong(argv):
    docopt = docoptinit(register_kong_doc, argv)
    print(docopt)
    name = docopt['--name']
    uris = docopt['--uris']
    port = docopt['--port']
    url = 'http://kong-admin.qbtrade.org/apis'
    ip = socket.gethostbyname(socket.gethostname())
    requests.delete(url + name)
    data = {'name': name,
            'uris': '/' + uris,
            'upstream_url': 'http://{}:{}'.format(ip, port),
            'strip_uri': 'true'
            }
    requests.post(url, data=data)
    print('redister ip', ip)


watch_git_doc = """
Usage:
    watch_git.py [options] <repo> <path>
    
Options:
    --debug

"""


def watch_git(argv):
    docopt = docoptinit(watch_git_doc, argv)
    directory = tempfile.mkdtemp()
    print('watch', directory, docopt)
    os.system('cd {} && git clone {} watch'.format(directory, docopt['<repo>']))
    path = '{}/watch/{}'.format(directory, docopt['<path>'])
    with open('{}/watch/{}'.format(directory, docopt['<path>'])) as f:
        buf = f.read()
    while True:
        import time
        time.sleep(10)
        os.system('cd {}/watch && git pull'.format(directory))
        with open(path) as f:
            new = f.read()
        if new != buf:
            logging.warning('changed')
            break


def run():
    print('argv---', sys.argv)
    if sys.argv[1] == 'register_kong':
        register_kong(sys.argv[1:])
    if sys.argv[1] == 'watch_git':
        watch_git(sys.argv[2:])


if __name__ == '__main__':
    watch_git(['git+ssh://git@github.com/qbtrade/quantlib.git', 'log_rpc.py'])
