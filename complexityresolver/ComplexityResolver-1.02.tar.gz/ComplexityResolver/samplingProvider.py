import algorithm
import exceptions
import consts
from threading import Thread
import functools
import logging
import time


class SamplingProvider:
    def __init__(self, timeout, nFrom, nTo):
        self.timeout = timeout
        self.samplingResult = []
        self.nFrom = nFrom
        self.nTo = nTo

    def DoSampling(self):
        try:
            samplingFunc = self.Timeout(self.timeout)(self.ExecuteSampling)
            samplingFunc()

        except exceptions.TimeoutException as exT:
            logging.info(exT)
        except Exception as err:
            raise err

        return self.samplingResult

    def Timeout(self, timeout):
        def deco(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                res = [exceptions.TimeoutException(
                    'function [%s] timeout [%s seconds] exceeded!'
                    % (func.__name__, timeout))]

                def newFunc():
                    try:
                        res[0] = func(*args, **kwargs)
                    except Exception as e:
                        res[0] = e
                t = Thread(target=newFunc)
                t.daemon = True
                try:
                    t.start()
                    t.join(timeout)
                except Exception as je:
                    logging.error('Error starting thread')
                    raise je
                ret = res[0]
                if isinstance(ret, BaseException):
                    raise ret
                return ret
            return wrapper
        return deco

    def ExecuteSampling(self):
        currentN = self.nFrom

        while(currentN <= self.nTo):
            logging.info("Start sampling with N = %d", currentN)
            alg = algorithm.Algorithm(currentN)

            start = time.time()
            alg.Execute()
            end = time.time()

            alg.Clean()

            self.samplingResult.append({"N": currentN, "time": (end - start)})
            logging.info("Execution time: %f ms", (end - start) * 1000.0)

            currentN *= consts.SAMPLING_CHANGE
