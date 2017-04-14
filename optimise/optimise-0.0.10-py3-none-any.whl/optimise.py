# -*- coding: utf-8 -*-
""" 
wrapper for optunity optimisation 

    enhanced format for search_space
        int (numbers without decimal point)
        bool
        list of strings
        fixed (single keys or single values)
        logspace e.g.[0,3] selects x=0-3 and then 10**x
        
    replaces log with runs object
        saves each iteration so resilient to crash or manual interrupt
        plots results by iteration

    NOTE ALSO commented out call_log in:
    C:/Users/s/Anaconda3/Lib/site-packages/optunity/api.py LINE 266
            call_dict = dict()######f.call_log.to_dict()
        BECAUSE
            call_log fails sometimes with incorrect key
            don't need the log as replaced by runs object
"""

import optunity
import yaml
import os
import sys
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from .runs import Runs
from time import time

import logging as log

class Optuner():
    """ wrapper for optunity """
    
    def __init__(self, folder="optimise"):
        self.intparams = []
        self.logparams = []
        self.fixedparams = dict()
        self.count = 1
        self.runs = Runs(folder, "w")
   
    def cleanparams(self, params):
        """ recursively convert search_space to optunity format
        
            convert
                bools to int
                list of strings to sub-keys
                single values to fixed parameters
                single keys to fixed parameters
            create for later processing
                self.fixedparams=list of fixed parameters 
                self.logparams=list of logspace params (10**value)
                self.intparams=list of keys to be constrained to int
            remove logparams (special key listing logspace params)
        """
        # logspace params e.g. -3, 3 => 10**-3, 10**3
        if not self.logparams:
            self.logparams = params.pop("logparams", [])
        
        for k in list(params.keys()):
            v = params[k]
            if isinstance(v, dict):
                if len(v.keys()) == 1:
                    k2, v2 = list(v.items())[0]
                    if not isinstance(v2, list):
                        self.fixedparams[k] = k2
                self.cleanparams(params[k])
                continue
            try:
                if v and not isinstance(v, list):
                    v = [v]
                # fixed param
                if len(set(v)) == 1:
                    v = v[0]
                    if v in self.logparams:
                        self.fixedparams[k] = 10**v
                    else:
                        self.fixedparams[k] = v
                    del params[k]
                # convert list of strings to sub-entries
                elif isinstance(v[0], str):
                    params[k] = {v: None for v in v}
                # convert bool to int
                elif all([isinstance(v, bool) for v in v]):
                    params[k] = sorted([x*1 for x in v])
                    self.intparams.append(k)
                # compile list of integer parameters
                elif all([isinstance(v, int) for v in v]):
                    self.intparams.append(k)
            except (TypeError, KeyError):
                pass
        
    def make_target(self, func, constants):
        """ make target
                func has signature score=func(**params)
                constants fixed for all iterations e.g. x and y
        """
        def target(**params):
            """ target function for each optunity iteration
                    enables fixed params in search space
                    removes nulls
                    converts intparams to integer
                    converts logparams to logspace
                    updates params with constants
                    logs params, scores

                params provided by optimiser for each iteration
            """
            starttime = time()
           
            # enable fixed parameters that are always the same value
            params.update(self.fixedparams)
            # remove k=None (bug in optunity) and v=None (na for this run) 
            params = {k:v for k,v in params.items() if k and v}
            # convert intparams to integer
            for k in set(params) & set(self.intparams):
                params[k] = int(round(params[k]))
            # convert logparams to logspace i.e. -3, 3 searches .001 to 1000
            for k in set(params) & set(self.logparams):
                params[k] = 10**params[k]

            # report params
            if self.verbose >= 20:
                paramsout = ', '.join("{!s}={!r}".format(k,v) 
                                    for (k,v) in params.items())
                log.info("[%s] %s"%(self.count, paramsout))

            # add constants such as x, y
            params.update(**constants)
            
            #########################################
            score = func(**params)
            #########################################

            # remove constants
            params = {k:v for k,v in params.items() if k not in constants}
            
            # log results
            params.update(score=score, 
                          elapsed=time()-starttime)
            for fixed in self.fixedparams:
                del params[fixed]
            self.runs.append(params)
          
            # report score
            if self.verbose >= 20:
                log.info("****** %s"%score)
            self.count += 1
            return score
        return target

    def maximise(self, target, num_evals, search, verbose=20,
                                         constants=dict()):
        """ 
            maximise target within defined search space
        
            target has signature score=target(**params)
            constants are fixed for every iteration e.g. x and y
            verbose=20 report every iteration
        """     
        self.verbose = verbose
        #pprint(search)
        self.cleanparams(search)
        #pprint(search)

        # note ignore return values as using runs instead
        # runs has functions such as plot, report and correlations
        optunity.maximize_structured(self.make_target(target, **constants), 
                                     search_space=search, 
                                     num_evals=num_evals)
        self.runs.report()
        
############################################################################
        
def get_search(target):
    """ return search space for optimisation
        target can be string or classifier
    """
    # classifier convert to string
    if isinstance(target, BaseEstimator):
        target = target.__class__.__name__
    
    # get latest params
    for path in sys.path + \
                    [os.path.join(sys.prefix, "etc", "optimise"), 
                     os.path.join(os.pardir, os.path.dirname(__file__))]:
        try:
            allparams = yaml.load(open(os.path.join(path, "search.yaml")))
            break
        except:
            continue

    return allparams[target]
    
def get_search_range(params, excluded=None, spread=None):
    """ gets search space in range """
    if spread is None:
        spread = [.9, 1.1]
    for k,v in params.items():
        if k in excluded:
            continue
        if isinstance(v, float):
            params[k] = [v*spread[0], v*spread[1]]
        elif isinstance(v, int):
            params[k] = [int(v*spread[0]), int(v*spread[1])]