# -*- coding: utf-8 -*-
""" manages collection of model runs with params, scores and predictions """

import os
import json
import shutil
import numpy as np
import pandas as pd
import logging as log
from IPython.display import clear_output

from .gridplot import Gridplot
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class Runs():
    """ resilient, file based store of a group of runs
        each run includes classifier name, params, scores, predictions
        train/test data is not currently included (should be?)
        classifier itself is not serialized (should be?)
        
        logruns.json
            One row per run
            Each row is a json object with index, clfname, params and scores
            No fixed schema so holds any parameters
            Reads whole table every time => avoid too many runs in a table
            Append adds to file => resilient to user interrupt or crash

        preds0, preds1 etc..
            Stores the predictions. Suffix is the index number from logruns
            
        self.next
            index of next row in logruns
            used as key to link logruns and preds files
    """
    def __init__(self, folder, mode="a"):
        """ 
        folder is location for logruns.json and preds files
        mode a=append, w=write
        """
        self.folder = folder
        
        if mode == "a":
            # set self.next
            self.read()
            
        elif mode =="w":
            shutil.rmtree(folder, ignore_errors=True)
            os.makedirs(folder, exist_ok=True)
            self.next = 0
            
        else:
            log.error("Runs mode must be a or w (append or write)")
        
    def read(self):
        """ return logruns as a pandas dataframe """
        try:
            # each row is a json object. convert to "," delimited list
            with open(os.path.join(self.folder, "logruns.json")) as f:
                data=",".join(f.readlines())
            df = pd.read_json("[%s]"%data)
        except FileNotFoundError as e:
            df = pd.DataFrame()
        self.next = len(df)
        return df
    
    def append(self, row, preds=None):
        """ append row as a json object
            save preds to file
        """
        # predictions
        with open(os.path.join(self.folder, 
                               "preds%s"%self.next), "wb") as f:
            np.save(f, preds)

        # params and scores
        with open(os.path.join(self.folder, "logruns.json"), "a") as f:
            json.dump(row, f)
            f.write("\n")
            self.next += 1
            
    def report(self, clear=True):
        """ reports best run and plots all runs
        """
        if clear:
            clear_output()

        # get best
        runs = self.read()
        best = runs.ix[runs.score.idxmax()].to_dict()
        best_params ={k:v for k, v in best.items() \
                       if k not in ["elapsed", "score", "clf", "name"]
                       and not pd.isnull(v)}
        
        # print best
        best_params = ', '.join("{!s}={!r}".format(k,v) 
                        for (k,v) in best_params.items())
        print("Best model:\n%s"%(best_params))
        print("Best score=%s"%(best["score"]))
        
        # print plots
        self.plot()
    
    def plot(self, metric="score", aggfunc="mean"):
        """ plots results by parameter 
        metric = score, elapsed
        aggfunc = mean, var, count
        """
        # drop errors so we can plot the rest. NOT NEEDED ANYMORE???
        #####runs = runs.replace([np.inf, -np.inf], np.nan)
    
        runs = self.read()

        # positive charts look better especially barcharts
        runs.score = runs.score.apply(abs)
    
        # show the plots in a grid
        Gridplot()

        # force axis to integer or rounded decimal
        ax = plt.figure().gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        # overall plot including all runs
        plt.plot(range(1,len(runs)+1), runs[metric])
        plt.title("%s by run"%metric)
        plt.ylabel(metric)
    
        # plots for each parameter
        for param in runs.drop(["score", "elapsed"], axis=1):
            agg = runs.groupby(param).agg(aggfunc)
                
            if len(agg) < 2:
                # 0=not used 1=constant
                continue
            # lineplot for numeric
            if agg.index.is_numeric():
                plt.plot(agg.index, agg[metric])
            else:
            # barchart for category
                xpos=np.arange(len(agg))            
                plt.bar(xpos, agg[metric], align='center', alpha=0.5)
                plt.xticks(xpos, agg.index)
                # stretch axis to highlight differences
                minx, maxx = min(agg[metric]), max(agg[metric])
                # extend axis to show the smallest bar
                extra = abs(maxx-minx)/10
                minx = minx - extra
                maxx = maxx + extra  
                plt.ylim(minx, maxx)
            plt.title(param)
            plt.ylabel(metric)
        plt.tight_layout()
        plt.show()
        
    def barchart(self):
        """ barchart of model scores. 
        colors is e.g. pd.Series(["pre"*3], ["optimised"]*2])
        """
        rep = self.read()[["name", "score"]]
        plt.figure(figsize=((10, 5)))
        plt.xlim(rep.score.min()*.98, rep.score.max()*1.02)
        rep = rep.set_index("name")
        rep.score.plot(kind="barh", legend=False)
        plt.title("CV scores")

    def get_correlations(self):
        """ returns dataframe with scores and correlations for all runs
            candidates for ensemble need high scores, low correlations
        """
        # get prediction data and correlate
        predfiles = [f for f in os.listdir(self.folder) if f.startswith("preds")]
        data = []
        for pred in predfiles:
            with open(os.path.join(self.folder, pred), "rb") as f:
                data.append(np.load(f).reshape(-1))
        df = pd.DataFrame(np.corrcoef(data))
    
        runs= self.read()
        
        # add row and column labels
        df.index.name = "runid1"
        df.columns = df.index.copy()
        df.columns.name = "runid2"

        # stack correlations. index is runid1/runid2
        df = pd.DataFrame(df.stack())
        df.columns = ["r2"]
        df = df.reset_index()
        df = df[df.runid1!=df.runid2]
        
        # add scores and names
        df["score1"] = df.runid1.map(runs.score)
        df["score2"] = df.runid2.map(runs.score)
        df["name1"] = df.runid1.map(runs.name)
        df["name2"] = df.runid2.map(runs.name)

        df = df.sort_values(["r2"])
        return df
        
    def plot_correlations(self, runid):
        """ scatter plot a runid against other runs to find 
        candidates for ensemble """
        df = self.get_correlations()
        df = df[(df.runid1==runid) & (df.runid2!=runid)]
        plt.plot(df.r2, df.score2, "o")
        plt.title("model %s"%runid)
        plt.xlabel("correlation")
        plt.ylabel("score")
        plt.gca().invert_xaxis()
        for row in df.itertuples():
            plt.annotate(row.runid2, (row.r2, row.score2))  