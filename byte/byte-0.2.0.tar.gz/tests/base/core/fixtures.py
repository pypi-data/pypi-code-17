from __future__ import absolute_import, division, print_function

from tests.base.core.helpers import FIXTURES_PATH, copy_tree, uri_from_path

from contextlib import contextmanager
from tempfile import NamedTemporaryFile, mkdtemp
import logging
import os
import shutil

log = logging.getLogger(__name__)


@contextmanager
def get_fixture(path, copy=True):
    """Retrieve fixture path.

    :param path: Fixture path (relative to fixtures directory)
    :type path: str

    :param copy: Create a copy of the fixture
    :type copy: bool
    """
    source_path = os.path.abspath(os.path.join(FIXTURES_PATH, path))

    # Ensure fixture exists
    if not os.path.exists(source_path):
        raise ValueError('Fixture %r doesn\'t exist' % (path,))

    # Return actual fixture path (if `copy` has been disabled)
    if not copy:
        yield source_path
        return

    # Copy fixture to temporary path
    if os.path.isdir(source_path):
        temp_path = copy_fixture_directory(source_path)
    else:
        temp_path = copy_fixture_file(source_path)

    try:
        # Return temporary fixture path
        yield temp_path
    finally:
        # Try delete temporary fixture
        try:
            if os.path.isdir(temp_path):
                shutil.rmtree(temp_path)
            else:
                os.remove(temp_path)
        except Exception as ex:
            log.warn('Unable to delete temporary fixture: %s', ex, exc_info=True)


@contextmanager
def get_fixture_uri(path, copy=True):
    """Retrieve fixture URI.

    :param path: Fixture path (relative to fixtures directory)
    :type path: str

    :param copy: Create a copy of the fixture
    :type copy: bool
    """
    single = False

    if type(path) is not tuple:
        single = True
        path = (path,)

    # Retrieve fixture generators
    fixtures = [
        get_fixture(p, copy=copy)
        for p in path
    ]

    # Yield fixture uris
    try:
        uris = [
            uri_from_path(fixture.__enter__()) for fixture in fixtures
        ]

        if not single:
            yield tuple(uris)
        else:
            yield uris[0]
    finally:
        # Cleanup fixtures
        for fixture in fixtures:
            try:
                fixture.__exit__()
            except:
                pass


def copy_fixture_directory(source_path):
    """Copy fixture directory.

    :param source_path: Source path
    :type source_path: str
    """
    temp_path = mkdtemp()

    # Copy contents of `path` into temporary directory
    copy_tree(source_path, temp_path)

    # Return temporary fixture path
    return temp_path


def copy_fixture_file(source_path):
    """Copy fixture file.

    :param source_path: Source path
    :type source_path: str
    """
    _, ext = os.path.splitext(source_path)

    # Create copy of fixture to temporary path
    with NamedTemporaryFile(suffix=ext, delete=False) as tp:
        with open(source_path, 'rb') as fp:
            shutil.copyfileobj(fp, tp)

        temp_path = tp.name

    # Return temporary fixture path
    return temp_path
