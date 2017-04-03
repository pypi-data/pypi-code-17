from py_ls.pattern_matching.pattern_matching import match, case

xr = xrange(0, 1000000)

import time

a = []
b = []
start = time.clock()
for x in xr:
    if x % 2 == 0:
        a.append(x)
    else:
        b.append(x)
end = time.clock()
print(end - start)

start = time.clock()
for x in xr:
    x % 2 >> match >> (
        case > 0, 1,
        case > 1, 1
    )
end = time.clock()
print(end - start)
