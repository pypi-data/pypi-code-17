# encoding: utf-8
'''
utils.logutil -- log tool

utils.logutil is a log tool, which can output log information both in console and file.
the log file can be rotated while it is too large or have too many old files.

@author:     Paul Fu

@copyright:  2016 MassClouds.Inc. All rights reserved.

@contact:    fu_zkun@massclouds.com
'''

import os

import logging.handlers
from functools import wraps
import time


def __create_file(path):     
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):  # 目录不存在，则创建
        os.makedirs(dir_path)
    f = open(path, 'w')  # 创建文件
    f.close()

def init_logger(log_path="/tmp/log/test.log"):
    '''
    Initialize log for client at the entry point.
    @param log_path: file
    '''
     
    if not os.path.exists(log_path):  # 文件不存在，则创建
        __create_file(log_path)
     
    #  %(pathname)s 
    log_format = ' [ %(levelname)s ]: %(asctime)s  %(filename)s %(funcName)s line:%(lineno)d #  ' \
                 + ' %(message)s \n'

    logger = logging.getLogger()
    '''
          logging.DEBUG
          logging.INFO
          logging.WARNING
          logging.ERROR
          logging.CRITICAL
    '''
    logger.setLevel(logging.INFO)

    fh = logging.handlers.RotatingFileHandler(log_path,
                                              maxBytes=10 ** 20,
                                              backupCount=5)
    ch = logging.StreamHandler()

    fmt = logging.Formatter(fmt=log_format,
                            datefmt='%a, %d %b %Y %H:%M:%S')

    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)


def runtime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(args, kwargs)
        end = time.time()
        msg = "%s runtime is %f" %(func.__name__, end-start)
        logging.info(msg)
    return wrapper
