import numpy as np
from scipy import sparse
import scipy.sparse.linalg as splinalg


#from fc_simesh.siMesh import siMesh
##from fc_vfemp1 import PDEelt as Pt
#from fc_vfemp1.FEMtools import getVFindices
#from fc_vfemp1.operators import Loperator,Hoperator,check_data,is_Loperator,is_Hoperator

class PDE:
  def __init__(self,**kwargs):
    Op=kwargs.pop('Op',None)
    f=kwargs.pop('f',None)
    dim=kwargs.pop('dim',2)
    m=kwargs.pop('m',1)
    assert len(kwargs)==0,'Unknow key arguments %s'%(", ".join([key for key in kwargs.keys()]))
      
    #delta=kwargs.get('delta',np.zeros((self.m,)))
    if Op is not None:
      assert is_Loperator(Op) or is_Hoperator(Op)
      dim=Op.dim
      m=Op.m
    else:
      if m==1:
        Op=Loperator(dim=dim)
      else:
        Op=Hoperator(dim=dim,m=m)
    self.Op=Op  
    self.dim=dim
    self.d=dim # unused
    self.m=m
    self.delta=np.zeros((self.m,)) # unused (prevision for generalized boundary condition)
    self.f=None
    if f is not None:
      if m==1:
        assert is_function_data(f)
        self.f=f
      else:
        assert isinstance(f,list) and len(f)==m
        self.f=m*[None]
        for i in range(m):
          self.f[i]=check_data(f[i])
    
       
    #assert len(args)==1 or len(args)==2
    #if len(args)==1:
      #Op=args[0]
      #assert isinstance(Op,Loperator) or isinstance(Op,Hoperator) 
      #self.dtype=kwargs.get('dtype', float)
      #self.dim=Op.dim
      #self.d=Op.d
      #self.m=Op.m
      #self.Op=Op
      #self.delta=kwargs.get('delta',np.zeros((self.m,)))
      #self.f=None
      #f=kwargs.get('f',None)
      #if f is None:
        #return      
      #if isinstance(f,list):
        #assert(len(f)==self.m)
        #self.f=f
      #else:
        #self.f=[]
        #for i in range(self.m):
          #self.f.append(f)
      #return 
    #if len(args)==2:
      #dim=args[0]
      #m=args[1]
      #if m==1:
        #self.Op=Loperator(dim=dim)
      #else:
        #self.Op=Hoperator(dim=dim,m=m)

  def __str__(self,**kwargs):
    indent=kwargs.pop('indent','')    
    strret = indent+' %s object : (dim,m) = (%d,%d)\n'%(self.__class__.__name__,self.dim,self.m)
    #strret += '      d : %d\n'%self.d 
    #strret += '    dim : %d\n'%self.dim
    #strret += '      m : %d\n'%self.m
    strret += indent+'     Op : %s\n'%(self.Op.__repr__(indent=4*' '))         #self.Op.__class__.__name__
    strret += indent+'      f : '+str(self.f)+'\n'
    if isinstance(self.delta,np.ndarray):
      strret += indent+'  delta : '+np.array_str(self.delta).replace('\n','\n          ')
    else:
      strret += indent+'  delta : '+str(self.delta)
    return strret
  
  def __repr__(self,**kwargs):
    return self.__str__(**kwargs)
  
  #-> FEM.assembly_pde
  def Assembly(self,sTh,**kwargs):
    from fc_vfemp1 import FEM
    assert isinstance(sTh,siMeshElt) and self.dim == sTh.dim
    #assert( (self.dim == sTh.dim) and (self.d == sTh.d) )
    local=kwargs.get('local',True)
    Num=kwargs.get('Num',1)
    block=kwargs.get('block',False)
    #if isinstance(self.Op,Loperator):
    if self.m==1:
      if self.Op is None:
        A=None
      else:
        #A=FEM.DAssemblyP1_OptV3new(sTh,self.Op,local=local)
        A=FEM.AssemblyP1(sTh,self.Op,**kwargs)
      if self.f is not None:
        Mop=Loperator(dim=sTh.dim,d=sTh.d,a0=self.f)
        #M=FEM.DAssemblyP1_OptV3new(sTh,Mop)
        M=FEM.AssemblyP1(sTh,Mop,**kwargs)
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
    if isinstance(self.Op,Hoperator):
      A=FEM.HAssemblyP1_OptV3(sTh,self.Op,local=local,Num=Num,block=block)
      b=FEM.RHSAssembly(sTh,self.f,m=self.m,local=local,Num=Num,block=block)
      #print('TODO : %s line %d'%(os.path.basename(__file__),__line__))
      #print('  -> function not implemented for Hoperator')
    return A,b

