"""interface to save data into HDF5 data using Pandas library"""

import pandas as pd
import os
import logging



log=None

def logmessage(log, mess, string):
    if log is not None:
        getattr(log,mess)(string)

def drop_duplicates(df):
    Cols = list(df.columns)
    found=False
    for i,item in enumerate(df.columns):
        if item in df.columns[:i]:
            logmessage(log,"Warning", "Dropping one instance of {0}".format(item))
            Cols[i] = "toDROP"
            found=True
    if found:
        df.columns = Cols
        df = df.drop("toDROP",1)
    return df

def add_columns(filename,columns,framename='df'):
    cframe = pd.DataFrame(columns).set_index('times')
    if os.path.exists(filename):
        with pd.HDFStore(filename,'a') as store:
            frame = store[framename]
            newframe = pd.concat([frame,cframe],axis=1)
            newframe = drop_duplicates(newframe)
            store[framename] = newframe
    else:
        with pd.HDFStore(filename) as store:
            store[framename] = cframe
            

    
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
    if isinstance(filename,str):
        handle = pd.HDFStore(filename,'r')
    else:
        handle=filename

    return handle["df"]
        
