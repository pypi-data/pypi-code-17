# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:38:16 2017

@author: liujiacheng1
"""

import scipy
import pandas as pd
import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import vq,kmeans,whiten
import numpy as np
import matplotlib.pylab as plt
from time import time
from sklearn import preprocessing

def cluster(n,time,method):

    
    
#points=scipy.randn(20,4) 



    points=pd.read_csv('process_pure'+time+'.csv')
    print('ok')
    points=points.iloc[:,0:]
    

#points=pd.DataFrame(points)

#points=np.loadtxt('raw_point.txt')
 
    print(points)

#normalizitiojn
    






    '''    
    points = preprocessing.scale(points)
    
    print(points)
    '''
    disMat = sch.distance.pdist(points,'euclidean') 
    

    s=sch.linkage(disMat,method=method) 

    P=sch.dendrogram(s)
    plt.savefig('plot_dendrogram.png')

    cluster= sch.fcluster(s,t=n,criterion='maxclust') 
    print(cluster)
    b=pd.DataFrame(cluster,columns=['clu'])

    a=pd.DataFrame(points)


    print(a)

    a.append(b)
    
    b=pd.concat([a,b],1)
    
    b=b.sort(columns='clu',axis=0)
    b.to_csv('clustered'+time+'.csv',index='false')
    print(b)



    print(cluster)
    
    
#cluster(30,'63912839','complete')