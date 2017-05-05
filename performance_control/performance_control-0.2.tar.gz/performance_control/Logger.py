import logging
import sys


def logger(filename):
    def real_dec(function):
        def new_func(*args, **kwargs):

            sys.stdout = open(filename, 'a')

            if str(function.__name__) != '__repr__':
                logging.basicConfig(filename=filename, level=logging.DEBUG)

                if str(function.__name__) == '__init__':
                    logging.info('Instantiating object of class ' +
                                 str(args[0]) +
                                 ' with arguments: ' + str(args[1:]))
                else:
                    logging.info('Function ' + str(function.__name__) +
                                 ' starts with arguments: ' + str(args))

            try:
                res = function(*args, **kwargs)
            except Exception as e:
                logging.warning('Exception was caught: ' + str(e))
                raise e

            logging.info('Function ' + str(function.__name__) +
                         'finished successfully...')
            return res
        return new_func
    return real_dec
