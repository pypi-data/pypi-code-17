def apiStart(req, res, nxt):
    nxt(None) #TODO: parse body instead

def apiStop(req, res, nxt, data):
    res.json(data)
    nxt()

def data(data):
    def func(req, res, nxt, _):
        nxt(data)
    return func
