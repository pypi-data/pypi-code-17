import pickle, requests, threading

try:
  import http.server as http_server
except ImportError:
  import BaseHTTPServer as http_server

try:
  import socketserver
except ImportError:
  import SocketServer as socketserver



__version__ = '0.2.1'
DEFAULT_HOST, DEFAULT_PORT = 'localhost', 4518
socketserver.TCPServer.allow_reuse_address = True


class DSPRPCServer(object):
  def __init__(self, target, host=DEFAULT_HOST, port=DEFAULT_PORT):
    self.target = target
    class Handler(http_server.BaseHTTPRequestHandler):
      def do_RPC(s):
        content_length = int(s.headers['Content-Length'])
        attr = s.path.lstrip('/')
        if attr.endswith('()'):
          is_func = True
          attr = attr[:-2]
        else:
          is_func = False
        args, kwargs = pickle.loads(s.rfile.read(content_length)) if content_length else ((),{})
        try:
          ret = getattr(target, attr)
          if is_func:
            ret = ret(*args, **kwargs)
          if not is_func and callable(ret):
            s.send_response(202)
            s.end_headers()
          else:
            s.send_response(200)
            s.end_headers()
            s.wfile.write(pickle.dumps(ret, protocol=-1))
        except Exception as e:
          s.send_response(420)
          s.end_headers()
          s.wfile.write(pickle.dumps(e, protocol=-1))
    self.httpd = socketserver.ThreadingTCPServer(("localhost", port), Handler)
    t = threading.Thread(target=self.httpd.serve_forever)
    t.daemon = True
    t.start()
  
  def shutdown(self):
    self.httpd.shutdown()
    

class DSPRPCClient(object):
  def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
    self.port = port
  
  def __getattr__(self, attr):
    resp = requests.request('RPC', 'http://localhost:%i/%s' % (self.port, attr))
    if resp.status_code==200:
      return pickle.loads(resp.content)
    elif resp.status_code==420:
      raise pickle.loads(resp.content)
    elif resp.status_code==202:
      def f(*args, **kwargs):
        data = None
        if args or kwargs:
          data = pickle.dumps((args, kwargs), protocol=-1)
        resp = requests.request('RPC', 'http://localhost:%i/%s()' % (self.port, attr), data=data)
        if resp.status_code==200:
          return pickle.loads(resp.content)
        elif resp.status_code==420:
          raise pickle.loads(resp.content)
        else:
          raise Exception('got an unknown connection error - status code: %i' % resp.status_code)
      return f
    else:
      raise Exception('got an unknown connection error - status code: %i' % resp.status_code)
    
  

