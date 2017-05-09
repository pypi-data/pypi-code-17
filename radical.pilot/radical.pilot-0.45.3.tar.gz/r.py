#!/usr/bin/env python

N = 1024 * 1024

import time
import resource      as r
import radical.utils as ru

urls = list()
for i in range(N):
    urls.append(ru.Url("file://localhost:123/path/to/file"))
    if not i % 1024:
        print "%-10d -- %10d" % (len(urls), r.getrusage(r.RUSAGE_SELF).ru_maxrss)

time.sleep(10)

