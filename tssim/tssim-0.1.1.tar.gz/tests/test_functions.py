"""This module tests the TimeFunction class"""

import pandas as pd
import pytest

import tssim

@pytest.fixture
def ts():
    """Setup test data.
    
    """

    periods = 10
    index = pd.date_range("2017-04-12", periods=periods)

    return pd.Series(range(periods), index)


def test_vectorized_no_condition(ts):
    func = lambda x: x * 2

    assert func(ts).equals(tssim.TimeFunction(func).generate(ts))
