#from . import operators
#from .FEMOptV3 import *
#from .FEMtools import getVFindices
#from .BVP import BVP
#from .PDEelt import PDEelt

from fc_simesh.siMesh import siMesh
from fc_simesh.siMeshElt import siMeshElt

import numpy as np
from scipy import linalg
from scipy import sparse
import scipy.sparse.linalg as splinalg
import itertools
import types
from math import *

from fc_vfemp1 import operators
from fc_vfemp1.FEMOptV3 import *
from fc_vfemp1.FEMtools import getVFindices
from fc_vfemp1.BVP import BVP,PDE

def  AssemblyP1(Th,Op,**kwargs):
  #dtype=kwargs.get('dtype',float)
  if isinstance(Th,siMeshElt):
    return AssemblyP1_siMeshElt(Th,Op,**kwargs)
    #version=kwargs.get('version', 'OptV3') 
    #if operators.isoperatorL(Op):
      #return globals()['DAssemblyP1_'+version](Th,Op,**kwargs)
    #if operators.isoperatorH(Op):
      #return globals()['HAssemblyP1_'+version](Th,Op,**kwargs)
  if isinstance(Th,siMesh):
    return AssemblyP1_siMesh(Th,Op,**kwargs)
    #bvp=BVP(Th,PDEelt(Op))
    #A,b=bvp.Assembly(Robin=False,Dirichlet=False)
    #return A
  assert False, 'Unknow Mesh %s or Operator %s '%(type(Yh),type(Op))
  
def  AssemblyP1_siMesh(Th,Op,**kwargs):
  assert isinstance(Th,siMesh)
  if operators.isoperatorL(Op):
    return AssemblyP1_siMesh_Loperator(Th,Op,**kwargs)
  if operators.isoperatorH(Op):
    return AssemblyP1_siMesh_Hoperator(Th,Op,**kwargs)
  assert False, 'Unknow operator : %s'%type(Op)
  
def AssemblyP1_siMesh_Loperator(Th,Op,**kwargs):
  assert isinstance(Th,siMesh) and operators.isoperatorL(Op)
  version=kwargs.pop('version', 'OptV3') 
  d=kwargs.pop('d',Th.d)
  all_labels=Th.sThlab[Th.find(d)]
  labels=kwargs.pop('labels',all_labels)
  dtype=kwargs.get('dtype',float)
  local=kwargs.get('local',False)
  if np.isscalar(labels):
    labels=[labels] # must be iterable
    nlab=1
  else:
    nlab=len(labels)
  if local:
    A=operators.NoneVector(nlab)
    toGlobal=operators.NoneVector(nlab)
  else:
    A=sparse.csc_matrix((Th.nq,Th.nq),dtype=dtype)
  for i in range(nlab):
    lab=labels[i]
    idx=Th.find(d,labels=lab)
    if idx is not None:
      A_lab=AssemblyP1_siMeshElt_Loperator(Th.sTh[idx],Op,**kwargs)
      if local:
        A[i]=A_lab
        toGlobal[i]=Th.sTh[idx].toGlobal
      else:
        toGlobal=Th.sTh[idx].toGlobal
        A=sum_sub_mat(A,A_lab,toGlobal,toGlobal)
  if local:
    return A,toGlobal
  else:
    return A

def AssemblyP1_siMesh_Hoperator(Th,Op,**kwargs):
  assert isinstance(Th,siMesh) and operators.isoperatorH(Op)
  #version=kwargs.pop('version', 'OptV3') 
  #d=kwargs.pop('d',Th.d)
  #all_labels=Th.sThlab[Th.find(d)
  #labels=kwargs.pop('labels',all_labels)
  dtype=kwargs.get('dtype',float)
  block=kwargs.get('block',False)
  local=kwargs.pop('local',False)
  if not block:
    local=False
  #Num=kwargs.get('Num',1)
  #if np.isscalar(labels):
    #labels=[labels] # must be iterable
    #nlab=1
  #else:
    #nlab=len(labels)
  m=Op.m
  if block:
    A=operators.NoneMatrix(m,m)
  else:
    A=sparse.csc_matrix((m*Th.nq,m*Th.nq),dtype=dtype)
    VFInd=getVFindices(Num,self.m,self.Th.nq)
  if block and local:
    for i in range(m):
      for j in range(m):
         A[i][j],toGlobal[i][j]=AssemblyP1_siMesh_Loperator(Th,Op.H[i][j],local=True,**kwargs)
    return A,toGlobal
  if block:
    for i in range(m):
      for j in range(m):
         A[i][j]=AssemblyP1_siMesh_Loperator(Th,Op.H[i][j],local=False,**kwargs)
    return A,toGlobal
  # Else not block and not local
  A=sparse.csc_matrix((m*Th.nq,m*Th.nq),dtype=dtype)
  VFInd=getVFindices(Num,self.m,self.Th.nq)
  Ind=np.arange(Th.nq)
  for i in range(m):
    I=VFInd(Ind,i)
    for j in range(m):
      J=VFInd(Ind,j)
      Aii=AssemblyP1_siMesh_Loperator(Th,Op.H[i][j],local=False,**kwargs)
      A=sum_sub_mat(A,Ai,I,J)
  return A

