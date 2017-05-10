# waelstow.py
__version__ = '0.10.0'

import contextlib, os, shutil, sys, tempfile, json
from unittest import TestCase, TestSuite, TestLoader

from six import StringIO

# =============================================================================
# Test Suite Discovery & Management
# =============================================================================

def list_tests(suites):
    """Takes a list of suites and returns an iterable of all the tests in
    the suites and their children.

    :param suites:
        A single or an interable of :class:`TestSuite` objects whose contents
        will be listed
    :returns:
        Iterable of :class:`TestCase` objects contained within the suites
    """
    for test in suites:
        if test.__class__.__name__ == 'ModuleImportFailure':
            # ignore the import fail module
            pass
        elif isinstance(test, TestCase):
            yield test
        else:
            for t in list_tests(test):
                yield t


def find_shortcut_tests(suites, shortcut_labels):
    """Takes a suite of tests and returns a list of tests that conform to the
    passed in list of short-cut labels.  A short-cut label begins with an "="
    and is then checked against the full test case and method name, if the
    shortcut string is in the full test name then the test is returned.

    Example:

    .. code-block::python

    >>> list_tests(suite)
    [
        test_foo (wrench.test.SomeTest),
        test_foo (wrench.test.AnotherTest),
        test_bar (wrench.test.AnotherTest),
        test_bar (wrench.test.DifferentTest),
    ]
    >>> find_shorcut_tests(suite, ['=foo'])
    [
        test_foo (wrench.test.SomeTest),
        test_foo (wrench.test.AnotherTest),
    ]
    >>> find_shorcut_tests(suite, ['=Another'])
    [
        test_foo (wrench.test.AnotherTest),
        test_bar (wrench.test.AnotherTest),
    ]

    :param suites:
        A single or iterable of :class:`TestSuite` objects to create the test
        subset from
    :param shortcut_labels:
        A list of short-cut labels to use to cull the list
    :returns:
        A list of :class:`TestCase` objects 
    """
    # strip the '=' from the front of each label
    labels = [label[1:] for label in shortcut_labels]

    results = []
    for test in list_tests(suites):
        name = '%s.%s.%s' % (test.__module__, test.__class__.__name__,
            test._testMethodName)
        for label in labels:
            if label in name:
                results.append(test)

    return results


def discover_tests(start_dir, labels=[], pattern='test*.py'):
    """Discovers tests in a given module filtered by labels.  Supports
    short-cut labels as defined in :func:`find_shortcut_labels`.

    :param start_dir:
        Name of directory to begin looking in
    :param labels:
        Optional list of labels to filter the tests by
    :returns:
        :class:`TestSuite` with tests
    """
    shortcut_labels = []
    full_labels = []
    for label in labels:
        if label.startswith('='):
            shortcut_labels.append(label)
        else:
            full_labels.append(label)

    if not full_labels and not shortcut_labels:
        # no labels, get everything
        return TestLoader().discover(start_dir, pattern=pattern)

    shortcut_tests = []
    if shortcut_labels:
        suite = TestLoader().discover(start_dir, pattern=pattern)
        shortcut_tests = find_shortcut_tests(suite, shortcut_labels)

    if full_labels:
        suite = TestLoader().loadTestsFromNames(full_labels)
        suite.addTests(shortcut_tests)
    else:
        # only have shortcut labels
        suite = TestSuite(shortcut_tests)

    return suite

# =============================================================================
# Context Managers
# =============================================================================

@contextlib.contextmanager
def replaced_directory(dirname):
    """This ``Context Manager`` is used to move the contents of a directory
    elsewhere temporarily and put them back upon exit.  This allows testing
    code to use the same file directories as normal code without fear of
    damage.

    The name of the temporary directory which contains your files is yielded.

    :param dirname:
        Path name of the directory to be replaced.


    Example:

    .. code-block:: python

        with replaced_directory('/foo/bar/') as rd:
            # "/foo/bar/" has been moved & renamed
            with open('/foo/bar/thing.txt', 'w') as f:
                f.write('stuff')
                f.close()


        # got here? => "/foo/bar/ is now restored and temp has been wiped, 
        # "thing.txt" is gone
    """
    if dirname[-1] == '/':
        dirname = dirname[:-1]

    full_path = os.path.abspath(dirname)
    if not os.path.isdir(full_path):
        raise AttributeError('dir_name must be a directory')

    base, name = os.path.split(full_path)

    # create a temporary directory, move provided dir into it and recreate the
    # directory for the user
    tempdir = tempfile.mkdtemp()
    shutil.move(full_path, tempdir)
    os.mkdir(full_path)
    try:
        yield tempdir

    finally:
        # done context, undo everything
        shutil.rmtree(full_path)
        moved = os.path.join(tempdir, name)
        shutil.move(moved, base)
        shutil.rmtree(tempdir)


@contextlib.contextmanager
def capture_stdout():
    """This ``Context Manager`` redirects STDOUT to a ``StringIO`` objects
    which is returned from the ``Context``.  On exit STDOUT is restored.

    Example:

    .. code-block:: python

        with capture_stdout() as capture:
            print('foo')

        # got here? => capture.getvalue() will now have "foo\\n"
    """
    stdout = sys.stdout
    try:
        capture_out = StringIO()
        sys.stdout = capture_out
        yield capture_out
    finally:
        sys.stdout = stdout


@contextlib.contextmanager
def capture_stderr():
    """This ``Context Manager`` redirects STDERR to a ``StringIO`` objects
    which is returned from the ``Context``.  On exit STDERR is restored.

    Example:

    .. code-block:: python

        with capture_stderr() as capture:
            print('foo')

        # got here? => capture.getvalue() will now have "foo\\n"
    """
    stderr = sys.stderr
    try:
        capture_out = StringIO()
        sys.stderr = capture_out
        yield capture_out
    finally:
        sys.stderr = stderr


# =============================================================================
# Misc
# =============================================================================

def pprint(data):
    """Alternative to `pprint.PrettyPrinter()` that uses `json.dumps()` for
    sorting and displaying data.  

    :param data: item to print to STDOUT.  The item must be json serializable!
    """
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
