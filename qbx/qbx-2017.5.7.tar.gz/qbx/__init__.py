from docopt import docopt as docoptinit
import requests
import socket

usage = """
Usage:
    run <method> [options]
    
Options:
    --name=<name>
    --uris=<uris>
    --port=<port>
"""


def run(argv):
    print('args--{}--'.format(argv))
    argv = argv.split(' ')
    docopt = docoptinit(usage, argv)
    name = docopt['--name']
    uris = docopt['--uris']
    port = docopt['--port']
    url = 'http://kong-admin.qbtrade.org/apis'
    my_pod_id = socket.gethostbyname(socket.gethostname())
    requests.delete(uris + '/' + name)
    data = {'name': name,
            'uris': '/' + name,
            'upstream_url': 'http://{}:{}'.format(my_pod_id, port),
            'strip_uri': 'true'
            }
    requests.post(url, data=data)
