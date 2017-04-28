import hfst

transducers = []

with open('testfile.att', 'r') as f:
    r = hfst.AttReader(f, "<eps>")
    for tr in r:
        transducers.append(tr)

assert(f.closed)
assert(len(transducers)) == 4

transducers = []

with open('testfile_fail.att', 'r') as f:
    try:
        r = hfst.AttReader(f, "<eps>")
        for tr in r:
            transducers.append(tr)
    except hfst.exceptions.NotValidAttFormatException as e:
        assert("1      baz    baz      0.3" in e.what())
        assert("line: 11" in e.what())

assert(f.closed)
assert(len(transducers)) == 4
