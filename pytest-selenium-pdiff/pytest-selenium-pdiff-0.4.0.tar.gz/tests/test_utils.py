import os

from pytest_selenium_pdiff import utils

def test_ensure_path_exists(tmpdir):
    path = os.path.join(str(tmpdir), 'subdir')

    assert os.path.exists(path) is False

    utils.ensure_path_exists(path)

    assert os.path.exists(path) is True
