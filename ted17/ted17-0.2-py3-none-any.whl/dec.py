# -*- coding: utf-8 -*-
import decimal
from collections import OrderedDict
import textwrap


def isNum(val):  # is val number or not ?
    """Check if val is number or not

    :param val: value to check
    :return: Boolean
    """
    try:
        float(val)
    except ValueError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """
    Always returns a decimal number. If poso is not a number or None
    returns dec(0)

    :param poso: Mumber in any format (string, float, int, ...)
    :param decimals: Number of decimals (default 2)
    :return: A decimal number rounded to decimals parameter
    """
    if poso is None:
        poso = 0
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(poso)
    else:
        tmp = decimal.Decimal('0')
    # in case of tmp = -0.00 to remove negative sign
    if tmp == decimal.Decimal(0):
        tmp = decimal.Decimal(0)
    return tmp.quantize(PLACES)


def triades(txt, separator='.'):
    '''
    Help function to split digits to thousants ( 123456 becomes 123.456 )
    '''
    return separator.join(textwrap.wrap(txt[::-1], 3))[::-1]


def dec2gr(poso, decimals=2, zero_as_space=False):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    dposo = dec(poso, decimals)
    if dposo == dec(0):
        if zero_as_space:
            return ' '
    sdposo = str(dposo)
    meion = '-'
    separator = '.'
    decimal_ceparator = ','
    prosimo = ''
    if sdposo.startswith(meion):
        prosimo = meion
        sdposo = sdposo.replace(meion, '')
    if '.' in sdposo:
        sint, sdec = sdposo.split('.')
    else:
        sint = sdposo
        decimal_ceparator = ''
        sdec = ''
    return prosimo + triades(sint) + decimal_ceparator + sdec


def gr2dec(poso):
    '''
    Returns decimal (12.345,67 becomes 12345.67)
    '''
    st = poso.replace('.', '')
    ds = st.replace(',', '.')
    return dec(ds)


class Ddict(dict):

    '''
    Dictionary of decimals only
    '''

    def __init__(self, *args, **kwargs):
        # self.update(*args, **kwargs)
        fkw = {}
        for key in kwargs:
            fkw[key] = dec(kwargs[key])
        dict.__init__(self, *args, **fkw)

    def __setitem__(self, key, val):
        dval = dec(val)
        dict.__setitem__(self, key, dval)


class Ddi(dict):

    '''
    Dictionary of decimals or text values
    '''

    def __init__(self, *args, **kwargs):
        # self.update(*args, **kwargs)
        fkw = {}
        for key in kwargs:
            if key.startswith('_'):
                fkw[key] = dec(kwargs[key])
            else:
                fkw[key] = kwargs[key]
        dict.__init__(self, *args, **fkw)

    def __setitem__(self, key, val):
        if key.startswith('_'):
            dval = dec(val)
        else:
            dval = val
        dict.__setitem__(self, key, dval)


def distribute(val, distArray, decimals=2):
    """
    input parameters:

    :param val: Decimal value for distribution
    :param distArray: Distribution Array
    :param decimals: Number of decimal digits
    :return: Tuple of distributed val
    """
    tmpArr = []
    val = dec(val, decimals)
    try:
        tar = dec(sum(distArray), decimals)
    except:
        return 0
    for el in distArray:
        tmpArr.append(dec(val * dec(el, decimals) / tar, decimals))
    nval = sum(tmpArr)
    dif = val - nval  # Get the possible difference to fix round problem
    if dif != 0:
        # Max number Element gets the difference
        tmpArr[tmpArr.index(max(tmpArr))] += dif
    return tuple(tmpArr)
