from os import chdir
from os.path import dirname, abspath


def cdr():
    '''
    CD to resource directory
    '''
    resourceDir =  "%s/../../../resources" % (dirname(__file__))
    chdir(abspath(resourceDir))