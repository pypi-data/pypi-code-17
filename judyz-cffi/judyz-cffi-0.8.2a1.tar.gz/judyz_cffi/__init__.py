"""
CFFI loader for Judy.
"""


def load():
    global _ffi, _cjudy
    import ctypes.util
    from _judy_cffi import ffi
    cjudy = ffi.dlopen(ctypes.util.find_library("Judy"))
    _ffi, _cjudy = ffi, cjudy

load()


class JudyError(Exception):
    """Judy error.
    """

    _msgs = [
        "None",
        "Full",
        "Out of Memory",
        "Null PPArray",
        "Null PIndex",
        "Not a Judy1",
        "Not a JudyL",
        "Not a JudySL",
        "Overrun",
        "Corruption",
        "Non-Null PPArray",
        "Null PValue",
        "Unsorted Indexes",
    ]

    def __init__(self, errno):
        super(JudyError, self).__init__()
        if 0 <= errno < len(JudyError._msgs):
            self.message = JudyError._msgs[errno]
        else:
            self.message = "Error {}".format(errno)

    def __str__(self):
        return self.message


class Judy1Iterator(object):
    def __init__(self, j):
        self._j = j
        self._array = j._array
        self._start = True
        self._index = _ffi.new("signed long*")

    def __iter__(self):
        return self

    def next(self):
        err = _ffi.new("JError_t *")
        if self._start:
            rc = _cjudy.Judy1First(self._array[0], self._index, err)
            self._start = False
        else:
            rc = _cjudy.Judy1Next(self._array[0], self._index, err)
        if rc == 0:
            raise StopIteration()
        if rc == -1:
            raise JudyError(err.je_Errno)
        return self._index[0]


class Judy1(object):
    """
    Judy1 class.
    """

    def __init__(self, iterable=None):
        self._array = _ffi.new("Judy1 **")
        if iterable:
            for item in iterable:
                self.add(item)

    def add(self, item):
        err = _ffi.new("JError_t *")
        if _cjudy.Judy1Set(self._array, item, err) == -1:
            raise JudyError(err.je_Errno)

    def clear(self):
        err = _ffi.new("JError_t *")
        if _cjudy.Judy1FreeArray(self._array, err) == -1:
            raise JudyError(err.je_Errno)

    def _get(self, item):
        err = _ffi.new("JError_t *")
        rc = _cjudy.Judy1Test(self._array[0], item, err)
        if rc == -1:
            raise JudyError(err.je_Errno)
        return rc

    def __contains__(self, item):
        return self._get(item)

    def __len__(self):
        err = _ffi.new("JError_t *")
        rc = _cjudy.Judy1Count(self._array[0], 0, -1, err)
        if rc == -1:
            raise JudyError(err.je_Errno)
        return rc

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def discard(self, item):
        err = _ffi.new("JError_t *")
        rc = _cjudy.Judy1Unset(self._array, item, err)
        if rc == -1:
            raise JudyError(err.je_Errno)

    def remove(self, item):
        err = _ffi.new("JError_t *")
        rc = _cjudy.Judy1Unset(self._array, item, err)
        if rc == 0:
            raise KeyError(item)
        if rc == -1:
            raise JudyError(err.je_Errno)

    def __iter__(self):
        return Judy1Iterator(self)


class JudyLIterator(object):
    def __init__(self, j):
        self._j = j
        self._array = j._array
        self._start = True
        self._index = _ffi.new("signed long*")

    def __iter__(self):
        return self

    def next(self):
        err = _ffi.new("JError_t *")
        if self._start:
            p = _cjudy.JudyLFirst(self._array[0], self._index, err)
            self._start = False
        else:
            p = _cjudy.JudyLNext(self._array[0], self._index, err)
        if p == _ffi.NULL:
            raise StopIteration()
        if p == JudyL.M1:
            raise JudyError(err.je_Errno)
        v = _ffi.cast("signed long", p[0])
        return self._index[0], int(v)