def  AssemblyP1_siMeshElt(sTh,Op,**kwargs):
  assert isinstance(sTh,siMeshElt)
  if operators.isoperatorL(Op):
    return AssemblyP1_siMeshElt_Loperator(sTh,Op,**kwargs)
  if operators.isoperatorH(Op):
    return AssemblyP1_siMeshElt_Hoperator(sTh,Op,**kwargs)
  assert False, 'Unknow operator : %s'%type(Op)

def  AssemblyP1_siMeshElt_Loperator(sTh,Op,**kwargs):
  #dtype=kwargs.get('dtype',float)
  assert isinstance(sTh,siMeshElt) and operators.isoperatorL(Op)
  version=kwargs.get('version', 'OptV3') 
  return globals()['DAssemblyP1_'+version](sTh,Op,**kwargs)
  
def  AssemblyP1_siMeshElt_Hoperator(sTh,Op,**kwargs):
  #dtype=kwargs.get('dtype',float)
  assert isinstance(sTh,siMeshElt) and operators.isoperatorH(Op)
  version=kwargs.get('version', 'OptV3') 
  return globals()['HAssemblyP1_'+version](sTh,Op,**kwargs)

def Apply(Lop,Th,u,**kwargs):
  # perm=lambda A: scipy.sparse.csgraph.reverse_cuthill_mckee(A)
  assert( isinstance(Th,siMesh) )
  solver=kwargs.get('solver', lambda A,b: splinalg.spsolve(A,b))
  perm=kwargs.get('perm', None)
  bvp=BVP(Th,pde=PDE(Op=Lop))
  [A,b]=bvp.Assembly(local=True)
  LopM=operators.Loperator(dim=Lop.dim,d=Lop.d,a0=1)
  bvp=BVP(Th,pde=PDE(Op=LopM))
  [M,b]=bvp.Assembly(local=True)
  u=u.reshape((u.shape[0],))
  b=A*u
  if perm is not None:
    p=perm(M)
    f=np.ndarray((Th.nq,))
    f[p]=solver(M[p,::][::,p],b[p])
  else:
    f=solver(M,b)
  if isinstance(f,tuple):
    info=f[1]
    f=f[0]
  return f

def NormH1(Th,U,**kwargs):
  Num=kwargs.get('Num', 1)
  M=kwargs.get('Mass', None)
  isM=False
  K=kwargs.get('Stiff', None)
  isK=False
  m=len(U)//Th.nq  # division entiere
  if ( m*Th.nq != len(U) ):
    print('dimension error m=%d,nq=%d,len(U)=%d'%(m,Th.nq,len(U)))
  VFNum=getVFindices(Num,m,Th.nq)
  if M!=None:
    assert(isinstance(M,sparse.csc.csc_matrix))
    assert(M.get_shape()==(Th.nq,Th.nq))
  else:
    isM=True
    OpM=operators.Lmass(Th.dim,1.0)
    M=AssemblyP1(Th,OpM)
  if K!=None:
    assert(isinstance(K,sparse.csc.csc_matrix))
    assert(K.get_shape()==(Th.nq,Th.nq))
  else:
    isK=True
    OpS=operators.Lstiff(Th.dim)
    K=AssemblyP1(Th,OpS)
  S=0.
  I=np.arange(Th.nq)
  for i in range(m):
    UI=np.abs(U[VFNum(I,i)])
    S+=np.dot(M*UI,UI)+np.dot(K*UI,UI)
  if isM and isK:
    return np.sqrt(S),M,K
  if isM:
    return np.sqrt(S),M
  if isK:
    return np.sqrt(S),K
  return np.sqrt(S)

