from wsgiprox.wsgiprox import WSGIProxMiddleware
from wsgiprox.resolvers import FixedResolver
import time


# ============================================================================
class TestUWSGI(object):
    def __call__(self, env, start_response):
        status = '200 OK'

        if env.get('HTTP_SEC_WEBSOCKET_KEY'):
            import uwsgi
            print(env)
            uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'],
                                      env.get('HTTP_ORIGIN', ''))

            buff = ''
            while True:
                try:
                    buff = uwsgi.websocket_recv()
                    print('RECV', buff)
                except Exception as e:
                    print(e)
                    return []

                msg = 'WS Request Url: ' + env.get('REQUEST_URI', '')
                msg += ' Echo: ' + buff.decode('utf-8')
                uwsgi.websocket_send(msg.encode('utf-8'))

        result = 'Requested Url: ' + env.get('REQUEST_URI', '')
        if env['REQUEST_METHOD'] == 'POST':
            result += ' Post Data: ' + env['wsgi.input'].read(int(env['CONTENT_LENGTH'])).decode('utf-8')

        result = result.encode('iso-8859-1')
        headers = [('Content-Length', str(len(result)))]

        start_response(status, headers)
        return [result]


application = WSGIProxMiddleware(TestUWSGI(), FixedResolver('/prefix/'), proxy_options={'enable_websockets': False})


def run_test_http():
    print('Running HTTP Test')

    import websocket
    ws = websocket.WebSocket()
    ws.connect('ws://example.com/websocket',
               http_proxy_host='localhost',
               http_proxy_port=8124)

    ws.send('plain message')
    msg = ws.recv()
    print(msg)
    assert(msg == 'WS Request Url: /prefix/http://example.com/websocket Echo: plain message')

def run_test_https():
    print('Running HTTPS Test')

    import websocket
    ws = websocket.WebSocket(sslopt={'ca_certs': './ca/wsgiprox-ca.pem'})
    ws.connect('wss://localhost:8124/websocket',
                http_proxy_host='localhost',
                http_proxy_port=8124)

    ws.send('ssl message')
    msg = ws.recv()
    print(msg)



if __name__ == "__main__":
#    run_test_http()
    run_test_https()