class JudyL(object):
    """
    JudyL class.
    """
    M1 = _ffi.cast("void*", -1)

    def __init__(self, other=None):
        self._array = _ffi.new("JudyL **")
        if other:
            self.update(other)

    def update(self, other):
        if other is None:
            return
        has_keys = True
        try:
            other.keys
        except AttributeError:
            has_keys = False
        if has_keys:
            for key in other:
                self[key] = other[key]
        else:
            for (k, v) in other:
                self[k] = v

    def clear(self):
        err = _ffi.new("JError_t *")
        if _cjudy.JudyLFreeArray(self._array, err) == -1:
            raise JudyError(err.je_Errno)

    def __len__(self):
        err = _ffi.new("JError_t *")
        rc = _cjudy.JudyLCount(self._array[0], 0, -1, err)
        if rc == -1:
            raise JudyError(err.je_Errno)
        return rc

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def __setitem__(self, key, value):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLIns(self._array, key, err)
        if p == _ffi.NULL:
            raise JudyError(err.je_Errno)
        p[0] = _ffi.cast("void*", value)

    def __getitem__(self, item):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLGet(self._array[0], item, err)
        if p == _ffi.NULL:
            raise KeyError(item)
        if p == JudyL.M1:
            raise JudyError(err.je_Errno)
        return int(_ffi.cast("signed long", p[0]))

    def __contains__(self, item):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLGet(self._array[0], item, err)
        if p == JudyL.M1:
            raise JudyError(err.je_Errno)
        return p != _ffi.NULL

    def get(self, item, default_value=0):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLGet(self._array[0], item, err)
        if p == _ffi.NULL:
            return default_value
        if p == JudyL.M1:
            raise JudyError(err.je_Errno)
        return int(_ffi.cast("signed long", p[0]))

    def inc(self, key, value=1):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudyLIns(self._array, key, err)
        if p == _ffi.NULL:
            raise JudyError(err.je_Errno)
        p[0] = int(_ffi.cast("signed long", p[0])) + _ffi.cast("void*", value)

    def __iter__(self):
        return JudyLIterator(self)

    def iteritems(self):
        err = _ffi.new("JError_t *")
        index = _ffi.new("signed long*")
        p = _cjudy.JudyLFirst(self._array[0], index, err)
        if p == JudyL.M1:
            raise Exception("err={}".format(err.je_Errno))
        if p == _ffi.NULL:
            return
        v = int(_ffi.cast("signed long", p[0]))
        yield index[0], v
        while 1:
            p = _cjudy.JudyLNext(self._array[0], index, err)
            if p == JudyL.M1:
                raise Exception("err={}".format(err.je_Errno))
            if p == _ffi.NULL:
                break
            v = int(_ffi.cast("signed long", p[0]))
            yield index[0], v

    def keys(self):
        err = _ffi.new("JError_t *")
        index = _ffi.new("signed long*")
        p = _cjudy.JudyLFirst(self._array[0], index, err)
        if p == JudyL.M1:
            raise Exception("err={}".format(err.je_Errno))
        if p == _ffi.NULL:
            return
        yield index[0]
        while 1:
            p = _cjudy.JudyLNext(self._array[0], index, err)
            if p == JudyL.M1:
                raise Exception("err={}".format(err.je_Errno))
            if p == _ffi.NULL:
                break
            yield index[0]


class StringCache(object):
    MAX_BUILDER_SIZE = 360
    buf = None

    @staticmethod
    def acquire(capacity):
        """Acquire a buffer of a particular size.

        If we've got one in cache, returns it.
        """
        if capacity <= StringCache.MAX_BUILDER_SIZE:
            b = StringCache.buf
            if b is not None:
                if capacity <= len(b):
                    StringCache.buf = None
                    b[0] = 0
                    return b
        return _ffi.new("unsigned char[%d]" % capacity)

    @staticmethod
    def release(buf):
        """Release the buffer.

        It must not be used thereafter.
        """
        if len(buf) <= StringCache.MAX_BUILDER_SIZE:
            StringCache.buf = buf


class JudySLIterator(object):
    _STATE_FIRST = 0
    _STATE_NEXT = 1
    _STATE_END = 2

    def __init__(self, j):
        self._j = j
        self._array = j._array
        self._state = JudySLIterator._STATE_FIRST
        self._index = StringCache.acquire(j._max_len)

    def __iter__(self):
        return self

    def next(self):
        err = _ffi.new("JError_t *")
        if self._state == JudySLIterator._STATE_FIRST:
            p = _cjudy.JudySLFirst(self._array[0], self._index, err)
            self._state = JudySLIterator._STATE_NEXT
        elif self._state == JudySLIterator._STATE_NEXT:
            p = _cjudy.JudySLNext(self._array[0], self._index, err)
        else:
            raise StopIteration()
        if p == _ffi.NULL:
            StringCache.release(self._index)
            self._state = JudySLIterator._STATE_END
            raise StopIteration()
        if p == JudySL.M1:
            raise JudyError(err.je_Errno)
        v = _ffi.cast("signed long", p[0])
        return _ffi.string(self._index), int(v)


