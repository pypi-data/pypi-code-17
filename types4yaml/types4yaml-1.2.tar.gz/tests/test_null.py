from types4yaml import make_type

def test_make():
    doc = """
    null
    """
    t = make_type(doc=doc)

def test_valid():
    doc = """
    null
    """
    val = None
    t = make_type(doc=doc)
    assert t.valid(val)

def test_invalid():
    doc = """
    null
    """
    val = 1
    t = make_type(doc=doc)
    assert not t.valid(val)
