# -*- coding: utf-8 -*-
#Tested in Python 2.7, 3.5, 3.6

"""
Module with class TicToc to replicate the functionality of MATLAB's tic and toc.
"""

__author__       = 'Eric Fields'
__version__      = '1.2.0'
__version_date__ = '27 April 2017'

#perf_counter is the preferred clock; 
#for Python versions before 3.3, use time.clock
try:
    from time import perf_counter
    clock = 'time.perf_counter'
except ImportError:
    import time
    perf_counter = time.clock
    clock = 'time.clock'


class TicToc(object):
    
    """
    Replicate the functionality of MATLAB's tic and toc.
        
    t = pytictoc.TicToc() #create instance of class
    
    #Methods
    t.tic()       #start or re-start the timer
    t.toc()       #print elapsed time since timer start
    t.tocvalue()  #return floating point value of elapsed time since timer start
    
    #Attributes
    t.start     #Time from time.perf_counter() when t.tic() was last called
    t.end       #Time from time.perf_counter() when t.toc() or t.tocvalue() was last called
    t.elapsed   #t.end - t.start; i.e., time elapsed from t.start when t.toc() or t.tocvalue() was last called
    """
    
    def __init__(self):
        """Create instance of TicToc class."""
        self.start   = float('nan')
        self.end     = float('nan')
        self.elapsed = float('nan')
        
    def tic(self):
        """Start the timer."""
        self.start = perf_counter()
        
    def toc(self, msg='Elapsed time is', restart=False):
        """
        Report time elapsed since last call to tic().
        
        Optional arguments:
            msg     - String to replace default message of 'Elapsed time is'
            restart - Boolean specifying whether to restart the timer
        """
        self.end     = perf_counter()
        self.elapsed = self.end - self.start
        print('%s %f seconds.' % (msg, self.elapsed))
        if restart:
            self.start = perf_counter()
        
    def tocvalue(self, restart=False):
        """
        Return time elapsed since last call to tic().
        
        Optional argument:
            restart - Boolean specifying whether to restart the timer
        """
        self.end     = perf_counter()
        self.elapsed = self.end - self.start
        if restart:
            self.start = perf_counter()
        return self.elapsed
