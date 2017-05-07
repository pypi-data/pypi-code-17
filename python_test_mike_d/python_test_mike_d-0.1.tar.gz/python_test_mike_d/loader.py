import argparse
from timeit import default_timer


# Error for situations where the loaded code doesn't have necessary functions
class FunctionsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


# Wrapper for run(n) that measures time
def measure_time(f):
    def wrapper(*args, **kwargs):
        start = default_timer()
        f(*args, **kwargs)
        end = default_timer()
        return end - start
    return wrapper


# Check for the necessary functions in loaded code
def check_functions(name):

    source_code = __import__(name)
    if not hasattr(source_code, 'init'):
        raise FunctionsError("The function init is missing in the loaded object.")
    if not hasattr(source_code, 'run'):
        raise FunctionsError("The function run is missing in the loaded object.")
    if not hasattr(source_code, 'clean'):
        raise FunctionsError("The function clean is missing in the loaded object.")

    # Test run
    try:
        c = source_code.init(1)
    except Exception:
        raise FunctionsError("The function init doesn't work correctly.")
    try:
        source_code.run(c)
    except Exception:
        raise FunctionsError("The function run doesn't work correctly")
    try:
        source_code.clean(c)
    except Exception:
        raise FunctionsError("The function clean doesn't work correctly")

    return source_code
