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


def run():
    docopt = docoptinit(usage)
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
