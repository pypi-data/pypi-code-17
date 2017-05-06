# -*- coding: utf-8 -*-
"""Module grup"""


def grup(txtval):
    '''
    Trasforms a string to uppercase special for Greek comparison
    '''
    ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΐΊκλμνξοόΌπρσςτυύϋΰΎφχψωώΏ"
    ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΪΪΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΫΫΥΦΧΨΩΩΩ"
    ftxt = u''
    for letter in txtval:
        if letter in ar1:
            ftxt += ar2[ar1.index(letter)]
        else:
            ftxt += letter.upper()
    return ftxt
