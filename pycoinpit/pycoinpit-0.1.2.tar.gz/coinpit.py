#!/usr/bin/env python
import pycoinpit
import atexit
import sys, getopt
import json

try:
    import readline
except ImportError:
    pass
else:
    import rlcompleter
    readline.parse_and_bind('set editing-mode emacs')

verbose = False
pretty  = False
keyfile = None
url     = None

methods            = {}
methods['GET']     = True
methods['POST']    = True
methods['PUT']     = True
methods['DELETE']  = True
methods['PATCH']   = True
methods['OPTIONS'] = True

def quit_gracefully():
    print "\n"

atexit.register(quit_gracefully)

def usage():
  print "Usage: ", sys.argv[0], " -k keyfile [-v] [-u url]"
  print "    keyfile: Your json file to access coinpit app"
  print "         -v: Verbose"
  print "     -u url: Use alternate url"
  sys.exit(2)

def dump_headers(headers):
    for key in headers.keys():
        print "{}: {}".format(key, headers[key])
    print "==================================="

try:
    opts, args = getopt.getopt(sys.argv[1:], "k:u:vp", ["keyfile=", "url=", "verbose", "pretty"])
except getopt.GetoptError as err:
    print "Error parsing arguments", str(err)
    usage()

for opt, arg in opts:
    if opt == '-h':
        usage()
    elif opt in ("-k", "--keyfile"):
        keyfile = arg
    elif opt in ("-u", "--url"):
        url = arg
    elif opt in ("-v", "--verbose"):
        verbose = True
    elif opt in ("-p", "--pretty"):
        pretty = True

if keyfile == None:
    usage()

if verbose:
    print "Using keyfile: ", keyfile

key = json.load(open(keyfile))
coinpit_me = pycoinpit.client.Client(key['privateKey'], url)
coinpit_me.connect()
user = key['address']
site = coinpit_me.base_url
done = False
prompt = user + ">" if sys.stdout.isatty() and sys.stdin.isatty() else ""

def help():
    print "\nConnected to ", site
    print "Enter REST commands: METHOD path body. Enter quit to exit"
    print "For more information: https://coinpit.io/api"
    print "\nExamples: "
    print '  GET /account'
    print '  POST /order [{"price":1201.2,"side":"buy","quantity":10,"orderType":"LMT"}]'
    print '  PUT /order [{"price":1201.3,"uuid":"b117ef30-1f50-11e7-b324-e2f410d2f5f7"}]'
    print '  GET /order'
    print '  DELETE /order/b117ef30-1f50-11e7-b324-e2f410d2f5f7'
    print ' '

if verbose:
    help()
while not done:
    try:
        user_input = raw_input(prompt)
        parts = user_input.split(None, 2)
        if(len(parts) == 1):
            command = parts[0].lower()
            if(command == 'quit' or command == 'exit'):
                done = True
            elif(command == 'help'):
                help()
                continue
            elif(command == ''):
                continue
            else:
                print "Unknown command: " + command
            continue
        if(len(parts) < 2):
            print "Unknown command: " + user_input + ": HTTP Method and url (optionally body) expected. Example: GET /account"
            continue
        method_name = parts[0].upper()
        url = parts[1]
        body = None if len(parts) <= 2 else parts[2]
        if(methods[method_name] == None):
            print "Unrecognized command: {}".format(method_name)
            continue
        result = coinpit_me.rest.auth_server_call(method_name, url, body)
        if(verbose):
            canonical = coinpit_me.rest.canonical(body)
            sparse = coinpit_me.rest.sparse_json(canonical)
            print "{} {} HTTP/1.1".format(method_name, site + url)
            dump_headers(coinpit_me.rest.get_headers(method_name, url, sparse))
            print "" if body is None else json.dumps(canonical, indent=4, separators=(',', ':'))
            print result.status_code
            print "==================================="
        if(verbose or pretty):
            print json.dumps(result.json(), indent=4, separators=(',', ':'))
        else:
            print json.dumps(result.json(), separators=(',', ':'))
    except EOFError:
        done = True
    except KeyboardInterrupt:
        print "^C"
        pass
    except Exception as err:
        print "Error on request:\n {}".format(err)
