import numpy as np

import fc_hypermesh.CartesianGrid as CG

from fc_tools.graphics import isMatplotlib

from  copy import deepcopy

class EltMesh:
  def __init__(self,d,m,q,me,toGlobal,**kwargs):
    color=kwargs.get('color', [0,0,1] )
    label=kwargs.get('label', '' )
    assert( m <= d)
    assert( q.shape[0]==d )
    self.d=d
    self.m=m
    self.q=q
    self.me=me
    self.toGlobal=toGlobal
    if (me.shape[0]==m+1): # m-simplicial
      self.type=0
    elif (me.shape[0]==2**m): # m-orthotope
      self.type=1;
    else:
      raise NameError('Trouble with "me" dimension!')
    self.nq=q.shape[1]
    self.nme=me.shape[1]
    self.color=color
    self.label=label
        
  def __repr__(self):
    strret = ' %s object \n'%self.__class__.__name__ 
    if self.type==0:
      strret += '    type : simplicial\n'
    else:
      strret += '    type : orthotope\n'
    strret += '       d : %d\n'%self.d 
    strret += '       m : %d\n'%self.m
    strret += '       q : (%d,%d)\n'%self.q.shape
    strret += '      me : (%d,%d)\n'%self.me.shape
   # strret += 'toGlobal : (%d,)\n'%self.toGlobal.shape
    return strret  
  
  if isMatplotlib():
    from .matplotlib import plotmesh
 
   
def LabelBaseName(d,m):
  if (m==d):
    return r"\Omega"
  if (m+1==d):
    return r"\Gamma"
  if (m+2==d):
    return r"\partial\Gamma"
  return r"\partial^{%d}\Gamma"%(d-m-1)