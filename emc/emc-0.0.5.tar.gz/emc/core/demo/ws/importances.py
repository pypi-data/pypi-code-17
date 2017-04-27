'''
Created on Mar 4, 2015

@author: Administrator
'''
from numpy import array, float32, arange
from emc.cpp.swig.emcpp import realignImportances


if __name__ == '__main__':
    alpha = 0.1
    
    grades = array([[1.0, 0.0],
                    [0.8, 0.0],
                    [0.6, 0.0],
                    [0.4, 0.0],
                    [0.2, 0.0],
                    [0.0, 0.0]], dtype=float32)
    
    
    imp = array([0.5, 0.5], dtype=float32)
    
    for i in arange(10000):
        realignImportances(imp, grades, alpha)
    
    print imp