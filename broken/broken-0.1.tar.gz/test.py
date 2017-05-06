import pytest
from main import Broken,hashify


@pytest.fixture(scope='module')
def a():
    return Broken(1, 2, 3)


def test_start(a):
    assert Broken(1, 2, 3) == [1, 2, 3]
    assert Broken(1, 2, [3]) == [1, 2, [3]]
    #assert Broken(1, 2, Broken(3))[2].str == '3'
    assert Broken(1, 2, Broken(3)) == [1,2,[3]]


def test_set(a):
    assert a.set == {1, 2, 3}
    assert a.add([2]).set == {1, 2, 3,(2,)}


def test_add(a):
    assert a.add([2]).set == {1, 2, 3,(2,)}
    assert a.add(4) == [1, 2, 3, [2],4]

def test_remove(a):
    assert a.remove(3) == [1, 2,[2],4]


def test_remove(a):
    assert a.remove(3) == [1, 2,[2],4]

def test_hashify(a):
    assert hashify([3]) == (3,)
    assert hashify([3,[4]]) == (3,(4,))
    assert hashify([3,[4,[4,2,['333']]]]) == (3, (4, (4, 2, ('333',))))


def test_get_attr(a):
    a = Broken(1, 2, 3, ('e', ('i', 4)))
    assert a.e == ['i',4]
    assert a.e.i == 4



def test_assign(a):
    a = Broken(1, 2, 3, ['ey', ['i', ['ju7', 5]]])
    a.ey = ['u', 2]
    assert a == [1, 2, 3, ['ey', ['u', 2]]]
    assert a.ey == ['u', 2]
    assert a.ey.u == 2
    a.append(['e', 5])
    assert a.e == 5
    assert a.e == 5
    a.e = 2
    assert a.e == a[4][1]
    a['e'] = 2
    assert a.e == 4
    assert a.e == a[4][1]
    # a.ey.u.i == 'q'
    # assert a == [1, 2, 3, ['ey', ['u', 2,['i','q']]]]
    a = Broken(1, 2, 3, ['ey', ['i', ['ju7', 5]]])
    a.ey.i = 4
    assert a == Broken(1, 2, 3, ['ey', ['i', 4]])
    assert not a['ey']['WHATEVER']
    a = Broken(1, 2, 3, ['ey', ['i', ['ju7', 5]]])
    a.append(['e',3])
    assert a['e'] == 3


def test_append():
    a = Broken(1, 2, 3, ['ey', ['i', ['ju7', 5]]])
    a.append([1])
    assert a[-1].len





def test_nested_keys(a):
    a = Broken(1, 2, 3, ['ey', ['i', ['ju7', 5]]])
    assert a.ey.i.ju7 == 5
    assert a == [1, 2, 3, ['ey', ['i', ['ju7', 5]]]]




def test_get_item():
    a = Broken(1, 2, 3, ['ey', ['i', ['ju7', 5]]])
    assert a['ey'] == ['i', ['ju7', 5]]
    assert a['ey']['i'] == ['ju7', 5]
    assert a['ey']['i']['ju7'] == 5





