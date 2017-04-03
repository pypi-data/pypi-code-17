import time
import pytest
import testincessantly

def test_debounce():
  def stream():
    yield 1
    yield 2
    yield 3
    time.sleep(0.05)
    yield 4

  debounced = testincessantly.debounce(stream(), delay=0.01)
  assert next(debounced) == [1, 2, 3]
  assert next(debounced) == [4]
