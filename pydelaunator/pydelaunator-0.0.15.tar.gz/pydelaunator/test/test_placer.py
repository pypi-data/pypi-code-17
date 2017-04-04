

import random
import pytest
from pydelaunator import Placer


class MockData:
    def __init__(self):
        self.data = random.randint(1, 1000)


@pytest.fixture
def placer():
    return Placer(1000, 1000)

@pytest.fixture
def social_network() -> dict:
    return {
        'Michel': (100, 100),
        'Gislaine': (500, 350),
        'Gérard': (200, 300),
        'Micheline': (400, 150),
    }

@pytest.fixture
def mockdata():
    return MockData(), MockData(), MockData(), MockData()


def test_basics(placer, social_network):
    added = set()
    for people, pos in social_network.items():
        placer.add(people, *pos)
        added.add((people, pos))
    assert set(placer.objects_and_positions) == added


def test_basic_navigation(placer, mockdata):
    one, two, tee, foo = mockdata
    positions = {one: (100, 100), two: (200, 100), tee: (200, 200), foo: (100, 200)}
    for obj, pos in positions.items():
        assert isinstance(placer.add(obj, *pos), MockData)
    assert set(placer.objects_and_positions) == set(positions.items())
    placer.move(foo, 50, 0)
    assert placer.position_of(foo) == (150, 200)
    nearests = tuple(placer.nearests(foo))
    assert len(nearests) == 1
    assert nearests[0] is tee
    neis = tuple(placer.neighbors(foo, max_dist=50))
    assert len(nearests) == 1
    assert nearests[0] is tee
    neis = set(placer.neighbors(foo, min_dist=51))
    print(*map(str, neis))
    assert len(neis) == 2
    assert neis == {one, two}
