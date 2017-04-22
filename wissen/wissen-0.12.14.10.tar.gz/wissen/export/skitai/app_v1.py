# 2017. 3. 13 by Hans Roh (hansroh@gmail.com)

__version__ = "0.1"
version_info = tuple (map (lambda x: not x.isdigit () and x or int (x),  __version__.split (".")))
	
import os
from skitai.saddle import Saddle
import skitai
import wissen
from wissen.lib import pathtool
import json
import codecs

app = Saddle (__name__)
app.debug = True
app.use_reloader = True
app.config.numthreads = 1

def getdir (*d):
	return os.path.join (app.config.resource_dir, *d)

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
def configure (was, alias, config = None):
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
		return was.jstream (status)
			
	if was.request.command == "delete":		
		wissen.drop (alias)
		os.remove (fn)		
		return was.jstream (wissen.status (alias))
	
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
def unlock (was, alias):	
	return was.jstream ({'errmsg': 'OK', "locks": wissen.get (alias).si.lock.locks ()})	

@app.route ("/<alias>/locks/<name>", methods = ["GET", "DELETE"])
def lock (was, alias, name):	
	if was/request.command == "get":
		wissen.get (alias).si.lock.lock (name)		
		return was.jstream ({'errmsg': 'OK', "lock": name})
	wissen.get (alias).si.lock.unlock (name)		
	return was.jstream ({'errmsg': 'OK', "unlock": name})

#-----------------------------------------------------------------

@app.route ("/<alias>/collection/retire", methods = ["GET"])
def retire (was, alias):
	fn = getdir ("config", alias)
	if os.path.isfile (fn):
		os.remove (fn)	
	wissen.close (alias)		
	return was.jstream ({'errmsg': 'OK'})

@app.route ("/<alias>/collection/close", methods = ["GET"])
def close (was, alias):
	wissen.close (alias)		
	return was.jstream ({'errmsg': 'OK'})

@app.route ("/<alias>/collection/commit", methods = ["GET"])
def commit (was, alias):	
	wissen.get (alias).queue.commit ()		
	return was.jstream ({'errmsg': 'OK'})

@app.route ("/<alias>/collection/rollback", methods = ["GET"])
def rollback (was, alias):	
	wissen.get (alias).queue.rollback ()
	return was.jstream ({'errmsg': 'OK'})

@app.route ("/<alias>/collection/refresh", methods = ["GET"])
def refresh (was, alias):
	return was.jstream (wissen.refresh (alias))

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
def add (was, alias):	
	if was.request.command == "delete":
		return was.jstream (wissen.delete (alias, q, a == "yes" and 1 or 0))			
	wissen.get (alias).queue (was.request.command, was.request.body)			
	return was.jstream ({'errmsg': 'OK'})

@app.route ("/<alias>/documents/query", methods = ["GET", "POST"])
def query (was, alias, **args):
	# args: q = '', o = 0, f = 10, s = "", w = 30, r = "", l = "un", analyze = 1, data = 1
	if was.request.command == "post" and not was.request.get_header ('content-type', '').startswith ('application/x-www-form-urlencoded'):
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
	return was.jstream (wissen.query (alias, q, o, f, s, w, r, l, analyze, data, limit = 1))

@app.route ("/<alias>/documents/guess", methods = ["GET", "POST"])
def guess (was, alias, **args):
	# args: q = '', l = 'un', c = "naivebayes", top = 0, cond = ""
	if was.request.command == "post" and not was.request.get_header ('content-type', '').startswith ('application/x-www-form-urlencoded'):
		args = was.request.json ()
	q = args.get ("q")
	if not q:
		return was.response ("400 Bad Request")
	l = args.get ("l", 'un')
	c = args.get ("c", 'naivebayes')
	top = args.get ("top", 0)
	cond = args.get ("cond", '')	
	return was.jstream (wissen.guess (alias, q, l, c, top, cond))
	
@app.route ("/<alias>/documents/cluster", methods = ["GET", "POST"])
def cluster (was, alias, q, l = 'un'):
	return was.jstream (wissen.cluster (alias, q, l))

@app.route ("/<alias>/documents/mguess", methods = ["POST"])
def mguess (was, alias):	
	mq = was.request.json ()
	l = mq.get ("l", 'un')
	c = mq.get ("c", 'naivebayes')
	top = mq.get ("top", 0)
	cond = mq.get ("cond", '')
	qs = mq ["q"]
	
	res = []
	for q in qs:
		res.append (wissen.guess (alias, q, l, c, top, cond))
	return was.jstream (res)

@app.route ("/<alias>/documents/mquery", methods = ["POST"])
def mquery (was, alias):	
	mq = was.request.json ()
	o = mq.get ("o", 0)
	f = mq.get ("f", 10)
	s = mq.get ("s", "")
	w = mq.get ("w", 30)
	l = mq.get ("l", "un")
	r = mq.get ("r", "")
	analyze = mq.get ("analyze", 1)
	data = mq.get ("data", 1)
	qs = mq ["q"]
	
	res = []
	for q in qs:
		res.append (wissen.query (alias, q, o, f, s, w, r, l, analyze, data, limit = 1))
	return was.jstream (res)
		