class BVP:
  def __init__(self,Th,**kwargs):
    assert isinstance(Th,siMesh)
    pde = kwargs.get('pde',None)
    labels = kwargs.get('labels',None)
    if pde is not None:
      assert isinstance(pde,PDE) and Th.dim == pde.dim 
      m=pde.m
    else:
      m = kwargs.get('m',1)
    self.dim=Th.dim
    self.d=Th.d
    self.Th=Th
    self.m=m
    self.ndof=self.m*Th.nq # only P1
    
    if labels is None:
      idxlab=Th.find(Th.d)
    else:
      idxlab=Th.find(Th.d,labels)
    self.pdes=[None]*Th.nsTh
    if pde is not None:
      for i in idxlab:
        self.pdes[i]=pde
    
  def __repr__(self):    
    strret = ' %s object \n'%self.__class__.__name__
    strret += '      d : %d\n'%self.d 
    strret += '    dim : %d\n'%self.dim
    strret += '      m : %d\n'%self.m
    strret += '     Th : %s\n'%self.Th.__class__.__name__
    strret += '   ndof : %d\n'%self.ndof
    #strret += '  delta : '+np.array_str(self.delta).replace('\n','\n          ')+'\n' 
    return strret
    
  def setDirichlet(self,label,fun,**kwargs):
    #comps=kwargs.get('comps',np.arange(1,self.m+1))
    comps=kwargs.get('comps',np.arange(self.m))
    idxlab=self.Th.find(self.d-1,labels=label)
    assert idxlab is not None,'labels %s not found'%str(label)
    LopD=Loperator(dim=self.dim,d=self.d-1,a0=1)
    if self.pdes[idxlab] is None:
      self.pdes[idxlab]=PDE(dim=self.dim,m=self.m)
    if self.m==1:
      self.pdes[idxlab].Op=LopD
      self.pdes[idxlab].f=check_data(fun)
      self.pdes[idxlab].delta=0
    else:
      i=0
      for cp in comps:
        # l=cp-1
        l=cp
        self.pdes[idxlab].delta[l]=0
        self.pdes[idxlab].Op.H[l][l]=LopD
        if self.pdes[idxlab].f is None:
          self.pdes[idxlab].f=self.m*[None]
        if isinstance(fun,list):
          self.pdes[idxlab].f[l]=check_data(fun[i])
        else:
          self.pdes[idxlab].f[l]=check_data(fun)
        i=i+1
  
  def setRobin(self,label,fun,**kwargs):
    #comps=kwargs.get('comps',np.arange(1,self.m+1))
    comps=kwargs.get('comps',np.arange(self.m))
    ar=kwargs.get('ar',None) # By default Neumann
    idxlab=self.Th.find(self.d-1,labels=label)
    if idxlab is None:
      print('Error with setRobin: ...')
      return
    if ar is None:
      LopD=None
    else:
      LopD=Loperator(dim=self.dim,d=self.d-1,a0=ar)
      
    if self.pdes[idxlab] is None:
      self.pdes[idxlab]=PDE(dim=self.dim,m=self.m)
    if self.m==1:
      self.pdes[idxlab].Op=LopD
      self.pdes[idxlab].f=check_data(fun)
      self.pdes[idxlab].delta=1
    else:
      i=0
      for cp in comps:
        #l=cp-1
        l=cp
        self.pdes[idxlab].delta[l]=1
        self.pdes[idxlab].Op.H[l][l]=LopD
        if self.pdes[idxlab].f is None:
          self.pdes[idxlab].f=self.m*[None]
        if isinstance(fun,list):
          self.pdes[idxlab].f[l]=check_data(fun[i])
        else:
          self.pdes[idxlab].f[l]=check_data(fun)
        i=i+1
  
  def setPDE(self,pde,**kwargs):
    d=kwargs.pop('d',self.d)
    assert self.dim==pde.dim and self.m == pde.m
    labels=kwargs.pop('labels',self.Th.find(d))
    idxlab=self.Th.find(d,labels=labels)
    assert idxlab is not None,'mesh label(s) not found'
    if np.isscalar(idxlab):
      self.pdes[idxlab]=pde
    else:
      for idx in idxlab:
        self.pdes[idx]=pde
    
  
  def Assembly(self,**kwargs):
    dtype=kwargs.get('dtype',float)
    local=kwargs.get('local',False)
    Num=kwargs.get('Num',1)
    dom=kwargs.get('dom',True)
    physical=kwargs.get('physical',True)
    interface=kwargs.get('interface',False)
    Robin=kwargs.get('Robin',True)
    Dirichlet=kwargs.get('Dirichlet',True)
    A=sparse.csc_matrix((self.ndof,self.ndof),dtype=dtype)
    b=np.zeros((self.ndof,1))
    VFInd=getVFindices(Num,self.m,self.Th.nq)
    if dom:
      idxlab=self.Th.find(self.Th.d)
      A,b=Assembly_main(self,A,b,VFInd,idxlab,local)
    if Robin:
      A,b=Assembly_BC(self,A,b,VFInd,physical,interface,Assembly_Robin)
    if Dirichlet: 
      A,b=Assembly_BC(self,A,b,VFInd,physical,interface,Assembly_Dirichlet)
  
    return A,b
  
  def splitsol(self,X,**kwargs):
    Num=kwargs.get('Num',1)
    if self.m==1:
      return X
    VFInd=getVFindices(Num,self.m,self.Th.nq)
    x=self.m*[None]
    I=np.arange(self.Th.nq)
    for i in range(self.m):
      x[i]=X[VFInd(I,i)]
    return x
    
  def solve( self, **kwargs):
    # perm=lambda A: scipy.sparse.csgraph.reverse_cuthill_mckee(A)
    split=kwargs.get('split',False)
    solver=kwargs.get('solver', lambda A,b: splinalg.spsolve(A,b))
    perm=kwargs.get('perm', None)
    A,b=self.Assembly()
    #A.eliminate_zeros()
    b=b.reshape((b.shape[0],))
    if perm is not None:
      p=perm(A)
      x=np.ndarray((self.ndof,))
      x[p]=solver(A[p,::][::,p],b[p])
    else:
      x=solver(A,b)
    if isinstance(x,tuple):
      info=x[1]
      x=x[0]
    #res=np.max(np.abs(A*x-b))
    #print('Residu : %.16f',res)
    if split:
      x=self.splitsol(x)
    return x
  
  
