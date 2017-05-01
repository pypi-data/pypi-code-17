import click
import os, sys
import errno
import pandas as pd
import numpy as np
import dnamodel as dm
#import logging


all_colors = 'black', 'red', 'green', 'yellow', 'blue', 'magenta', \
             'cyan', 'white'

@click.command()
@click.argument('input_file')
@click.option('--model', '-m', type=click.Path(), help='An existing dnamodel .h5 file')


def main(input_file, model):
    """Automated, experimentally-driven design and optimization of DNA sequences."""
    greet = 'Hello'
    print input_file


    raw_data = pd.read_excel(input_file, header=0)
    print len(raw_data.columns)
    col_names = ['sequence']
    for i in range(1, len(raw_data.columns)):
        col_names.append('output'+str(i))
    raw_data.columns = col_names
    print raw_data.columns

    #should do this for each column
    df = raw_data[np.isfinite(raw_data['output1'])]

    dnaCNN = dm.dnaModel(df, filename=model) 
    ### dnaCNN is now a model object with a CNN and training/testing data ###
    ### it compiles ### 
    ### and trains (default my current hyperparams, but this should ###
    ### eventually tune/optimize hyperparams) the CNN ### 
    dnaCNN.train()
    
    dnaCNN.design()
    ### when we execute design (default maximizes col B), ###
    ### it returns a set (default some percentage of the input data) ###
    ### of new designs to test (default cheap). ###


    dnaCNN.save()
    ### BUT FOR NOW ... the last thing it does is output a saved model file. ###

    dnaCNN.test()

    #dnaCNN.design()
