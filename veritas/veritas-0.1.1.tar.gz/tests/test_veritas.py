# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from decimal import Decimal as D
from fractions import Fraction as F

import pytest

from veritas import Teritas

class TestTeritas:

    def test_basic_customization(self):
        # init
        assert Teritas
        assert Teritas()
        assert Teritas('any', 'arguments', (2,3,4), dir(type))

        _ = Teritas()

        # repr
        assert repr(_) == '<class Teritas>'

        # str
        assert str(_) == '<class Teritas>'

        # TODO: bytes
        assert bytes(_) == b'<class Teritas>'

        # format
        assert format(_) == '<class Teritas>'


    def test_ordering(self):
        _ = Teritas()

        test_values = [
            float('-inf'),
            D('-1e425000000'),
            -1e308,
            F(-22, 7),
            -3.14,
            -2,
            0.0,
            1e-320,
            True,
            F('1.2'),
            D('1.3'),
            float('1.4'),
            F(275807, 195025),
            D('1.414213562373095048801688724'),
            F(114243, 80782),
            F(473596569, 84615),
            7e200,
            D('infinity'),
            Teritas,
            Teritas()
        ]
        for test_value in test_values:
            assert _ < test_value
            assert _ <= test_value
            assert _ == test_value
            assert _ != test_value
            assert _ > test_value
            assert _ >= test_value

        assert hash(_)
        assert hash(_) == True

        assert bool(_) == True


    def test_attribute_access(self):
        _ = Teritas()
        assert _.any_method() == True

        _.any_other_method = lambda x: False
        assert _.any_other_method() == True

        del _.yet_another_method
        assert _.yet_another_method() == True

        # Teritas is returned, which means ordering rules work!
        assert _.final_method() != True
        assert _.final_method() == True
        assert _.final_method() < True
        assert _.final_method() > True

        assert repr(_.final_method()) == '<class Teritas>'


    def test_callable(self):
        assert Teritas
        assert Teritas()
        assert Teritas()()
        assert Teritas('any', 'arguments')('=')(true=True)


    def test_container(self):
        _ = Teritas()

        assert len(_)

        assert _[1]
        assert _[3:4]
        _[0] = False
        assert _[0]

        del _[3]
        assert _[3]

        for x in _:
            assert x



    def test_numeric_types(self):
        '''binary ops, bitwise ops,
        '''
        _ = Teritas()

        test_values = [
            float('-inf'),
            #D('-1e425000000'),
            -1e308,
            -3.14,
            -2,
            1e-320,
            7e200
        ]
        for test_value in test_values:
            assert _ + test_value
            assert _ - test_value
            assert _ * test_value
            assert _ / test_value
            assert _ // test_value
            assert _ % test_value
            assert divmod(_, test_value)
            assert pow(_, test_value)
            assert _ ** test_value

            # associative?
            assert test_value + _
            assert test_value - _
            assert test_value * _
            assert test_value / _
            assert test_value // _
            assert test_value % _
            assert divmod(test_value, _)
            assert pow(test_value, _)
            assert test_value ** _

            # rsub
            _ += test_value
            _ -= test_value
            _ *= test_value
            _ /= test_value
            _ //= test_value
            _ %= test_value
            _ **= test_value

        assert _ << 1
        assert _ >> 1
        assert _ & 1
        assert _ ^ 1
        assert _ | 1

        assert 1 & _
        assert 1 ^ _
        assert 1 | _

        _ &= 1
        _ ^= 1
        _ |= 1

        assert abs(_)
        assert -_
        assert +_
        assert ~_


    def test_context_manager(self):
        with Teritas() as x:
            assert x
