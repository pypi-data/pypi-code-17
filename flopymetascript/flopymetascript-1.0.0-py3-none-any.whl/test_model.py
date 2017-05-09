# coding=utf-8
import glob
import io
import hashlib
import os
import zipfile
from tempfile import TemporaryDirectory
import flopy

from flopymetascript.model import Model

"""
0. process zip in to zip out
    if no serious errors occured, happy
1. unzip the input files to temporary directory
2. unzip output files to temperary directory
3. evaluate python script, model_ws -> temporary directory and write the the input files


"""

fn_in = '/Users/bfdestombe/PycharmProjects/BW/BW.zip'


p_list = flopy.seawat.Seawat().mfnam_packages.keys()
Model(add_pack=p_list)
