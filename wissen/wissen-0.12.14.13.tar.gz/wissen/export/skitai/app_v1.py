# 2017. 3. 13 by Hans Roh (hansroh@gmail.com)

from skitai.saddle import Saddle
import skitai
import wissen
from wissen.lib import pathtool
import os
import json
import codecs

app = Saddle (__name__)
app.debug = True
app.use_reloader = True
app.config.numthreads = 1

def getdir (*d):
	return os.path.join (app.config.resource_dir, *d)

def is_json (request):
	return request.command == "post" and not request.get_header ('content-type', '').startswith ('application/x-www-form-urlencoded')
		
def load_data (alias, numthreads, plock):	
	with codecs.open (getdir ("config", alias), "r", "utf8") as f:
		colopt = json.loads (f.read ())			
		colopt ['data_dir'] = [getdir ('models', os.path.normpath(d)) for d in colopt ['data_dir']]
		
	if 'classifier' in colopt:
		analyzer = wissen.standard_analyzer (10000, numthreads, **colopt ["analyzer"])
		col = wissen.model (colopt ["data_dir"], wissen.READ, analyzer, plock = plock)	
		actor = col.get_classifier (**colopt.get ('classifier', {}))
	else:
		analyzer = wissen.standard_analyzer (8, numthreads, **colopt ["analyzer"])
		col = wissen.collection	(colopt ["data_dir"], wissen.READ, analyzer, plock = plock)	
		actor = col.get_searcher (**colopt.get ('searcher', {}))
	wissen.assign (alias, actor)
			
#-----------------------------------------------------------------

@app.startup
def startup (wasc):
	app.config.numthreads = len (wasc.threads)
	wissen.configure (app.config.numthreads, wasc.logger.get ("app"), 16384, 128)
	pathtool.mkdir (getdir ("config"))
		
	for alias in os.listdir (getdir ("config")):		
		load_data (alias, app.config.numthreads, wasc.plock)
  
@app.shutdown
def shutdown (wasc):	
	wissen.shutdown ()

#-----------------------------------------------------------------

@app.before_request
def before_request (was):
	if was.request.args.get ('alias') and not wissen.get (was.request.args ['alias']):
		return was.response ("404 Not Found")
	
#-----------------------------------------------------------------

@app.route ("/")
def index (was):
	return was.jstream ({'errmsg': 'OK', 'collections': list (wissen.status ().keys ())})

@app.route ("/<alias>", methods = ["GET", "POST", "PUT", "DELETE"])
def config (was, alias, config = None):
	fn = getdir ("config", alias)
	if was.request.command == "get":				
		status = wissen.status (alias)
		
		conf = getdir ("config", alias)
		with codecs.open (conf, "r", "utf8") as f:
			colopt = json.loads (f.read ())		
			status ['colopt'] = {
				'data': colopt,
				'mtime': 	os.path.getmtime (conf),
				'size': 	os.path.getsize (conf),
				'path': conf
			}
		status ['errmsg'] = "OK"	
		return was.jstream (status)
			
	if was.request.command == "delete":		
		wissen.drop (alias)
		os.remove (fn)		
		return was.jstream ({'errmsg': 'OK'})
	
	if was.request.command in ("post", "put"):
		if was.request.command == "post" and wissen.get (alias):
			return was.response ("406 Resource Exists")
			
		colopt = was.request.json()
		data_dir = []
		for d in colopt ['data_dir']:
			b = os.path.normpath (d)			
			t = os.sep + "resources" + os.sep + "models" + os.sep
			s = b.find (t)
			if s == -1:
				return was.response ("400 Bad Request")
			data_dir.append (b [s + len (t):])
		colopt ['data_dir']	= data_dir
		with codecs.open (fn, "w", "utf8") as f:
			f.write (json.dumps (colopt))

		if was.request.command == "post":
			load_data (alias, app.config.numthreads, was.plock)			
		else:	
			wissen.refresh (alias)
			
		return was.jstream ({'errmsg': 'OK', 'config': was.request.json ()})

#-----------------------------------------------------------------

@app.route ("/<alias>/locks", methods = ["GET"])
def locks (was, alias):	
	return was.jstream ({'errmsg': 'OK', "locks": wissen.get (alias).si.lock.locks ()})	

