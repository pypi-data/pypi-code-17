
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.cm as cm, matplotlib.font_manager as fm
# define the font styles
title_font = fm.FontProperties(family='serif', style='normal', size=19, weight='normal', stretch='normal')
label_font = fm.FontProperties(family='serif', style='normal', size=16, weight='normal', stretch='normal')
ticks_font = fm.FontProperties(family='serif', style='normal', size=10, weight='normal', stretch='normal')
annotation_font = fm.FontProperties(family='serif', style='normal', size=10, weight='normal', stretch='normal')
axis_bgcolor = 'white'
# make a re-usable function to draw nice bar charts
def plot_hist(data, title='', xlabel='Test Statistic Values', ylabel='Frequency', color='red', test_stat=None):
    
    if type(data) == list:
        data = pd.Series(data)
    ax = data.hist(figsize=[9, 6], width=0.35, alpha=0.5, 
                   color=color, edgecolor='k', grid=False, rwidth=.9)

    ax.set_xticklabels(data.index, rotation=45, rotation_mode='anchor', ha='right')
    ax.yaxis.grid(True)
    #for label in ax.get_yticklabels():
    #    label.set_fontproperties(ticks_font)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(False)
    ax.set_facecolor(axis_bgcolor)   
    ax.set_title(title, fontproperties=title_font)
    ax.set_xlabel(xlabel, fontproperties=label_font)
    ax.set_ylabel(ylabel, fontproperties=label_font)
    if test_stat:
        plt.axvline(test_stat, lw=7)

    plt.show()