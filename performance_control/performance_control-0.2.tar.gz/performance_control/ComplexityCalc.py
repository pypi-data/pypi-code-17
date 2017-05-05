from performance_control.ArgData \
    import ArgData
from performance_control.PerformanceControllerException \
    import PerformanceControllerException
from performance_control.Logger \
    import logger
from performance_control.Timeout \
    import timeout, TimeoutExceededException
from timeit \
    import Timer
import math
import numpy
import copy
import sys


class ComplexityCalc:

    SCALE = 2
    TEST_RANGE = range(9, 18)
    COMPLEXITITES = {'O(logn)': lambda N: math.log(N, 2),
                     'O(nlogn)': lambda N: N * math.log(N, 2),
                     'O(n)': lambda N: N,
                     'O(n^2)': lambda N: N * N,
                     'O(n^3)': lambda N: N * N * N}

    def __init__(self, func, arg, maxtime_sec=1000, repeat=1):
        if not callable(func) \
                or ArgData not in arg.__class__.__bases__ \
                or maxtime_sec < 1 or repeat < 1:
            raise PerformanceControllerException("Invalid arguments.")

        self.test_algorithm = func
        self.test_arg = arg
        self.timeout = maxtime_sec
        self.measures = dict()
        self.complexity = None
        self.SIZES = [pow(self.SCALE, i) for i in self.TEST_RANGE]
        self.repeat = repeat
        self.constance = 1

    @logger('logs.log')
    def calculate_complexity(self):
        measures = self.get_measures()
        if not measures or len(measures) < 3:
            print('Not enough information...')
            return None
        errors = self.count_errors(measures)
        minc = ('', float('inf'), 0)
        for complexity_name, (std, mean) in errors.items():
            if std < minc[1]:
                minc = (complexity_name, std, mean)
        self.complexity = minc[0]
        self.constance = minc[2]
        return minc[0]

    # returns: dictionary N -> time
    @timeout()
    @logger('logs.log')
    def get_measures(self):
        measures = dict()
        prev = 0            # previous size
        self.test_arg.set_data(0)
        progress = 1
        try:
            for i in self.SIZES:
                for _ in range(self.repeat):
                    self.test_arg.inc_data(i - prev)
                    prev = i
                    rawdata_copy = copy.deepcopy(self.test_arg.get_raw_data())

                    print('counting for ' + str(i))
                    print(str(int(progress * 100 / len(self.TEST_RANGE)
                                  / self.repeat)) + '% progress...')

                    t = Timer(lambda: self.test_algorithm(rawdata_copy))
                    measures[i] = t.timeit(number=1)
                    progress += 1
        except TimeoutExceededException:
            print('Timeout exceeded, final result is not certain...')
        finally:
            self.measures = measures
            return measures

    # returns: dictionary COMPLEXITY -> wariancja
    def count_errors(self, measures):
        res = dict()
        for name, f in self.COMPLEXITITES.items():
            vals = []
            for N, time in measures.items():
                vals.append(time / f(N))
            res[name] = (numpy.std(vals) / numpy.mean(vals), numpy.mean(vals))
        return res

    def get_timeforecaster(self):
        if not self.complexity:
            raise PerformanceControllerException(
                "Forcaster is availible after calculating complexity."
                )

        def forecast_time(n):
            compl = self.COMPLEXITITES[self.complexity]
            res = compl(n) * self.constance
            return res
        return forecast_time

    def get_sizeforecaster(self):
        if not self.complexity:
            raise PerformanceControllerException(
                "Forcaster is availible after calculating complexity."
                )

        def forecast_size(time):

            def compl(n):
                return self.constance * self.COMPLEXITITES[self.complexity](n)
            start = 1
            end = sys.maxsize
            prev = -1
            mid = 0
            while prev != mid:
                prev = mid
                mid = int((end + start) / 2)
                if compl(mid) < time:
                    start = mid
                else:
                    end = mid

            return end
        return forecast_size
