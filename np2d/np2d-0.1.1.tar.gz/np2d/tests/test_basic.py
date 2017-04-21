from nose import tools
from ..basic import kmax, kmin
import numpy as np

def test_kmax():
    """Test kmax."""
    nvals = 3
    dims = 10
    # Get a set of values bigger than anything in the array
    max_vals = np.arange(20+nvals,20, -1, dtype=float)
    # Get a random set of indices
    x = np.random.choice(dims, size=nvals)
    y = np.random.choice(dims, size=nvals)
    # Generate a random array
    a = np.random.uniform(low=0, high=10, size=(dims,dims))
    a[x,y] = max_vals

    # Run the function
    vals, indices = kmax(a, 3)

    # Test the output
    np.testing.assert_array_equal(max_vals, vals)
    np.testing.assert_array_equal(x, indices[:,0])
    np.testing.assert_array_equal(y, indices[:,1])

def test_kmin():
    """Test kmin."""
    nvals = 3
    dims = 10
    # Get a set of values bigger than anything in the array
    min_vals = np.arange(0, nvals, dtype=float)
    # Get a random set of indices
    x = np.random.choice(dims, size=nvals)
    y = np.random.choice(dims, size=nvals)
    # Generate a random array
    a = np.random.uniform(low=10, high=20, size=(dims,dims))
    a[x,y] = min_vals

    # Run the function
    vals, indices = kmin(a, 3)

    # Test the output
    np.testing.assert_array_equal(min_vals, vals)
    np.testing.assert_array_equal(x, indices[:,0])
    np.testing.assert_array_equal(y, indices[:,1])
