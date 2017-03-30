# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import errno, itertools, select, subprocess, sys, time

from . import encode, ffprobe
from ... import module
from ...encoding import string_types
from ...subprocess import kill, make_async, raw_cmd, to_args_list

_all = module.All(globals())


class FFmpeg(object):
    """
    Encode a set of input files input to a set of output files and yields statistics about the encoding.
    """

    executable = 'ffmpeg'
    ffprobe_class = ffprobe.FFprobe
    statistics_class = encode.EncodeStatistics

    def __init__(self, executable=None, chunk_read_timeout=0.5, encode_poll_delay=0.5, encoding='utf-8'):
        self.executable = executable or self.executable
        self.chunk_read_timeout = chunk_read_timeout
        self.encode_poll_delay = encode_poll_delay
        self.encoding = encoding
        self.ffprobe = self.ffprobe_class()

    def __call__(self, *arguments):
        """Call FFmpeg with given arguments (connect stderr to a PIPE)."""
        return raw_cmd(itertools.chain([self.executable], arguments), stderr=subprocess.PIPE, universal_newlines=True)

    def encode(self, inputs, outputs, options=None, create_directories=True, process_poll=True, process_kwargs=None,
               statistics_kwargs=None):
        """
        Encode a set of input files input to a set of output files and yields statistics about the encoding.
        """
        arguments, inputs, outputs, options = self._get_arguments(inputs, outputs, options)

        # Create outputs directories
        if create_directories:
            for output in outputs:
                output.create_directory()

        statistics = self.statistics_class(inputs, outputs, options, **(statistics_kwargs or {}))
        process = self._get_process(arguments, **(process_kwargs or {}))
        try:
            yield statistics.start(process)
            while True:
                chunk = self._get_chunk(process)
                yield statistics.progress(chunk or '')
                if process_poll:
                    returncode = process.poll()
                    if returncode is not None:
                        break
                if self.encode_poll_delay:
                    time.sleep(self.encode_poll_delay)
            yield statistics.end(returncode)
        except Exception as exception:
            tb = sys.exc_info()[2]
            kill(process)
            raise exception.with_traceback(tb) if hasattr(exception, 'with_traceback') else exception

    def _clean_medias_argument(self, value):
        """
        Return a list of Media instances from passed value. Value can be one or multiple instances of string or Media.
        """
        values = [value] if isinstance(value, (string_types, self.ffprobe.media_class)) else value
        return [self.ffprobe.to_media(v) for v in values] if values else []

    def _get_arguments(self, inputs, outputs, options=None):
        """
        Return the arguments for the encoding process.

        * Set inputs to one or multiple strings (paths) or Media instances (with options).
        * Set outputs to one or multiple strings (paths) or Media instances (with options).
        * Set options to a string or a list with the options to put in-between the inputs and outputs (legacy API).

        In return you will get a tuple with (arguments, inputs -> list Media, outputs -> list Media, options -> list).
        """
        inputs = self._clean_medias_argument(inputs)
        outputs = self._clean_medias_argument(outputs)
        options = to_args_list(options)
        args = [self.executable, '-y']
        for the_input in inputs:
            args.extend(the_input.to_args(is_input=True))
        args.extend(options)
        for output in outputs:
            args.extend(output.to_args(is_input=False))
        return args, inputs, outputs, options

    def _get_chunk(self, process):
        select.select([process.stderr], [], [], self.chunk_read_timeout)
        try:
            chunk = process.stderr.read()
            return chunk if chunk is None or isinstance(chunk, string_types) else chunk.decode(self.encoding)
        except IOError as e:
            if e.errno != errno.EAGAIN:
                raise

    def _get_process(self, arguments, **process_kwargs):
        """Return an encoding process with stderr made asynchronous."""
        process = raw_cmd(arguments, stderr=subprocess.PIPE, close_fds=True, **process_kwargs)
        make_async(process.stderr)
        return process

__all__ = _all.diff(globals())
