#!/usr/bin/env python
N = 1024 * 10
import resource
import radical.utils as ru
urls = list()
for i in range(N):
    urls.append(ru.Url("file://localhost:123/path/to/file"))
    print "%-10d  %10.2f kb" % \
       (len(urls), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)) 

