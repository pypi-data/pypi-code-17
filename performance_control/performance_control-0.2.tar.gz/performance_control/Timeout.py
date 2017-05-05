import signal

#   This is a decorator that timeouts methods
#   A class has to have defined a field called "timeout"


class TimeoutExceededException(Exception):
    pass


def timeout():
    def real_dec(func):
        def alarm_handle(signo, info):
            raise TimeoutExceededException

        def timeouted_func(*args, **kwargs):
            sec = args[0].timeout
            signal.signal(signal.SIGALRM, alarm_handle)
            signal.alarm(sec)
            try:
                res = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return res
        return timeouted_func
    return real_dec
