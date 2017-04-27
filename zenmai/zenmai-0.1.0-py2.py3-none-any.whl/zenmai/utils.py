class Symbol(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<S {!r}>".format(self.name)


missing = Symbol("missing")


def isquoted(d):
    return "$quote" in d


def quote(d):
    return {"$quote": d}


def unquote(d):
    assert len(d) == 1
    return d["$quote"]
