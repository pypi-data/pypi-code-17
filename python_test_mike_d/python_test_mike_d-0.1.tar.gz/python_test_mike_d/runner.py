from timeit import default_timer
import logging


TIMEOUT = 5
STEP = 10


# Runs the algorithm and returns the data size and time taken
def run_algorithm(init, run, clean, n):
    c = init(n)
    measure = [n, run(c)]
    clean(c)
    return measure


# Takes $TIMEOUT seconds to get as much data as possible
def get_data(init, run, clean):

    measures = []
    n = 1
    start = default_timer()
    end = default_timer()

    while (end - start) < TIMEOUT and n <= 10000000:
        logging.info("Gathering data for size " + str(n))

        measure = run_algorithm(init, run, clean, n)
        measures.append(measure)
        end = default_timer()
        n *= STEP

    return measures

