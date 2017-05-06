# -*- coding: utf-8 -*-
import decimal
from collections import OrderedDict


def isNum(val):  # is val number or not ?
    """ use: Returns False if val is not a number , True otherwise
        input parameters :
            1.val : the value to check against.
        output: True or False
        """
    try:
        float(val)
    except ValueError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """ use : Given a number, it returns a decimal with a specific number
        of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
    if poso is None:
        poso = 0
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


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


class Dordict(OrderedDict):

    '''
    Ordered Dictionary of decimals
    '''

    def __init__(self, *args, **kwargs):
        # self.update(*args, **kwargs)
        fkw = {}
        for key in kwargs:
            fkw[key] = dec(kwargs[key])
        OrderedDict.__init__(self, *args, **fkw)

    def __setitem__(self, key, val):
        dval = dec(val)
        OrderedDict.__setitem__(self, key, dval)


def triades(txt, separator='.'):
    '''
    Help function to split digits to thousants ( 123456 becomes 123.456 )
    '''
    ltxt = len(txt)
    rem = ltxt % 3
    precSpace = 3 - rem
    stxt = ' ' * precSpace + txt
    a = []
    while len(stxt) > 0:
        a.append(stxt[:3])
        stxt = stxt[3:]
    a[0] = a[0].strip()
    fval = ''
    for el in a:
        fval += el + separator
    return fval[:-1]


def dec2gr(poso, decimals=2, zeroasnull=False):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    if poso == 0 and zeroasnull:
        return ' '
    prosimo = ''
    strposo = str(poso)
    if len(strposo) > 0:
        if strposo[0] in '-':
            prosimo = '-'
            strposo = strposo[1:]
    timi = '%s' % dec(strposo, decimals)
    intpart, decpart = timi.split('.')
    final = triades(intpart) + ',' + decpart
    if final[0] == '.':
        final = final[1:]
    return prosimo + final


def dec2gr2(poso, decimals=2, zeroAsSpace=False):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    if dec(poso) == dec(0):
        if zeroAsSpace:
            return ''
        else:
            decs = '0' * decimals
            if decimals > 0:
                return '0,' + decs
            else:
                return '0'

    def triades2(txt, separator='.'):
        '''
        Help function to split digits to thousants ( 123456 becomes 123.456 )
        '''
        ltxt = len(txt)
        rem = ltxt % 3
        precSpace = 3 - rem
        stxt = ' ' * precSpace + txt
        a = []
        while len(stxt) > 0:
            a.append(stxt[:3])
            stxt = stxt[3:]
        a[0] = a[0].strip()
        fval = ''
        for el in a:
            fval += el + separator
        return fval[:-1]

    prosimo = ''
    strposo = str(poso)
    if len(strposo) > 0:
        if strposo[0] in '-':
            prosimo = '-'
            strposo = strposo[1:]
    timi = '%s' % dec(strposo, decimals)
    intpart, decpart = timi.split('.')
    final = triades2(intpart) + ',' + decpart
    if final[0] == '.':
        final = final[1:]
    return prosimo + final


def gr2dec(poso):
    '''
    Returns decimal (12.345,67 becomes 12345.67)
    '''
    st = poso.replace('.', '')
    ds = st.replace(',', '.')
    return dec(ds)


def nul2DecimalZero(val):
    '''
    Instead of null returns 0.
    '''
    return dec(val)


def distribute(val, distArray, decimals=2):
    """
    input parameters:
    val       : Decimal value for distribution
    distArray : Distribution Array
    decimals  : Number of decimal digits
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
    if dif == 0:
        pass
    else:
        # Max number Element gets the difference
        tmpArr[tmpArr.index(max(tmpArr))] += dif
    return tmpArr


def nul2z(val):
    '''
    Instead of null returns 0. For sqlite use.
    '''
    if val:
        return val
    else:
        return 0