class JudySL(object):
    """
    JudySL class.
    """
    M1 = _ffi.cast("void*", -1)

    def __init__(self, other=None):
        self._array = _ffi.new("JudySL **")
        self._max_len = 1
        if other:
            self.update(other)

    def update(self, other):
        if other is None:
            return
        has_keys = True
        try:
            other.keys
        except AttributeError:
            has_keys = False
        if has_keys:
            for key in other:
                self[key] = other[key]
        else:
            for (k, v) in other:
                self[k] = v

    def clear(self):
        err = _ffi.new("JError_t *")
        if _cjudy.JudySLFreeArray(self._array, err) == -1:
            raise JudyError(err.je_Errno)

    def __len__(self):
        n = 0
        for k, v in self.iteritems():
            n += 1
        return n

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def __setitem__(self, key, value):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudySLIns(self._array, key, err)
        if p == _ffi.NULL:
            raise JudyError(err.je_Errno)
        p[0] = _ffi.cast("void*", value)
        klen = len(key) + 1
        if self._max_len < klen:
            self._max_len = klen

    def inc(self, key):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudySLIns(self._array, key, err)
        if p == _ffi.NULL:
            raise JudyError(err.je_Errno)
        p[0] = _ffi.cast("void*", int(_ffi.cast("long", p[0])) + 1)
        klen = len(key) + 1
        if self._max_len < klen:
            self._max_len = klen

    def __getitem__(self, item):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudySLGet(self._array[0], item, err)
        if p == _ffi.NULL:
            raise KeyError(item)
        if p == JudySL.M1:
            raise JudyError(err.je_Errno)
        return int(_ffi.cast("signed long", p[0]))

    def __contains__(self, item):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudySLGet(self._array[0], item, err)
        if p == JudySL.M1:
            raise JudyError(err.je_Errno)
        return p != _ffi.NULL

    def get(self, item, default_value=0):
        err = _ffi.new("JError_t *")
        p = _cjudy.JudySLGet(self._array[0], item, err)
        if p == _ffi.NULL:
            return default_value
        if p == JudySL.M1:
            raise JudyError(err.je_Errno)
        return int(_ffi.cast("signed long", p[0]))

    def __iter__(self):
        return JudySLIterator(self)

    def iteritems(self):
        err = _ffi.new("JError_t *")
        index = StringCache.acquire(self._max_len)  # _ffi.new("char[%d]" % self._max_len)
        try:
            p = _cjudy.JudySLFirst(self._array[0], index, err)
            if p == JudySL.M1:
                raise Exception("err={}".format(err.je_Errno))
            if p == _ffi.NULL:
                return
            v = int(_ffi.cast("signed long", p[0]))
            yield _ffi.string(index), v
            while 1:
                p = _cjudy.JudySLNext(self._array[0], index, err)
                if p == JudySL.M1:
                    raise Exception("err={}".format(err.je_Errno))
                if p == _ffi.NULL:
                    break
                v = int(_ffi.cast("signed long", p[0]))
                yield _ffi.string(index), v
        finally:
            StringCache.release(index)

    def keys(self):
        for k, v in self.iteritems():
            yield k

    def get_first(self, buf=None):
        """
        Get the first item in the JudySL
        :param buf: None...
        :return: (key, value, internal "iterator" for get_next) or (None, None, None)
        :rtype: tuple
        """
        err = _ffi.new("JError_t *")
        if buf is None:
            buf = StringCache.acquire(self._max_len)
        p = _cjudy.JudySLFirst(self._array[0], buf, err)
        if p == JudySL.M1:
            StringCache.release(buf)
            raise Exception("err={}".format(err.je_Errno))
        if p == _ffi.NULL:
            StringCache.release(buf)
            return None, None, None
        v = int(_ffi.cast("signed long", p[0]))
        return _ffi.string(buf), v, buf

    def get_next(self, buf):
        """
        Get the next item in the JudySL
        :param buf: internal "iterator" returned by get_first or get_next
        :type buf:
        :return: (key, value, internal "iterator" for get_next) or (None, None, None)
        :rtype: tuple
        """
        if buf is None:
            return None, None, None
        err = _ffi.new("JError_t *")
        p = _cjudy.JudySLNext(self._array[0], buf, err)
        if p == JudySL.M1:
            StringCache.release(buf)
            raise Exception("err={}".format(err.je_Errno))
        if p == _ffi.NULL:
            StringCache.release(buf)
            return None, None, None
        v = int(_ffi.cast("signed long", p[0]))
        return _ffi.string(buf), v, buf
