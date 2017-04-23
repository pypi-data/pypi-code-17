# -*- coding: utf-8 -*-
""" manages collection of model runs with params, scores and predictions """

import os
import numpy as np
import pandas as pd
import logging as log
from IPython.display import clear_output

from .gridplot import Gridplot
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import hyperopt

class Trials(hyperopt.Trials):
    """ adds reporting to trials object """
    
    excluded = ["elapsed", "loss", "status"]
    
    def report(self, clear=True):
        """ reports best run and plots all runs
        """
        if clear:
            clear_output()

        # get best
        best = self.best_trial["result"]
        
        # print best
        best_params = ', '.join("{!s}={!r}".format(k,v) 
                        for (k,v) in best.items()
                            if k not in self.excluded
                            and v)
        print("Best model:\n%s"%(best_params))
        print("Best loss=%s"%(best["loss"]))
        
        # print plots
        self.plot()
    
    def plot(self, metric="loss", aggfunc="mean"):
        """ plots results by parameter 
        metric = loss, elapsed
        aggfunc = mean, var, count
        """
        df = pd.DataFrame(self.results, index=range(len(self.results)))
        
        # positive charts look better especially barcharts
        for col in df.columns:
            try:
                df[col].apply(abs)
            except:
                pass
    
        # show the plots in a grid
        Gridplot()

        # overall plot including all runs
        plt.plot(range(1,len(df)+1), df[metric])
        plt.xticks(range(1,len(df)+1))
        plt.title("%s by run"%metric)
        plt.ylabel(metric)
    
        # plots for each parameter
        for param in df.drop(self.excluded, axis=1):
            agg = df.groupby(param).agg(aggfunc)
                
            if len(agg) < 2:
                # 0=not used 1=constant
                continue
            # lineplot for numeric
            if agg.index.is_numeric():
                plt.plot(agg.index, agg[metric])
                if agg.index.dtype == np.int64:
                    plt.xticks(range(min(agg.index), max(agg.index)+1))
            else:
            # barchart for category
                xpos=np.arange(len(agg))            
                plt.bar(xpos, agg[metric], align='center', alpha=0.5)
                plt.xticks(xpos, agg.index)
                plt.ylim(min(agg[metric])*.98, max(agg[metric]*1.02))
            plt.title(param)
            plt.ylabel(metric)
        plt.tight_layout()
        plt.show()
        
    def barchart(self):
        """ barchart of model scores
        """
        df = pd.DataFrame(self.results, 
                          index=range(len(self.results))) \
                          ["name", "loss"]
        df.loss = df.loss.apply(abs)
                
        plt.figure(figsize=((10, 5)))
        plt.xlim(df.score.min()*.98, df.score.max()*1.02)
        df = df.set_index("name")
        df.loss.plot(kind="barh", legend=False)
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