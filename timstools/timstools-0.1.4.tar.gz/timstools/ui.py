import threading
from functools import wraps
import time
import sched
import _thread as thread

def rate_limited(max_per_second, mode='wait', delay_first_call=False):
    """
    Decorator that make functions not be called faster than
    set mode to 'kill' to just ignore requests that are faster than the
    rate.
set mode to 'refresh_timer' to reset the timer on successive calls TODO

    set delay_first_call to True to delay the first call as well
    """
    assert mode in ('wait', 'kill', 'refresh_timer')
    lock = threading.Lock()
    min_interval = 1.0 / float(max_per_second)
    def decorate(func):
        last_time_called = [0.0] # TODO differentiate betwenen last_time_run and this
        last_time_run = [0.0]
        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            def run_func():
                lock.release()
                ret = func(*args, **kwargs)
                last_time_called[0] = time.time()
                return ret
            lock.acquire()
            elapsed = time.time() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            # import pdb;pdb.set_trace()
            nonlocal delay_first_call
            if delay_first_call:
                delay_first_call = False
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                    return run_func()
                else:
                    return run_func()
            else:
                # Allows the first interval to not have to wait
                # if not last_time_called[0] or elapsed > min_interval:
                if elapsed > min_interval:
                    return run_func()
                elif left_to_wait > 0:
                    if mode == 'wait':
                        time.sleep(left_to_wait)
                        return run_func()
                    elif mode == 'kill':
                        lock.release()
                        return
                    elif mode == 'refresh_timer':
                        # lock.release()
                        last_time_called[0] = time.time()
                        import pdb;pdb.set_trace()
                        # return run_func()


        return rate_limited_function
    return decorate

def delay_call(seconds):
    '''Decorator to delay the runtime of your function,
    each succesive call to function will refresh the timer,
    canceling any previous functions
    '''
    my_scheduler = sched.scheduler(time.perf_counter, time.sleep)
    def delayed_func(func): # this gets passed the function!
        def modded_func(*args, **kwargs):
            if len(my_scheduler.queue) == 1:
                my_scheduler.enter(seconds, 1, func, args, kwargs)
                my_scheduler.cancel(my_scheduler.queue[0])
            else:
                my_scheduler.enter(seconds, 1, func, args, kwargs)
                thread.start_new_thread(my_scheduler.run, ())
        thread.start_new_thread(my_scheduler.run, ())
        modded_func.scheduler = my_scheduler
        return modded_func
    return delayed_func

if __name__ == "__main__":
    @rate_limited(2, mode='wait') # 2 per second at most
    def print_num_wait(num):
        print (num)

    @rate_limited(2, mode='kill')
    def print_num_kill(num):
        print(num)

    @rate_limited(10000, mode='kill', delay_first_call=True)
    def print_num_kill_delay(num):
        print(num)

    @rate_limited(1/3, mode='wait', delay_first_call=True)
    def print_num_wait_delay(num):
        print(num)

    @rate_limited(2, mode='refresh_timer')
    def print_num_refresh(num):
        print(num)

    @rate_limited(2, mode='refresh_timer', delay_first_call=True)
    def print_num_refresh_delay(num):
        print(num)

    # @delay_call(1)
    # def print_num_wait_refresh(num):
        # print(num)
    # print('Rate limited at 2 per second at most')
    # print()
    # print("Mode is Kill")
    # print("1 000 000 print requests sent to decorated function")
    # for i in range(1,1000000):
        # print_num_kill(i)

    # print()
    # print('Mode is Wait - default')
    # print("10 print requests sent to decorated function")
    # for i in range(1,11):
        # print_num_wait(i)

    # print()
    # print('Mode is Kill with Delay on first request')
    # print("1 000 000 print requests sent to decorated function")
    # for i in range(1, 1000000):
        # print_num_kill_delay(i)

    # print()
    # print('Mode is Wait with Delay on first request')
    # print("5 print requests sent to decorated function")
    # for i in range(1, 6):
        # print_num_wait_delay(i)
    # print()

    print('Mode is refresh_timer')
    print("100 000 print requests sent to decorated function")
    for i in range(1,100001):
        print_num_refresh(i)
    print('Finished Printing')
    # time.sleep(1.5)
    # print('a second try should also work')
    # for i in range(1,100001):
        # print_num_wait_refresh(i)
    # print('Finished Printing')

    while 1:
        time.sleep(0.5)

