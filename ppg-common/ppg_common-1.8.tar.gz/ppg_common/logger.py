import logging


def configure_logging(logger_name, file_name, level=logging.DEBUG,
                      sys_log=False):
    """
    Function for creating logger
    :param logger_name: Name of wanted logger to be displayed in logg. 
    Recommended value is logger = logging.getLogger(__name__) 
    :param file_name: Name of file on disk where log will be saved
    :param level: logging level - INFO, DEBUG...
    :param sys_log: Flag for system log
    :return: logger object
    """
    if sys_log:
        file_name = 'sys.log'
        mode = 'a'
    else:
        file_name = '{}.log'.format(file_name)
        mode = 'w'
    log_formatter = logging.Formatter('%(asctime)s %(module)s:%('
                                      'levelno)s'' %('
                                      'levelname)s'' %(message)s')

    handler = logging.FileHandler(file_name, mode)
    handler.setFormatter(log_formatter)
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
