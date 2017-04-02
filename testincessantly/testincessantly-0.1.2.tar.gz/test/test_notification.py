import os
import tempfile
import testincessantly

def test_iter_modified_file_paths():
  with tempfile.TemporaryDirectory() as dirpath:
    paths = testincessantly.iter_modified_file_paths(dirpath)
    open(os.path.join(dirpath, 'a'), 'w').close()
    assert os.path.abspath(next(paths)) == os.path.abspath(os.path.join(dirpath, 'a'))