# A(tgr,tgc) <- A(tgr,tgc)+Ai
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
  
  
# A(tgr,:) <- 0 
# A(tgr,tgc) <- Ai
def dirichlet_mat(A,Ai,tgr,tgc):
  (I,J,K)=sparse.find(Ai)
  if tgr.ndim==0: # tgr is np.array(0) for example
    tgr=tgr.reshape((1,))
  if tgc.ndim==0:
    tgc=tgc.reshape((1,))
  csr_zero_rows(A,tgr)
  A+=sparse.csc_matrix((K,(tgr[I],tgc[J])),shape=A.shape)
  return A
  
def Assembly_main(self,A,b,VFInd,idxlab,local):
  block=self.m>1
  if np.isscalar(idxlab):
    idxlab=[idxlab]
  for i in idxlab:
    if self.pdes[i] is not None:
      Ai,bi=self.pdes[i].Assembly(self.Th.sTh[i],local=local,block=block)
      #print(Ai[0][1])
      if Ai is not None:
        if block:
          for l in np.arange(self.m):
            tgl=VFInd(self.Th.sTh[i].toParent,l)
            for s in np.arange(self.m):
              if Ai[l][s] is not None:
                tgs=VFInd(self.Th.sTh[i].toParent,s)
                A=sum_sub_mat(A,Ai[l][s],tgl,tgs)
            if bi[l] is not None:
              b[tgl]=b[tgl]+bi[l]
        else:
          tg=VFInd(self.Th.sTh[i].toParent,0)
          #print(tg)
          #A[tg,:][:,tg]=A[tg,:][:,tg]+Ai
          A=sum_sub_mat(A,Ai,tg,tg)
        
          if bi is not None:
            if bi.shape==b.shape:
              b+=bi
            else:
              b[tg]+=bi
  #print(A)
  return A,b

