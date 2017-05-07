import runner
import loader
import mysolver
import logging


def mike(file_name):
    logging.basicConfig(level=logging.INFO)

    logging.info("Accessing functions...")
    source_code = loader.check_functions(file_name)
    init = source_code.init
    run = loader.measure_time(source_code.run)
    clean = source_code.clean

    logging.info("Gathering data...")
    measures = runner.get_data(init, run, clean)

    logging.info("Solving...")
    time, size = mysolver.solve(measures)
    return time, size
