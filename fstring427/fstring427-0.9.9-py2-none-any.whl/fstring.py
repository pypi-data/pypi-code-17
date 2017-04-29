# Copyright (c) 2017 Smartvid.io
"""String formatter this is similar to that found in: https://www.python.org/dev/peps/pep-0498/"""
import sys
import inspect

from string import Formatter


class Fmt(Formatter):
    _parsed_cache = {}
    _compiled_cache = {}
    hits = 0
    misses = 0
    c_hits = 0
    c_misses = 0
    calls = 0
    caching = True
    compile_caching = True

    @classmethod
    def _reset(cls, caching=True, compile_caching=True):
        cls.caching = caching
        cls.compile_caching = compile_caching
        cls._parsed_cache = {}
        cls._compiled_cache = {}
        cls.hits = cls.misses = cls.calls = cls.c_hits = cls.c_misses = 0

    def _parse_format(self, s):
        if not self.caching:
            Fmt.misses += 1
            return list(self.parse(s))
        # Caching the format parse at the beginning saves 85% on repeated calls
        _parsed = Fmt._parsed_cache.get(s, None)
        if _parsed is None:
            Fmt.misses += 1
            Fmt._parsed_cache[s] = _parsed = list(self.parse(s))
        else:
            Fmt.hits += 1
        return _parsed

    def _compile_field(self, field_name):
        if not self.compile_caching:
            return compile(field_name, "-", 'eval')
        compiled = Fmt._compiled_cache.get(field_name)
        if compiled is None:
            Fmt.c_misses += 1
            compiled = Fmt._compiled_cache[field_name] = compile(field_name, "-", 'eval')
        else:
            Fmt.c_hits += 1
        return compiled

    def __init__(self, s, *args, **kwargs):
        super(Fmt, self).__init__(*args, **kwargs)
        self.format_string = s
        self._parsed = self._parse_format(s)

    def __call__(self, *args, **kwargs):
        Fmt.calls += 1
        __lookback = kwargs.pop("__lookback", 1)
        if not self.format_string:
            return str(kwargs)
        d = {}
        frame = inspect.currentframe()
        try:
            while __lookback > 0:
                __lookback -= 1
                frame = frame.f_back
            d.update(frame.f_locals)
            d.update(kwargs)
            result = []
            used_args = set([])
            for literal_text, field_name, format_spec, conversion in self._parsed:
                if literal_text:
                    result.append(literal_text)
                if field_name is not None:
                    try:
                        obj, arg_used = self.get_field(field_name, args, d)
                        used_args.add(arg_used)
                    except:
                        compiled = self._compile_field(field_name)
                        obj = eval(compiled,frame.f_globals,d)
                    obj = self.convert_field(obj, conversion)
                    format_spec = self._vformat(format_spec, args, d,
                                                used_args, 1)
                    result.append(self.format_field(obj, format_spec))
            return ''.join(result)
        finally:
            del frame
            del d

    @classmethod
    def showstat(cls, stream=None):
        if stream is None:
            stream = sys.stderr
        ncached = len(cls._parsed_cache)
        print >> stream, "Fmt: calls={cls.calls} hits={cls.hits} misses={cls.misses} compile_hits={cls.c_hits} compile_misses={cls.c_misses}".format(**locals())

    def __str__(self):
        return self(__lookback=2)

    # Can also evaluate with `fmt`
    __repr__ = __str__

f = Fmt

def printf(*args, **kwargs):
    if not 1 <= len(args) <= 2:
        raise RuntimeError("printf needs a format string")
    def like_file(obj):
        return hasattr(obj, "write")
    outf = sys.stdout
    if kwargs.has_key("file") and like_file(kwargs["file"]):
        format_string = args[0]
        outf = kwargs["file"]
    elif len(args) == 1:
        format_string = args[0]
    elif len(args) == 2:
        if not like_file(args[0]):
            raise RuntimeError("'%s' not a file" % args[0])
        outf = args[0]
        format_string = args[1]
    f = Fmt(format_string)
    print >>outf, f(__lookback=2,**kwargs)

