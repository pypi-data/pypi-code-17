"""
yamlint - check YAML/JSON files satisfy a type schema

usage:
    yamlint [options] <file>...

options:
    -j          write out the input files in JSON format
    -t FILE     check the input files conform to the type schema in FILE.
    -y          write out the input files in YAML format

"""

import json
import sys

import docopt
import types4yaml
import yaml

def main():
    opts = docopt.docopt(__doc__, sys.argv[1:])

    if opts['-j'] and opts['-y']:
        print >> sys.stderr, 'warning: both -j and -y specified.'

    t = None
    if opts['-t']:
        with open(opts['-t']) as f:
            t = types4yaml.make_type(file=f)

    for fn in opts['<file>']:
        if fn == '-':
            n = 0
            for x in yaml.safe_load_all(sys.stdin):
                n += 1
                if t and not t.valid(x):
                    print >> sys.stderr, 'stdin (document %d): typecheck failed.' % (n, )
                if opts['-j']:
                    print json.dumps(x)
                if opts['-y']:
                    print yaml.safe_dump(x, explicit_start=True, default_flow_style=False)
        else:
            with open(fn) as f:
                n = 0
                for x in yaml.safe_load_all(f):
                    n += 1
                    if t and not t.valid(x):
                        print >> sys.stderr, '%s: typecheck failed.' % (fn, n)
                    if opts['-j']:
                        print json.dumps(x)
                    if opts['-y']:
                        print yaml.safe_dump(x, explicit_start=True, default_flow_style=False)

if __name__ == '__main__':
    main()