def Assembly_BC(self,A,b,VFInd,physical,interface,Assemblyfun):
  for dd in np.arange(self.Th.d-1,-1,-1):
    Allidxlab=self.Th.find(dd)
    if Allidxlab is not None:
      idxlab=np.array([],dtype=int)
      if physical:
        I=np.where((self.Th.sThlab[Allidxlab]>=0) & (self.Th.sThlab[Allidxlab]<10000))[0]
        idxlab=np.concatenate((idxlab,Allidxlab[I]))
      if interface:
        I=np.where((self.Th.sThlab(Allidxlab)<0) | (self.Th.sThlab(Allidxlab)>=10000))[0]
        idxlab=np.concatenate((idxlab,Allidxlab[I]))
      
      if len(idxlab)>0:
        [A,b]=Assemblyfun(self,A,b,VFInd,idxlab)
  return A,b

def Assembly_Robin(self,A,b,VFInd,idxlab):
  block=self.m>1
  #print(idxlab)
  for i in idxlab:
    #print(i)
    if self.pdes[i] is not None:
      #print(self.pdes[i])
      #print(self.Th.sTh[i])
      #Ai,bi=self.pdes[i].Assembly(self.Th.sTh[i],block=block)
      BB=self.pdes[i].Assembly(self.Th.sTh[i],block=block,local=True)
      if BB is not None:
        Ai,bi=BB
        if self.m>1:
          for l in np.arange(self.m):
            if self.pdes[i].delta[l]==1: # Robin
              tgl=VFInd(self.Th.sTh[i].toParent,l)   
              for k in np.arange(self.m):
                if Ai[l][k] is not None:
                  tgk=VFInd(self.Th.sTh[i].toParent,k)
                  #A[tgl,:][:,tgk]=A[tgl,:][:,tgk]+Ai[l,k]
                  A=sum_sub_mat(A,Ai[l][k],tgl,tgk)
              if bi[l] is not None:
                b[tgl]=b[tgl]+bi[l]
        else:
          if self.pdes[i].delta==1:
            tg=self.Th.sTh[i].toParent
            A=sum_sub_mat(A,Ai,tg,tg)
            if bi is not None:
              b[tg]=b[tg]+bi
  return A,b

def Assembly_Dirichlet(self,A,b,VFInd,idxlab):
  #print('Dirichlet')
  block=self.m>1
  for i in idxlab:
    #print(i)
    if self.pdes[i] is not None:
      BB=self.pdes[i].Assembly(self.Th.sTh[i],block=block,local=True)
      if BB is not None:
        Ai,bi=BB
        if self.m>1:
          for l in np.arange(self.m):
            if self.pdes[i].delta[l]==0: # Dirichlet
              tgl=VFInd(self.Th.sTh[i].toParent,l)   
              for k in np.arange(self.m):
                if Ai[l][k] is not None:
                  tgk=VFInd(self.Th.sTh[i].toParent,k)
                  A=dirichlet_mat(A,Ai[l][k],tgl,tgk)
              if bi[l] is not None:
                b[tgl]=bi[l]
        else:
          if self.pdes[i].delta==0:
            tg=self.Th.sTh[i].toParent
            A=dirichlet_mat(A,Ai,tg,tg)
            if bi is not None:
              b[tg]=bi
  return A,b

from fc_simesh.siMesh import siMesh
from fc_simesh.siMeshElt import siMeshElt
#from fc_vfemp1 import PDEelt as Pt
from fc_vfemp1.FEMtools import getVFindices
from fc_vfemp1.operators import Loperator,Hoperator,check_data,is_function_data,is_Loperator,is_Hoperator
