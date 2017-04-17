"""This module tests the TimeFunction class"""

import pytest
import pandas as pd

from tssim.functions import TimeFunction


@pytest.fixture
def ts():
    """Setup test data.
    
    """

    periods = 10
    index = pd.date_range("2017-04-12", periods=periods)

    return pd.Series(range(periods), index)


def test_vectorized_no_condition(ts):
    func = lambda x: x * 2

    assert func(ts).equals(TimeFunction(func).generate(ts))
