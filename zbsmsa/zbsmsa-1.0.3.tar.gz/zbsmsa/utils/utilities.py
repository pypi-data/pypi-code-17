"""
Written by: Ian Doarn

Basic utilities for 
use in other modules
"""
import json
import os
import re
from zbsmsa.utils.exceptions import InvalidRange

PATH = os.path.dirname(os.path.realpath(__file__))

def concat_selectors(*args, concat=''):
    """
    Combines strings, since some selectors 
    paths and variable names when combines 
    are MUCH longer than 127 chars
    
    :param args: Variable amount of strings to combine
    :return: combined string
    """
    return concat.join(args)

def load_selectors(file, path=os.path.join(PATH, 'json')):
    """
    Load css selector json file into python
    :param file: json file
    :param path: path to json files, default @ zbsmsa/utils/json
    :return: selectors
    """
    with open(os.path.join(path, file), 'r')as f:
        data = json.load(f)
    f.close()
    return data

def get_range_from_results(results):
    """
    Get min and max range of table from results
    at the end of table
    
    When SMS tells you how many results there are, it
    usually looks like:
        
        1 - 25 of 25
        
    This uses regex to ensure the results are formatted this way
    it then split the text on the 'of' and again on the '-'
    We can then get the min and max range to use when iterating a table
    
    If the regex match returns false, we raise an error saying that
    the results passed in are invalid
    
    :param results: String from site
    :return: min value, max value
    """
    # TODO: Add exception for "No records" result

    if results == 'Loading...':
        raise InvalidRange(results, msg='Results still loading.')

    if results == '1-1 of 1':
        return 1, 1

    if results == '1-100 of 100+':
        raise InvalidRange(results, msg="Range to large.")

    if results == 'No records':
        raise InvalidRange(results, msg='No records.')

    pattern = re.compile(r"(?:(?P<min>\d{1,3})-(?P<max>\d{1,3})\s(?P<of>of)\s(?P=max))")
    if bool(pattern.match(results)):
        search_range = results.split('of')[0].split('-')
        return int(search_range[0].replace(' ','')), int(search_range[1].replace(' ',''))
    else:
        raise InvalidRange(results)
