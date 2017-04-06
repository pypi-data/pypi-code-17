class objict(dict):
    """A trick class that allows objects attributes be handled as dictionary
    keys and vice versa. That is, o.a == o['a']. Very useful when handling
    JSON."""
    def __init__(self, other=None, **kwargs):
        if other is not None:
            self.update(other)
        self.update(kwargs)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __iter__(self):
        return self.__dict__.__iter__()

    def update(self, other):
        if isinstance(other, list):
            self.__dict__.update(other)
        else:
            for k, v in other.items():
                if isinstance(v, dict):
                    self[k] = objict(v)
                else:
                    self[k] = v

    def clear(self):
        self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def items(self):
        return self.__dict__.items()

    def __bool__(self):
        return bool(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


def run_tests():
    def ass(x, y=None):
        if y is None:
            assert x
        else:
            try:
                assert x == y
            except AssertionError:
                print("%r != %r" % (x, y))
                raise

    # I can create an object and nothing explodes
    # quite basic, but I started with this
    o = objict()

    # setting items behaves like a dict
    o['a'] = 1
    ass('a' in o)
    ass(o['a'], 1)
    # and I can access the attribute
    ass(o.a, 1)

    # setting attributes behaves like an object
    o.b = 2
    ass(o.b, 2)
    # but also like a dict
    ass('b' in o)
    ass(o['b'], 2)

    # deleting items
    del o['a']
    ass('a' not in o)
    ass(not hasattr(o, 'a'))

    # deleting attributes
    del o.b
    ass(not hasattr(o, 'b'))
    ass('b' not in o)

    # constructor tests
    ass(objict(a=1).a, 1)
    ass(objict({'a': 1}).a, 1)
    ass(objict([ ('a', 1) ]).a, 1)
    o.c = 3
    ass(objict(o).c, 3)

    # recursive
    o = objict({'a': {'b': 1}})
    ass(o.a.b, 1)
    ass(o['a'].b, 1)
    ass(o.a['b'], 1)
    ass(o['a']['b'], 1)

    # other stuff
    ass(bool(o))
    ass(str(o), '''{'a': {'b': 1}}''')
    ass(repr(o), '''{'a': {'b': 1}}''')

    # we can json-dump it
    import json.encoder
    # debug
    json.encoder.c_make_encoder = None
    ass(json.dumps(o), '{"a": {"b": 1}}')

    # and of course json-load it
    # taken from http://www.json.org/example
    j = """{
    "glossary": {
        "title": "example glossary",
        "GlossDiv": {
            "title": "S",
            "GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                        "GlossSeeAlso": ["GML", "XML"]
                    },
                    "GlossSee": "markup"
                }
            }
        }
    }
}"""
    ass(objict(json.loads(j)).glossary.GlossDiv.GlossList.GlossEntry.ID, 'SGML')

if __name__ == '__main__':
    run_tests()
