from os import getpid

from psutil import process_iter


def killOtherPys():
    '''
    Kill all other instances of python.exe except for current one.
    '''
    PROCNAME = "python.exe"
    currentPid = getpid()
    for proc in process_iter():
        try:
            if proc.name() == PROCNAME and proc.pid != currentPid:
                print 'Killing Python process %d' %proc.pid
                proc.kill()
        except:
            pass