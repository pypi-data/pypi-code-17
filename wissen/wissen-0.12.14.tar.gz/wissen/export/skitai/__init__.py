import skitai
import sys, os

def init_app (pref):	
	config = pref.config
	
	sched = None
	logpath = config.get ("logpath")
	
	if config.get ("enable_mirror", False):
		script = skitai.joinpath ("appack", "mirror.py")
		script += " " + config.mirror_server
		redirect = logpath and (" > %s 2>&1" % os.path.join (logpath, "mirror.log")) or ""
		sched = config.sched_mirror
		
	elif config.get ("enable_index", False):
		script = skitai.joinpath ("appack", "indexer.py")
		redirect = logpath and (" > %s 2>&1" % os.path.join (logpath, "indexer.log")) or ""
		sched = config.sched_index
	
	if sched:
		skitai.cron (sched, r"%s %s%s" % (sys.executable, script, redirect))

	