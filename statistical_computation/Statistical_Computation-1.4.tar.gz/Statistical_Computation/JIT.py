from __future__ import division
import numpy as np
import scipy.linalg as la
from numpy.testing import assert_almost_equal
import multiprocessing as mp
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans
import random
import pandas as pd
import time

@jit
def jit_distance(x,Y):
    ''' 
        Function to calculate the distance between a point x and a Y, a subset of X
        Input: x, a single data point. Y, a collection of data points 
        Output: The minimum Euclidean norm of x and each element in Y  
    '''
    dist=np.zeros(len(Y))
    
    for i in range(len(Y)):
        dist_int = 0
        for j in range(len(x)):
            dist_int =dist_int+(x[j] - Y[i,j])**2
        dist[i]= dist_int**0.5
        
    min_dist = dist[0]
    
    for i in range(len(dist)):
        if dist[i] < min_dist:
            min_dist = dist[i]
    return min_dist

@jit
def jit_k_means_pp(X,k):
    
    ''' 
        Function to initialize centers for the k-means++ algorithm
        Input: X, an array of data. k, the number of clusters
        Output: C, an array with length k of initial cluster centers. 
    '''
       #randomly choose the first c
    first_center = np.random.choice(X.shape[0], 1)
    C = X[first_center,:]
    
    
    for i in range(k-1):
        #calculate the distance between each x in X and the currently initialized centers 
        dist_x=np.ones(len(X))
        for i in range(len(X)):
            if X[i,:] in C:
                dist_x[i]=0
            else:
                dist_x[i]=jit_distance(X[i,:],C)**2
        #use dist_x to calculate the probability that each x is chose 
        probabilities=dist_x/sum(dist_x)
        #randomly choose an x according to these probabilities
        rand=np.random.choice(X.shape[0],1, p=probabilities)
        C = np.vstack([C, X[rand,:]])
    
    #finally, return the array of centers 
    return C
    

@jit
def jit_weighted_clusters(weights, X,k):
    '''
        Function to return weighted centers for the k-means++ algorithm. To be used in kmeans||
        Input: X, an array of data. k, the number of clusters. weights, a vector of length X
        Output: C, an array with length k of initial cluster centers. 
    
    '''
    first_center = np.random.choice(X.shape[0], 1)
    C = X[first_center,:]

    for i in range(k-1):
        #calculate the distance between each x in X and the currently initialized centers 
        dist_x=np.ones(len(X))
        for i in range(len(X)):
            if X[i,] in C:
                dist_x[i]=0
            else:
                dist_x[i]=jit_distance(X[i,:],C)**2
        #use dist_x to calculate the probability that each x is chose 
        probabilities=dist_x/sum(dist_x)
        #randomly choose an x according to these probabilities
        rand=np.random.choice(X.shape[0],1, p=probabilities)
        C = np.vstack([C, X[rand,:]])
  
    
    #finally, return the array of centers 
    return C
    

@jit
def jit_scalable_k_means_pp(X,k,ell):
    ''' 
        Function to initialize centers for the k-means|| algorithm
        Input: X, an array of data. k, the number of clusters
        Output: C, an array with length k of initial cluster centers.  
    '''
    first_center = np.random.choice(X.shape[0], 1)
    C = X[first_center,:]
    
    #calculate the intitial cost. This will tell us how many times to loop.
    cost_initial=0
    for x in X:
        cost_initial=cost_initial+jit_distance(x,C)**2
    
    for i in range(int(round(np.log(cost_initial)))):
        #calculate the distance 
        dist_x=np.ones(len(X))
        for i in range(len(X)):
            if X[i,:] in C:
                dist_x[i]=0
            else:
                dist_x[i] =jit_distance(X[i,:],C)**2
       
        #calculate the probabilities for each x
        probabilities=(np.array(dist_x)*ell)/sum(dist_x)
        #iterate through each datapoint
        for j in range(len(X)):
            #draw a random uniform number. 
            rand=np.random.uniform()
            #if rand<= the probability and that datapoint isn't already in C, add to C
            if rand<=probabilities[j]: 
                C = np.vstack([C, X[j,:]])
                
    #initialize weights 
    weights=np.zeros(C.shape[0])
    #iterate through each item in C
    for x in X:
        c_no = -1
        min_dist = np.inf
        for i in range(C.shape[0]):
            dist=0
            for j in range(len(x)):
                c=C[i]
                dist += (x[j] - c[j])**2
            dist= dist**0.5
        
            if min_dist > dist:
                min_dist = dist
                c_no = i
        weights[c_no] = weights[c_no]+1
    
    #normalize the weights 
    weights=weights/sum(weights)

    #return those weights as the chosen centers
    return jit_weighted_clusters(weights, C,k) 
    
    