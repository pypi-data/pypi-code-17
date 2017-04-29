

# ============================================================================
class TestWSGI(object):
    def __call__(self, env, start_response):
        status = '200 OK'
        print(env)

        ws = env.get('wsgi.websocket')

        if ws:
            msg = 'WS Request Url: ' + env.get('REQUEST_URI', '')
            msg += ' Echo: ' + ws.receive()
            ws.send(msg)
            return []

        result = 'Requested Url: ' + env.get('REQUEST_URI', '')
        if env['REQUEST_METHOD'] == 'POST':
            result += ' Post Data: ' + env['wsgi.input'].read(int(env['CONTENT_LENGTH'])).decode('utf-8')

        result = result.encode('iso-8859-1')
        headers = [('Content-Length', str(len(result)))]

        start_response(status, headers)
        return [result]


