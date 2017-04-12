# -*- coding:utf-8 -*-
import sys
import logging
import editdistance


def calc_str_distance(command, candidate):
    """ Calculates the distance between two strings
        ref: Levenshtein Distance
    """
    return editdistance.eval(command, candidate)


def guess(command, candidates):
    holy_table = {}
    for candidate in candidates:
        holy_table[candidate] = calc_str_distance(command, candidate)
    sorted_command = sorted(holy_table.iteritems(), key=lambda (k,v): (v,k))
    return sorted_command[0][0]


def create_logger(app_name):
    """Creates a logger for the given application.
    """
    _logger = logging.getLogger(app_name)
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    file_handler = logging.FileHandler("{}.log".format(app_name))
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    _logger.setLevel(logging.INFO)
    # print log to file and console
    _logger.addHandler(stream_handler)
    _logger.addHandler(file_handler)
    return _logger

if __name__ == '__main__':
    pass
