from __future__ import absolute_import

from itertools import islice
from collections import OrderedDict

from turbodbc_intern import make_row_based_result_set, make_parameter_set

from .exceptions import translate_exceptions, InterfaceError, Error

def _has_numpy_support():

    try:
        import turbodbc_numpy_support
        return True
    except ImportError:
        return False

def _make_masked_arrays(result_batch):
    from numpy.ma import MaskedArray
    from numpy import object_
    masked_arrays = []
    for data, mask in result_batch:
        if isinstance(data, list):
            masked_arrays.append(MaskedArray(data=data, mask=mask, dtype=object_))
        else:
            masked_arrays.append(MaskedArray(data=data, mask=mask))
    return masked_arrays

class Cursor(object):
    def __init__(self, impl):
        self.impl = impl
        self.result_set = None
        self.rowcount = -1
        self.arraysize = 1

    def __iter__(self):
        return self

    def __next__(self):
        element = self.fetchone()
        if element is None:
            raise StopIteration
        else:
            return element

    next = __next__  # Python 2 compatibility

    def _assert_valid(self):
        if self.impl is None:
            raise InterfaceError("Cursor already closed")

    def _assert_valid_result_set(self):
        if self.result_set is None:
            raise InterfaceError("No active result set")

    @property
    def description(self):
        if self.result_set:
            info = self.result_set.get_column_info()
            return [(c.name, c.type_code(), None, None, None, None, c.supports_null_values) for c in info]
        else:
            return None

    @translate_exceptions
    def execute(self, sql, parameters=None):
        """Execute an SQL query"""
        self._assert_valid()
        self.impl.prepare(sql)
        if parameters:
            buffer = make_parameter_set(self.impl)
            buffer.add_set(parameters)
            buffer.flush()
        self.impl.execute()
        self.rowcount = self.impl.get_row_count()
        cpp_result_set = self.impl.get_result_set()
        if cpp_result_set:
            self.result_set = make_row_based_result_set(cpp_result_set)
        else:
            self.result_set = None
        return self

    @translate_exceptions
    def executemany(self, sql, parameters=None):
        """Execute an SQL query"""
        self._assert_valid()
        self.impl.prepare(sql)

        if parameters:
            buffer = make_parameter_set(self.impl)
            for parameter_set in parameters:
                buffer.add_set(parameter_set)
            buffer.flush()

        self.impl.execute()
        self.rowcount = self.impl.get_row_count()
        cpp_result_set = self.impl.get_result_set()
        if cpp_result_set:
            self.result_set = make_row_based_result_set(cpp_result_set)
        else:
            self.result_set = None
        return self

    @translate_exceptions
    def fetchone(self):
        self._assert_valid_result_set()
        result = self.result_set.fetch_row()
        if len(result) == 0:
            return None
        else:
            return result

    @translate_exceptions
    def fetchall(self):
        return [row for row in self]

    @translate_exceptions
    def fetchmany(self, size=None):
        if size is None:
            size = self.arraysize
        if (size <= 0):
            raise InterfaceError("Invalid arraysize {} for fetchmany()".format(size))

        return [row for row in islice(self, size)]

    def fetchallnumpy(self):
        from numpy.ma import concatenate
        batches = list(self._numpy_batch_generator())
        column_names = [description[0] for description in self.description]
        return OrderedDict(zip(column_names, [concatenate(column) for column in zip(*batches)]))

    def fetchnumpybatches(self):
        batchgen = self._numpy_batch_generator()
        column_names = [description[0] for description in self.description]
        for next_batch in batchgen:
            yield OrderedDict(zip(column_names, next_batch))

    def _numpy_batch_generator(self):
        self._assert_valid_result_set()
        if _has_numpy_support():
            from turbodbc_numpy_support import make_numpy_result_set
        else:
            raise Error("turbodbc was compiled without numpy support. Please install "
                        "numpy and reinstall turbodbc")
        numpy_result_set = make_numpy_result_set(self.impl.get_result_set())
        first_run = True
        while True:
            result_batch = _make_masked_arrays(numpy_result_set.fetch_next_batch())
            is_empty_batch = (len(result_batch[0]) == 0)
            if is_empty_batch and not first_run:
                raise StopIteration # Let us return a typed result set at least once
            first_run = False
            yield result_batch

    def close(self):
        self.result_set = None
        self.impl = None

    def setinputsizes(self, sizes):
        """
        setinputsizes() has no effect. turbodbc automatically picks appropriate
        return types and sizes. Method exists since PEP-249 requires it.
        """
        pass

    def setoutputsize(self, size, column=None):
        """
        setoutputsize() has no effect. turbodbc automatically picks appropriate
        input types and sizes. Method exists since PEP-249 requires it.
        """
        pass
