"""Holds utility functions useful in a variety of situations"""
import logging

LOGGER = logging.getLogger(__name__)

def find_function(func_path):
    '''Searches for and returns a function if it exists'''
    LOGGER.debug("Searching for function %s", func_path)
    paths = func_path.split(':')
    module = __import__(''.join(paths[:-1]), fromlist=['.'.join(paths[1:])])
    func = getattr(module, paths[-1])

    return func
