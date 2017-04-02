import time
import gc
import os
from collections import defaultdict

import numpy as np
import xarray as xr

import pytest

from pyndl import ndl
from pyndl.activation import activation

slow = pytest.mark.skipif(not pytest.config.getoption("--runslow"),
                          reason="need --runslow option to run")

TEST_ROOT = os.path.join(os.path.pardir, os.path.dirname(__file__))
FILE_PATH_SIMPLE = os.path.join(TEST_ROOT, "resources/event_file_simple.tab")
FILE_PATH_MULTIPLE_CUES = os.path.join(TEST_ROOT, "resources/event_file_multiple_cues.tab")

LAMBDA_ = 1.0
ALPHA = 0.1
BETAS = (0.1, 0.1)


def test_exceptions():
    with pytest.raises(ValueError) as e_info:
        wm = ndl.dict_ndl(FILE_PATH_SIMPLE, ALPHA, BETAS, remove_duplicates=None)
        activation(FILE_PATH_MULTIPLE_CUES, wm)
        assert e_info == 'cues or outcomes needs to be unique: cues "a a"; outcomes "A"; use remove_duplicates=True'

    with pytest.raises(ValueError) as e_info:
        activation(FILE_PATH_MULTIPLE_CUES, "magic")
        assert e_info == "Weights other than xarray.DataArray or dicts are not supported."


def test_activation_matrix():
    weights = xr.DataArray(np.array([[0, 1], [1, 0], [0, 0]]),
                           coords={
                               'cues': ['c1', 'c2', 'c3']
                           },
                           dims=('cues', 'outcomes'))
    events = [(['c1', 'c2', 'c3'], []),
              (['c1', 'c3'], []),
              (['c2'], []),
              (['c1', 'c1'], [])]
    reference_activations = np.array([[1, 1], [0, 1], [1, 0], [0, 1]])

    with pytest.raises(ValueError):
        activations = activation(events, weights, number_of_threads=1)

    activations = activation(events, weights, number_of_threads=1, remove_duplicates=True)
    activations_mp = activation(events, weights, number_of_threads=3, remove_duplicates=True)

    assert np.allclose(reference_activations, activations)
    assert np.allclose(reference_activations, activations_mp)


def test_activation_dict():
    weights = defaultdict(lambda: defaultdict(float))
    weights['o1']['c1'] = 0
    weights['o1']['c2'] = 1
    weights['o1']['c3'] = 0
    weights['o2']['c1'] = 1
    weights['o2']['c2'] = 0
    weights['o2']['c3'] = 0
    events = [(['c1', 'c2', 'c3'], []),
              (['c1', 'c3'], []),
              (['c2'], []),
              (['c1', 'c1'], [])]
    reference_activations = {
        'o1': [1, 0, 1, 0],
        'o2': [1, 1, 0, 1]
    }

    with pytest.raises(ValueError):
        activations = activation(events, weights, number_of_threads=1)

    activations = activation(events, weights, number_of_threads=1, remove_duplicates=True)
    for outcome, activation_list in activations.items():
        assert np.allclose(reference_activations[outcome], activation_list)


@slow
def test_activation_matrix_large():
    """
    Test with a lot of data. Better run only with at least 12GB free RAM.
    To get time prints for single and multiprocessing run with pytest ... --capture=no --runslow
    """
    print("")
    print("Start setup...")

    def time_test(func, of=""):
        def dec_func(*args, **kwargs):
            print("start test '{}'".format(of))
            st = time.clock()
            res = func(*args, **kwargs)
            et = time.clock()
            print("finished test '{}'".format(of))
            print("  duration: {:.3f}s".format(et-st))
            print("")
            return res
        return dec_func

    n = 2000
    n_cues = 10*n
    n_outcomes = n
    n_events = 10*n
    n_cues_per_event = 30
    weight_mat = np.random.rand(n_cues, n_outcomes)
    cues = ['c'+str(i) for i in range(n_cues)]
    weights = xr.DataArray(weight_mat,
                           coords={'cues': cues},
                           dims=('cues', 'outcomes'))
    events = [(np.random.choice(cues, n_cues_per_event), [])
              for i in range(n_events)]  # no generator, we use it twice

    print("Start test...")
    print("")
    gc.collect()
    asp = (time_test(activation, of="single threaded")
           (events, weights, number_of_threads=1, remove_duplicates=True))
    gc.collect()
    amp = (time_test(activation, of="multi threaded (up to 8 threads)")
           (events, weights, number_of_threads=8, remove_duplicates=True))
    del weights
    del events
    gc.collect()
    print("Compare results...")
    assert np.allclose(asp, amp), "single and multi threaded had different results"
    print("Equal.")
