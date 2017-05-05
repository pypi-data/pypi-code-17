#!/usr/bin/env python
from . import t15
import netCDF4
import dwell.rad.terminal as terminal
from argh import arg
import numpy
import asciitable
from collections import OrderedDict
import os
import logging

@arg("filenames", nargs="+")
def plot(filenames, output=None,t15obs=None):
    import pylab as pl
    from . import plots
    import os

    data = dict((f,asciitable.read(f,delimiter=",")) for f in filenames)
    pl.figure(figsize=(8,8))
    t15obs = t15obs or filenames[0]
    data["t15obs"] = asciitable.read(t15obs,delimiter=",")
    for f in filenames:
        plots.ls_plot(data[f]["ls"],data[f]["t15"],loop=True,label=os.path.dirname(f).split("/")[-1])
    plots.ls_plot(data["t15obs"]["ls"],data[f]["t15obs"],loop=True,label="T15")
    pl.gca().set_xlabel("Ls")
    pl.gca().set_ylabel("T15 (K)")
    pl.legend(loc='top left')
    output = output or "t15.pdf"
    pl.savefig(output)
    return None

def main():
    terminal.argh_main("t15",[plot])
if __name__=="__main__":
    main()
