# Some basic funcs
def skip(req, res, nxt, *args, **kwargs):
    nxt(*args, **kwargs)
def stop(req, res, nxt, *args, **kwargs):
    pass
# Function for chaining functions into one big function
def chain(*funcs):
    if funcs:
        while isinstance(funcs[0], (list, tuple)):
            funcs = list(funcs[0]) + list(funcs[1:])
        head, tail = funcs[0], chain(*funcs[1:])
        if head == stop:
            return stop
        def func(req, res, nxt, *args, **kwargs):
            def nxtFunc(*args, **kwargs):
                tail(req, res, nxt, *args, **kwargs)
            head(req, res, nxtFunc)
        return func
    else:
        return skip
# Functions for directly sending data
def html(html):
    def func(req, res, nxt):
        res.html(html)
    return func
def json(obj):
    def func(req, res, nxt):
        res.json(obj)
    return func
def text(text):
    def func(req, res, nxt):
        res.text(text)
    return func
# Function to run multiple functions and merge the args and kwargs that they send
def merge(*funcs):
    def func(req, res, nxt, *args, **kwargs):
        args_ = []
        kwargs_ = {}
        def nxtFunc(req, res, nxt, *args, **kwargs):
            args_ += args
            kwargs_ = {**kwargs_, **kwargs}
        for f in funcs:
            chain(f, nxtFunc)(req, res, None, *args, **kwargs)
        nxt(*args_, **kwargs_)
    return func
