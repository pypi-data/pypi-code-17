#!/usr/bin/env python

import wptools
import time

n = 1
t = int(time.time())

while True:
    p = wptools.page(show=False, silent=True)
    d = int(time.time()) - t
    print "[%d]" % n, p.title, d, "seconds"
    try:
        p.get()
    except LookupError:
        pass  # no Wikidata, e.g. Stylochoerus
    time.sleep(3)
    n += 1
