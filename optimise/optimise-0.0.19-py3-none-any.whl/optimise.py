# -*- coding: utf-8 -*-
import yaml
import os
import sys
import pickle
from time import time
from hyperopt import fmin, tpe, hp, STATUS_OK
from .trials import Trials

import logging as log

class Optimiser():
    """ 
    wrapper for optimisation using hyperopt
    
        simplified search space (in addition to hyperopt distributions)
            max_depth=[8,10],       # int
            color=["r", "g", "b"],  # categoric
            normalize=[True,False], # bool
            c=[1., 5],              # float
            classifier="SVM"        # constant
            x=hp.lognormal("x",0,1) # any hyperopt distribution
                   
        before each iteration
            report parameters
        
        after each iteration
            report result
            pickle trials object so resilient to crash
            
        after optimisation
            report best result and params
            plot results by iteration
            plot results for each parameter
    """
    def __init__(self, folder="optimise"):
        """
        folder=location of logging
        """
        self.intparams = []
        self.findmax = False
        self.folder = folder
        if not os.path.exists(folder):
            os.mkdir(folder)
        self.trials = Trials()
    
    def convert(self, space):
        """ converts simple search space to hyperopt format
        """
        for k, v in list(space.items()):
            # hyperopt expression
            if isinstance(v, str) and v.startswith("hp."):
                pass
            # constant
            elif not isinstance(v, list):
                pass
            # categoric and bool
            elif len(v)>2 \
                    or any(isinstance(v, str) for v in v) \
                    or any(isinstance(v, bool) for v in v):
                space[k] = hp.choice(k, v)
            # integer
            elif all(isinstance(v, int) for v in v):
                space[k] = hp.quniform(k, v[0]-.5, v[1]+.5, 1)
                self.intparams.append(k)
            # float
            else:
                space[k] = hp.uniform(k, v[0], v[1])
            
    def make_target(self, func, inputs):
        """ wrap func with pre and post processing
            func signature: score=func(**params)
        """
        def target(params):
            """ called by optimiser for each iteraton
            """
            # save at start of iteration. Note latest only added on return.
            with open(os.path.join(self.folder, "trials.pkl"), "wb") as f:
                pickle.dump(self.trials, f)
            
            starttime = time()
            
            # report params
            if self.verbose >= 20:
                paramsout = ', '.join("{!s}={!r}".format(k,v) 
                                    for (k,v) in params.items())
                log.info(f"[{len(self.trials)}] {paramsout}")

            # hyperopt integers stored as float (probably a bug)
            for k in self.intparams:
                params[k] = int(round(params[k]))
            
            # add fixed inputs such as x, y
            params.update(inputs)
            
            #########################################
            loss = func(**params)
            #########################################

            # exclude fixed inputs from reporting or trials object
            params = {k:v for k,v in params.items() if k not in inputs}
            
            if self.findmax:
                loss = -loss
            
            # report score
            if self.verbose >= 20:
                log.info("****** %s"%loss)

            # add iteration to trials object
            params.update(loss=loss,
                          status=STATUS_OK, 
                          elapsed=time()-starttime)
            
            return params
        
        return target
    
    def minimise(self, func, evals=1, verbose=20, inputs=dict(), **hpargs):
        """
        minimise func by varying hyperparameters
        
        func=signature func(**params). returns loss to be minimised
        evals=additional func evaluations
                ignored if hpargs["max_evals"]
                hpargs["max_evals"] includes previous trials
        inputs=constants passed to each iteration e.g. x, y
                optional as can be passed in other ways
        hpargs["space"]=simplified hyperopt space to be converted to hp format
        hpargs passed to hyperopt
        """
        self.verbose = verbose
        
        if "trials" in hpargs:
            self.trials = hpargs["trials"]
        else:
            hpargs["trials"] = self.trials
        hpargs.setdefault("max_evals", len(self.trials) + evals)
        hpargs.setdefault("algo", tpe.suggest)
        self.convert(hpargs["space"])
        target = self.make_target(func, inputs)

        try:
            fmin(target, **hpargs)
        except KeyboardInterrupt:
            pass
        
        with open(os.path.join(self.folder, "trials.pkl"), "wb") as f:
            pickle.dump(self.trials, f)
        
        self.trials.report()

    def maximise(self, *args, **kwargs):
        """ maximise func by varying hyperparameters """
        self.findmax = True
        self.minimise(*args, **kwargs)

###############################################################
   
def get_space(key, folder=None):
    """ lookup space using key in search.yaml
    """
    for path in [folder] + sys.path + \
                    [os.path.join(sys.prefix, "etc", "optimise"), 
                     os.path.join(os.pardir, os.path.dirname(__file__))]:
        try:
            space = yaml.load(open(os.path.join(path, "search.yaml")))[key]
            space["name"] = key
            break
        except:
            continue

    return space
    
def get_params_range(params, excluded=None, spread=None):
    """ gets params space in range
        spread is either side of params.values()
        e.g. v=10, spread=[.9, 1.1] ==> v=[9, 11]
    """
    if spread is None:
        spread = [.9, 1.1]
    for k,v in params.items():
        if k in excluded:
            continue
        if isinstance(v, float):
            params[k] = [v*spread[0], v*spread[1]]
        elif isinstance(v, int):
            params[k] = [int(v*spread[0]), int(v*spread[1])]