@app.route ("/<alias>/locks/<name>", methods = ["GET", "DELETE"])
def handle_lock (was, alias, name):	
	if was/request.command == "get":
		wissen.get (alias).si.lock.lock (name)		
		return was.jstream ({'errmsg': 'OK', "lock": name})
	wissen.get (alias).si.lock.unlock (name)		
	return was.jstream ({'errmsg': 'OK', "unlock": name})

#-----------------------------------------------------------------

@app.route ("/<alias>/collection/<command>", methods = ["GET"])
def retire (was, alias, command):
	if command == "retire":
		fn = getdir ("config", alias)
		if os.path.isfile (fn):
			os.remove (fn)	
		wissen.close (alias)
	elif command == "close":
		wissen.close (alias)	
	elif command == "commit":
		wissen.get (alias).queue.commit ()		
	elif command == "rollback":
		wissen.get (alias).queue.rollback ()
	elif command == "refresh":
		wissen.refresh (alias)
	else:
		return was.response ("400 Bad Request")			
	return was.jstream ({'errmsg': 'OK', 'command': command})

@app.route ("/<alias>/collection/<group>/<fn>", methods = ["GET"])
def getfile (was, alias, group, fn):
	s = wissen.status (alias)
	if group == "primary":
		path = os.path.join (s ["indexdirs"][0], fn)
	else:
		path = os.path.join (s ["indexdirs"][0], group, fn)		
	return was.fstream (path)

#-----------------------------------------------------------------

@app.route ("/<alias>/segments/<group>/<fn>", methods = ["GET"])
def getsegfile (was, alias, group, fn):
	s = wissen.status (alias)
	seg = fn.split (".") [0]
	if group == "primary":
		path = os.path.join (s ["segmentsizes"][seg][0], fn)	
	else:
		path = os.path.join (s ["indexdirs"][0], group, fn)
	return was.fstream (path)

#-----------------------------------------------------------------

@app.route ("/<alias>/documents", methods = ["POST", "PUT", "DELETE"])
def add (was, alias, **args):	
	if was.request.command == "delete":
		q = args.get ("q")
		if not q:
			return was.response ("400 Bad Request")		
		return was.jstream (wissen.delete (alias, q))
	
	if was.request.command == "put":
		doc = was.request.json ()
		q = doc.get ("query")
		if not q:
			q = '_id:"%s"' % doc ['fields']['_id']
		wissen.delete (alias, q)
				
	wissen.get (alias).queue (0, was.request.body)
	return was.jstream ({'errmsg': 'OK'})

@app.route ("/<alias>/documents/query", methods = ["GET", "POST"])
def query (was, alias, **args):
	# args: q = '', o = 0, f = 10, s = "", w = 30, r = "", l = "un", analyze = 1, data = 1
	if is_json (was.request):
		args = was.request.json ()
	q = args.get ("q")
	if not q:
		return was.response ("400 Bad Request")
	o = args.get ("o", 0)
	f = args.get ("f", 10)
	s = args.get ("s", "")
	w = args.get ("w", 30)
	l = args.get ("l", "un")
	r = args.get ("r", "")
	analyze = args.get ("analyze", 1)
	data = args.get ("data", 1)	
	if type (q) is list:
		return was.jstream ([wissen.query (alias, eq, o, f, s, w, r, l, analyze, data, limit = 1) for eq in q])
	return was.jstream (wissen.query (alias, q, o, f, s, w, r, l, analyze, data, limit = 1))

@app.route ("/<alias>/documents/guess", methods = ["GET", "POST"])
def guess (was, alias, **args):
	# args: q = '', l = 'un', c = "naivebayes", top = 0, cond = ""
	if is_json (was.request):
		args = was.request.json ()
	q = args.get ("q")
	if not q:
		return was.response ("400 Bad Request")
	l = args.get ("l", 'un')
	c = args.get ("c", 'naivebayes')
	top = args.get ("top", 0)
	cond = args.get ("cond", '')
	if type (q) is list:
		return was.jstream ([wissen.guess (alias, eq, l, c, top, cond) for eq in q])
	return was.jstream (wissen.guess (alias, q, l, c, top, cond))
	
@app.route ("/<alias>/documents/cluster", methods = ["GET", "POST"])
def cluster (was, alias, **args):
	if is_json (was.request):
		args = was.request.json ()
	q = args.get ("q")
	if not q:
		return was.response ("400 Bad Request")	
	l = args.get ("l", 'un')	
	if type (q) is list:
		return was.jstream ([wissen.cluster (alias, eq, l) for eq in q])	
	return was.jstream (wissen.cluster (alias, q, l))

