import numpy as np
import scipy.linalg as la
from numpy.testing import assert_almost_equal
import multiprocessing as mp
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans
import random
import pandas as pd
import time
from __future__ import division


def distance(x,Y):
    ''' 
        Function to calculate the distance between a point x and a Y, a subset of X
        Input: x, a single data point. Y, a collection of data points 
        Output: The minimum Euclidean norm of x and each element in Y  
    '''
    distances=[la.norm(x-y) for y in Y]
    return min(distances)
    
    
def k_means_pp(X,k):
    ''' 
        Function to initialize centers for the k-means++ algorithm
        Input: X, an array of data. k, the number of clusters
        Output: C, an array with length k of initial cluster centers. 
    '''
    random.seed(22)
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
                dist_x[i]=distance(X[i,:],C)**2
        #use dist_x to calculate the probability that each x is chose 
        probabilities=dist_x/sum(dist_x)
        #randomly choose an x according to these probabilities
        rand=np.random.choice(X.shape[0],1, p=probabilities)
        C = np.vstack([C, X[rand,:]])
    
    #finally, return the array of centers 
    return C


def weighted_clusters(weights, X,k):
    '''
        Function to return weighted centers for the k-means++ algorithm. To be used in kmeans||
        Input: X, an array of data. k, the number of clusters. weights, a vector of length X
        Output: C, an array with length k of initial cluster centers. 
    
    '''
    first_center = np.random.choice(X.shape[0], 1)
    weight_C = X[first_center,:]

    for i in range(k-1):
        #calculate the distance between each x in X and the currently initialized centers 
        dist_x=np.ones(len(X))
        for i in range(len(X)):
            if X[i,:] in weight_C:
                dist_x[i]=0
            else:
                dist_x[i]=distance(X[i,:],weight_C)**2
        #use dist_x to calculate the probability that each x is chose 
        probabilities=dist_x/sum(dist_x)
        #randomly choose an x according to these probabilities
        rand=np.random.choice(X.shape[0],1, p=probabilities)
        weight_C = np.vstack([weight_C, X[rand,:]])
    
    #finally, return the array of centers 
    return weight_C
    
    
    
    def scalable_k_means_pp(X,k,ell):
    ''' 
        Function to initialize centers for the k-means|| algorithm
        Input: X, an array of data. k, the number of clusters
        Output: C, an array with length k of initial cluster centers.  
    '''
    #randomly choose the first c
    first_center = np.random.choice(X.shape[0], 1)
    C = X[first_center,:]
    
    #calculate the intitial cost. This will tell us how many times to loop.
    cost_initial=sum([distance(x,C)**2 for x in X])
    
    for i in range(int(round(np.log(cost_initial)))):
        #calculate the distance 
        dist_x=[distance(x,C)**2 for x in X]
       
        #calculate the probabilities for each x
        probabilities=(np.array(dist_x)*ell)/sum(dist_x)
        #iterate through each datapoint
        for j in range(len(X)):
            #draw a random uniform number. 
            rand=np.random.uniform()
            #if rand<= the probability and that datapoint isn't already in C, add to C
            if rand<=probabilities[j] and X[j,:] not in C: 
                C = np.vstack([C, X[j,:]])
    
    #initialize weights 
    weights=np.zeros(C.shape[0])
    #iterate through each item in C
    for x in X:
        c_no = -1
        min_dist = np.inf
        for i in range(C.shape[0]):
            dist = la.norm(C[i]-x)
            if min_dist > dist:
                min_dist = dist
                c_no = i
        weights[c_no] = weights[c_no]+1
    
    #normalize the weights 
    weights=np.array(weights)/sum(weights)

    #return those weights as the chosen centers
    return weighted_clusters(weights, C,k)     
    
def check_module():
    print('This is Statistical Computation Project')
    
def asdf():
    print('asdfs')
