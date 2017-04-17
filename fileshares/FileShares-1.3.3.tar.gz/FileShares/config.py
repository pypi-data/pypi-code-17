import os, sys, logging
from termcolor import colored


ENV = (sys.platform, sys.version.split()[0])
PATH_DEL = '\\' if ENV[0][:3].lower() == 'win' else '/'

logging.basicConfig(
    format='%(levelname)s:%(asctime)s:%(message)s',
    level=logging.DEBUG,
)

loger = logging.getLogger()

def setloglevel(i):
    global loger
    value = {
        1: logging.INFO,
        2: logging.WARN,
        3: logging.DEBUG,
        4: logging.ERROR
    }.get(i,logging.DEBUG)
    
    loger.setLevel(value)

if __name__ == '__main__':
    print(ENV)