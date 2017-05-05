"""Interface to read and write asciitable files from postprocess"""

import asciitable as at
import os
import logging


log=None

def logmessage(log, mess, string):
    if log is not None:
        getattr(log,mess)(string)

def add_columns(filename,columns,framename='df'):
    cframe = at.read(columns,Reader=at.Memory)
    from numpy.lib.recfunctions import append_fields
    if os.path.exists(filename):
        store = at.read(filename)
        if len(store) != len(cframe):
            print("file and data lengths don't match, aborting")
            return

        for col in cframe.dtype.names:
            if col in store.dtype.names:
                setattr(store,col,getattr(cframe,col))
            else:
                store=append_fields(store, col, getattr(cframe,col), dtypes=cframe.dtype[col],fill_value = -1e9)                
    else:
        store = cframe
    at.write(store,filename,delimiter=',')    

    
def init_file(filename, data=None, log=None):
    if not os.path.exists(filename):
        logmessage(log,"info","filename: {0} doesn't exist".format(filename))
    else:
        logmessage(log,"info","filename: {0} exists".format(filename))

def write(filename, data, keys, log=None,init=True,keepopen=False, format='h5'):
    if init:
        init_file(filename,data,log=log)
    add_columns(filename,data)
    
def read(filename):
    return at.read(filename,delimiter=',')
    
    
    
