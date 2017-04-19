# -*- coding: utf-8 -*-

import functools

from .profile import StatementProfiler


def sqlprofile(engine,
               count=-1, insert=-1, update=-1, select=-1, delete=-1,
               seq=None):
    def _sqlprofile(func):
        @functools.wraps(func)
        def __sqlprofile(*args, **kwargs):

            with StatementProfiler(engine) as profiler:
                ret = func(*args, **kwargs)

            if count != -1:
                msg = 'Number of total SQL statements do not match (expect:{0} actual:{1})'  # noqa
                assert profiler.count == count, msg.format(count,
                                                           profiler.count)

            if insert != -1:
                msg = 'Number of INSERT SQL statements do not match (expect:{0} actual:{1})'  # noqa
                assert profiler.insert == insert, msg.format(insert,
                                                             profiler.insert)

            if update != -1:
                msg = 'Number of UPDATE SQL statements do not match (expect:{0} actual:{1})'  # noqa
                assert profiler.update == update, msg.format(update,
                                                             profiler.update)

            if delete != -1:
                msg = 'Number of DELETE SQL statements do not match (expect:{0} actual:{1})'  # noqa
                assert profiler.delete == delete, msg.format(delete,
                                                             profiler.delete)

            if seq is not None:
                fmt = 'Unexpected statement found (expect: {0}, actual: {1})'
                msg = fmt.format(seq.upper(), profiler.sequence.upper())
                assert profiler.sequence.upper() == seq.upper(), msg

            return ret
        return __sqlprofile
    return _sqlprofile
