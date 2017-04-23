import pytest
import boogie


def test_project_defines_author_and_version():
    assert hasattr(boogie, '__author__')
    assert hasattr(boogie, '__version__')
