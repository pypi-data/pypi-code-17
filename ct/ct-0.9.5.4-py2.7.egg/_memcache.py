import datetime
from cantools.web import respond, succeed, cgi_get, getmem, setmem, delmem, read_file, send_file
from cantools.util import token, transcode

def response():
	action = cgi_get("action", choices=["get", "set", "forget"])
	key = cgi_get("key")
	json = cgi_get("json", default=False)
	mode = cgi_get("mode", default="normal")
	if action == "forget":
		delmem(key)
	elif action == "get":
		data = getmem(key, json)
		if data and mode == "countdown":
			succeed({
				"ttl": (data["ttl"] - datetime.datetime.now()).total_seconds(),
				"token": data["token"]
			})
		elif mode == "blob":
			send_file(data, detect=True)
		succeed(data)
	elif action == "set":
		value = cgi_get("value")
		if mode == "countdown":
			setmem(key, {
				"ttl": datetime.datetime.now() + datetime.timedelta(0, value),
				"token": token()
			}, json)
		elif mode == "blob":
			value = read_file(value)
			if cgi_get("transcode", default=False):
				value = transcode(value, True)
			setmem(key, value, False) # JSON disallowed
		else:
			setmem(key, value, json)

respond(response)