def NormL2(Th,U,**kwargs):
  Num=kwargs.get('Num', 1)
  isRetMat=False
  M=kwargs.get('Mass', None)
  if M!=None:
    assert(isinstance(M,sparse.csc.csc_matrix))
    assert(M.get_shape()==(Th.nq,Th.nq))
  else:
    isRetMat=True
    OpM=operators.Lmass(Th.dim,1.0)
    M=AssemblyP1(Th,OpM)
  m=round(U.shape[0]/Th.nq)
  assert(m*Th.nq==U.shape[0])
  VFNum=getVFindices(Num,m,Th.nq)
  S=0.
  I=np.arange(Th.nq)
  for i in range(m):
    UI=np.abs(U[VFNum(I,i)])
    S+=np.dot(M*UI,UI)
  if isRetMat:
    return np.sqrt(S),M
  else:
    return np.sqrt(S)

def Assembly_pde(pde,sTh,**kwargs):
  assert isinstance(pde,PDE)
  assert isinstance(sTh,siMeshElt)
  assert (pde.dim == sTh.dim)
  local=kwargs.get('local',True)
  Num=kwargs.get('Num',1)
  block=kwargs.get('block',False)
  #if isinstance(pde.Op,Loperator):
  if pde.m==1:
    if pde.Op is None:
      A=None
    else:
      A=FEM.DAssemblyP1_OptV3(sTh,pde.Op,local=local)
    if pde.f is not None:
      Mop=Loperator(dim=sTh.dim,d=sTh.d,a0=pde.f)
      M=FEM.DAssemblyP1_OptV3(sTh,Mop)
      f=M.sum(axis=1)
      if local:
        b=f
      else:
        b=np.zeros((sTh.nqParent,1))
        b[sTh.toParent]=f
    else:
      if local:
        b=np.zeros((sTh.nq,1))
      else:
        b=np.zeros((sTh.nqParent,1))
    if block:
      A=[A];b=[b]
    return A,b
  if isinstance(pde.Op,Hoperator):
    A=FEM.HAssemblyP1_OptV3(sTh,pde.Op,local=local,Num=Num,block=block)
    b=FEM.RHSAssembly(sTh,pde.f,m=pde.m,local=local,Num=Num,block=block)
    #print('TODO : %s line %d'%(os.path.basename(__file__),__line__))
    #print('  -> function not implemented for Hoperator')
  return A,b

def Gradient(Th,u,**kwargs):
  U=Th.eval(u)
  dim=Th.dim
  solver=kwargs.pop('solver', lambda A,b: splinalg.spsolve(A,b))
  perm=kwargs.pop('perm', None)
  # Compute Mass matrix (M)
  Lop=operators.Loperator(dim=dim,a0=1)
  M=AssemblyP1(Th,Lop)
  if perm is not None:
    p=perm(M)
    M=M[p,::][::,p]
  # Compute V=Grad(u)
  V=np.ndarray((dim,U.shape[0]))
  for i in range(dim):
    c=dim*[None];c[i]=1
    Lop=operators.Loperator(dim=dim,c=c)
    A=AssemblyP1(Th,Lop)
    b=A*U
    if perm is not None:
      b=b[p]
    V[i]=solver(M,b,**kwargs)
    if perm is not None:
      V[i,p]=V[i]    
  return V

def sum_sub_mat(A,Ai,tgr,tgc):
  if Ai is None:
    return A
  if A.shape==Ai.shape:
    return A+Ai
  (I,J,K)=sparse.find(Ai)
  A+=sparse.csc_matrix((K,(tgr[I],tgc[J])),shape=A.shape)
  return A

def csr_zero_rows(A, rows_to_zero):
  if not isinstance(A, sparse.csc_matrix):
    raise ValueError('Matrix given must be of CSR format.')
  mask=np.in1d(A.indices, rows_to_zero)
  A.data[mask]=0
  #A.eliminate_zeros()
  #A.eliminate_zeros()
