from math import factorial
from scipy import sparse
import numpy as np

from fc_simesh.siMeshElt import siMeshElt

from . import FEMtools
from . import operators

#def DAssemblyP1_OptV3(sTh,Lop,**kwargs):
  #dtype=kwargs.get('dtype',float)
  #Kg=KgP1_OptV3(sTh,Lop,dtype=dtype)
  #Ig,Jg=IgJgP1_OptV3(sTh.d,sTh.nme,sTh.me)
  #N=sTh.nme*(sTh.d+1)**2
  #A=sparse.csc_matrix((np.reshape(Kg,N),(np.reshape(Ig,N),np.reshape(Jg,N))),shape=(sTh.nq,sTh.nq))
  #A.eliminate_zeros()
  #return A

#def DAssemblyP1_OptV3new(sTh,Lop,**kwargs):
def DAssemblyP1_OptV3(sTh,Lop,**kwargs):
  assert(isinstance(sTh, siMeshElt))
  assert(isinstance(Lop, operators.Loperator))
  dtype=kwargs.get('dtype',float)
  local=kwargs.get('local',False)
  Kg=KgP1_OptV3(sTh,Lop,dtype=dtype)
  if local:
    ndof=sTh.nq
    Ig,Jg=IgJgP1_OptV3(sTh.d,sTh.nme,sTh.me)
  else:
    ndof=sTh.nqParent
    Ig,Jg=IgJgP1_OptV3(sTh.d,sTh.nme,sTh.toParent[sTh.me])
  N=sTh.nme*(sTh.d+1)**2
  A=sparse.csc_matrix((np.reshape(Kg,N),(np.reshape(Ig,N),np.reshape(Jg,N))),shape=(ndof,ndof))
  A.eliminate_zeros()
  return A
  
def HAssemblyP1_OptV3(sTh,Hop,**kwargs):
  assert(isinstance(sTh, siMeshElt))
  assert(isinstance(Hop, operators.Hoperator))
  dtype=kwargs.get('dtype',float)
  spformat=kwargs.get("spformat", "csc")
  local=kwargs.get('local',True)
  Num=kwargs.get('Num',1)
  block=kwargs.get('block',True)
  
  if local:
    nq=sTh.nq
    Ig,Jg=IgJgP1_OptV3(sTh.d,sTh.nme,sTh.me)
  else:
    nq=sTh.nqGlobal
    Ig,Jg=IgJgP1_OptV3(sTh.d,sTh.nme,sTh.toGlobal[sTh.me])
  N=sTh.nme*(sTh.d+1)**2
  Ig=np.reshape(Ig,N)
  Jg=np.reshape(Jg,N)
  
  m=Hop.m;ndof=m*nq
  VFInd=FEMtools.getVFindices(Num,m,nq) 
  if block:
    #M=m*[m*[None]] # Failed all lines points to the same line
    M=FEMtools.NoneMatrix(m,m)
  else:
    M=sparse.csc_matrix((ndof,ndof),dtype=dtype)
  
  for i in range(m):
    for j in range(m):
      if Hop.H[i][j] is not None:
        Kg=np.reshape(KgP1_OptV3(sTh,Hop.H[i][j],dtype=dtype),N)
        if block:
          M[i][j]=sparse.csc_matrix((Kg,(Ig,Jg)),shape=(nq,nq),dtype=dtype)
        else:  
          M=M+sparse.csc_matrix((Kg,(VFNum(Ig,i),VFNum(Jg,j))),shape=(ndof,ndof),dtype=dtype)
      #print('*** i=%d,j=%d'%(i,j))
      #print(M)
  if (spformat=="csc"):
    return M
  else:
    return eval("M.to%s()"%spformat, globals(), locals())
  
def RHSAssembly(sTh,f,**kwargs):
  assert(isinstance(sTh, siMeshElt))
  dtype=kwargs.get('dtype',float)
  #spformat=kwargs.get("spformat", "csc")
  local=kwargs.get('local',True)
  Num=kwargs.get('Num',1)
  block=kwargs.get('block',True)
  m=kwargs.get('m',1)
  if local:
    nq=sTh.nq
  else:
    nq=sTh.nqGlobal
    
  #N=sTh.nme*(sTh.d+1)**2
  ndof=m*nq
  #VFInd=FEMtools.getVFindices(Num,m,nq) 
  if block:
    b=FEMtools.NoneVector(m)
  else:
    b=np.zeros((ndof,1))
  if f is None:
    return b
  if (m==1) and not (isinstance(f,list)):
    f=[f]
  VFInd=FEMtools.getVFindices(Num,m,nq)   
  Mop=operators.Loperator(dim=sTh.dim,d=sTh.d,a0=1)
  M=DAssemblyP1_OptV3(sTh,Mop,local=True)
  if not block:
    I=np.arange(sTh.nq)
  for i in range(m):
    if f[i] is not None:
      fh=sTh.feval(f[i]).reshape((sTh.nq,1))
      Fh=M*fh
      if block:
        b[i]=Fh
      else:
        b[VFInd(I,i)]=Fh
  return b

