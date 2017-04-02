

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
    for people, pos in social_network.items():
        placer.add(people, *pos)

def test_basic_navigation(placer, mockdata):
    one, two, tee, foo = mockdata
    assert isinstance(placer.add(one, 100, 100), MockData)
    assert isinstance(placer.add(two, 200, 100), MockData)
    assert isinstance(placer.add(tee, 200, 200), MockData)
    assert isinstance(placer.add(foo, 100, 200), MockData)
    placer.move(foo, 50, 0)
    nearests = tuple(placer.nearests(foo))
    assert len(nearests) == 1
    assert nearests[0] is tee
