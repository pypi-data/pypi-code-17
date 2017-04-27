from types4yaml import make_type

def test_make():
    doc = """
    boolean
    """
    t = make_type(doc=doc)

def test_valid_0():
    doc = """
    boolean
    """
    t = make_type(doc=doc)
    vals = [True, False]
    for val in vals:
        assert t.valid(val)

def test_valid_1():
    doc = """
    boolean
    """
    t = make_type(doc=doc)
    vals = [0, 1]
    for val in vals:
        assert t.valid(val)

def test_valid_2():
    doc = """
    boolean
    """
    t = make_type(doc=doc)
    vals = ['y', 'yes', 'Yes', 'YES', 'n', 'no', 'No']
    for val in vals:
        assert t.valid(val)

def test_valid_3():
    doc = """
    boolean
    """
    t = make_type(doc=doc)
    vals = ['on', 'On', 'ON', 'off', 'Off', 'OFF']
    for val in vals:
        assert t.valid(val)

def test_valid_4():
    doc = """
    boolean
    """
    t = make_type(doc=doc)
    vals = ['true', 'True', 'TRUE', 'false', 'False', 'FALSE']
    for val in vals:
        assert t.valid(val)

def test_invalid_1():
    doc = """
    boolean
    """
    val = 42
    t = make_type(doc=doc)
    assert not t.valid(val)

def test_invalid_2():
    doc = """
    boolean
    """
    val = "foo"
    t = make_type(doc=doc)
    assert not t.valid(val)