def IgJgP1_OptV3(d,nme,me):
  ndfe=d+1
  Ig=np.zeros((nme,ndfe,ndfe),dtype=np.int32)
  Jg=np.zeros((nme,ndfe,ndfe),dtype=np.int32)
  for il in range(ndfe):
    mel=me[il]
    for jl in range(ndfe):
      Ig[:,il,jl]=Jg[:,jl,il]=mel
  return Ig,Jg
  
def KgP1_OptV3(sTh,Lop,**kwargs):
  d=sTh.d;ndfe=d+1
  dtype=kwargs.get('dtype', float)
  Kg=np.zeros((sTh.nme,ndfe,ndfe),dtype)
  Kg=Kg+KgP1_OptV3_guv(sTh,Lop.a0,dtype)
  if (Lop.get_order()==0):
    return Kg
  if Lop.A is not None:
    for i in range(d):
      for j in range(d):
          Kg=Kg+KgP1_OptV3_gdudv(sTh,Lop.A[i][j],j,i,dtype)
  if Lop.b is not None:
    for i in range(d):
        Kg=Kg-KgP1_OptV3_gudv(sTh,Lop.b[i],i,dtype)
  if Lop.c is not None:
    for i in range(d):
        Kg=Kg+KgP1_OptV3_gduv(sTh,Lop.c[i],i,dtype)
  return Kg
  
def KgP1_OptV3_guv(sTh,g,dtype):
  if g is None: return 0
  gh=FEMtools.setFdata(g,sTh,dtype=dtype)
  d=sTh.d;ndfe=d+1
  Kg=np.zeros((sTh.nme,ndfe,ndfe),dtype=dtype)
  gme=gh[sTh.me]
  gs=(gme.sum(axis=0)).reshape(sTh.nme)
  KgElem=lambda il,jl: (factorial(d)/float(factorial(d+3)))*(1+(il==jl))*sTh.vols*(gs+gme[il]+gme[jl])
  for il in range(ndfe):
    for jl in range(ndfe):
      Kg[:,il,jl]=KgElem(il,jl)
  return Kg

def KgP1_OptV3_gdudv(sTh,g,i,j,dtype):
  if g is None: return 0
  G=sTh.GradBaCo
  gh=FEMtools.setFdata(g,sTh,dtype=dtype)
  d=sTh.d;ndfe=d+1
  Kg=np.zeros((sTh.nme,ndfe,ndfe),dtype=dtype)
  gme=gh[sTh.me]
  gs=(gme.sum(axis=0)).reshape(sTh.nme)
  KgElem=lambda il,jl: (factorial(d)/float(factorial(d+1)))*sTh.vols*gs*G[:,jl,i]*G[:,il,j]
  for il in range(ndfe):
    for jl in range(ndfe):
      Kg[:,il,jl]=KgElem(il,jl)
  return Kg
  
def KgP1_OptV3_gudv(sTh,g,i,dtype):
  if g is None: 
    return 0
  G=sTh.GradBaCo
  gh=FEMtools.setFdata(g,sTh,dtype=dtype)
  d=sTh.d;ndfe=d+1
  Kg=np.zeros((sTh.nme,ndfe,ndfe),dtype=dtype)
  gme=gh[sTh.me]
  gs=(gme.sum(axis=0)).reshape(sTh.nme)
  KgElem=lambda il,jl: (factorial(d)/float(factorial(d+2)))*sTh.vols*(gs+gme[jl])*G[:,il,i]
  for il in range(ndfe):
    for jl in range(ndfe):
      Kg[:,il,jl]=KgElem(il,jl)
  return Kg
  
def KgP1_OptV3_gduv(sTh,g,i,dtype):
  if g is None: 
    return 0
  G=sTh.GradBaCo
  gh=FEMtools.setFdata(g,sTh,dtype=dtype)
  d=sTh.d;ndfe=d+1
  Kg=np.zeros((sTh.nme,ndfe,ndfe),dtype=dtype)
  gme=gh[sTh.me]
  gs=(gme.sum(axis=0)).reshape(sTh.nme)
  KgElem=lambda il,jl: (factorial(d)/float(factorial(d+2)))*sTh.vols*(gs+gme[il])*G[:,jl,i]
  for il in range(ndfe):
    for jl in range(ndfe):
      Kg[:,il,jl]=KgElem(il,jl)
  return Kg
