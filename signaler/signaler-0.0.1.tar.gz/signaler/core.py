import signal


class Signaler:
    def __init__(self, signals_to_handle=[signal.SIGINT, signal.SIGUSR1]):
        if not (hasattr(signals_to_handle, '__iter__')
                and hasattr(signals_to_handle, '__len__')):
            raise ValueError("arg must be a sequence")

        self._to_handle = signals_to_handle

        self._recieved = []

        for s in signals_to_handle:
            signal.signal(s, self.handler)

    def handler(self, signum, frame):
        """
        Called when any signal

        :param signal:
        :param frame:
        """
        self._recieved.append(signum)

    def got(self, signum):
        """
        Returns True iff the signal has been received.

        :param signalval: signal number
        """
        return signum in self._recieved

    @property
    def got_sigint(self):
        return self.got(signal.SIGINT)

    @property
    def got_sigusr1(self):
        return self.got(signal.SIGUSR1)
