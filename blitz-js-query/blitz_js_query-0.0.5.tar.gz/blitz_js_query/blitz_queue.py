import time
from promise import Promise
from threading import Timer


def queue_promise_shift(self, resolve, reject):
    self.length -= 1
    resolve(None)


def queue_promise_timer(self, resolve, reject, now, next_shift):
    # Get current expected interval resolution
    if not self.next_shift_at:
        current_shift = 0
    else:
        current_shift = self.next_shift_at - now

    # Finished while waiting for next interval -> repeat
    if current_shift > next_shift:
        self.throttle().then(lambda res: queue_promise_shift(self, resolve, reject))
    # Finished without waiting for interval
    else:
        self.length -= 1
        resolve(None)


def queue_promise(self, resolve, reject):
    now = time.time() * 1000

    # Set time until next interval
    if not self.next_shift_at:
        next_shift = 0
    else:
        next_shift = self.next_shift_at - now

    # Check time between now and next available call
    until_next_shift = now - self.next_created_at - next_shift

    # Set new last request date
    self.next_created_at = now

    # Calculate waiting delay
    delay = self.length * self.delay_diff + next_shift

    # Min diff is met
    if until_next_shift > self.delay_diff:
        resolve(None)
    # Otherwise, wait for delay difference
    else:
        self.length += 1

        # Resolve promise & sub ongoing
        t = Timer(delay/1000, queue_promise_timer, args=(self, resolve, reject, now, next_shift,))
        t.start()


def delay_promise_timer(self, resolve, reject):
    self.next_shift_at = 0
    resolve(None)


def delay_promise(self, resolve, reject, delay):
    self.next_shift_at = time.time() + delay

    t = Timer(delay/1000, delay_promise_timer, args=(self, resolve, reject,))
    t.start()


class Queue:
    """
    Set queue timings
    """
    def __init__(self, options):
        # Delay timers
        if options.get('ignore_limiter'):
            self.delay_diff = 0
            self.delay_max = 0
        # Token provided
        elif options.get('user_key'):
            self.delay_diff = 850
            self.delay_max = 10000
        # No token
        else:
            self.delay_diff = 1100
            self.delay_max = 10000

        # Queue counter (Objects in queue)
        self.length = 1

        # Queue states
        self.next_created_at = 0
        self.next_shift_at = 0

    """
    Make sure limiter isn't triggered since last request
    """
    def throttle(self):
        return Promise(lambda resolve, reject: queue_promise(self, resolve, reject))

    """
    Manages interval delays for rate limiting (coupled with self.throttle())
    """
    def delay(self, delay):
        return Promise(lambda resolve, reject: delay_promise(self, resolve, reject, delay))
