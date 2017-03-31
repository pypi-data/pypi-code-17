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
            head(req, res, nxtFunc, *args, **kwargs)
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
        args_ = ()
        kwargs_ = {}
        def nxtFunc(*args, **kwargs):
            nonlocal args_, kwargs_
            args_ += args
            kwargs_ = {**kwargs_, **kwargs}
        for f in funcs:
            if isinstance(f, (list, dict)):
                f = chain(f)
            f(req, res, nxtFunc, *args, **kwargs)
        nxt(*args_, **kwargs_)
    return func
# Function to pass on any arguments and keyword arguments to the next function
def args(*args, **kwargs):
    def func(req, res, nxt, *args_, **kwargs_):
        nxt(*args, **kwargs)
    return func
# Same but for the args that were captured in the url
def urlArgs(args=True, kwargs=True):
    def func(req, res, nxt, *args_, **kwargs_):
        nxt(*req.args if args else [], **req.kwargs if kwargs else {})
    return func
# Same two functions as above but adding to the current args and kwargs instead of replacing
addArgs = lambda *args_, **kwargs: merge(skip, args(*args_, **kwargs))
addUrlArgs = lambda args=True, kwargs=True: merge(skip, urlArgs(args, kwargs))
# Function to choose between two different functions based on a condition function
def cond(if_, then_, else_=skip):
    def func(req, res, nxt, *args, **kwargs):
        if chain(if_)(req, res, None, *args, **kwargs):
            then_(req, res, nxt, *args, **kwargs)
        else:
            else_(req, res, nxt, *args, **kwargs)
    return func
