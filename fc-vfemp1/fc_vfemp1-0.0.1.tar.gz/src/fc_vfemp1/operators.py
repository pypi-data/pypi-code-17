import numpy as np
import types
from scipy.sparse.linalg import spsolve

from fc_simesh.siMesh import siMesh
from fc_tools.others import func2str,is_function,is_lambda_function,is_def_function

def is_function_data(f):
  return is_function(f) or np.isscalar(f) or isinstance(f,np.ndarray) or (f is None)

def check_data(f):
  assert is_function_data(f) or isinstance(f,np.ndarray)
  if is_lambda_function(f) or is_def_function(f):
    f=np.vectorize(f)
  return f
      
def check_vector(b,dim):
  assert b is None or isinstance(b,list) or isinstance(b,np.ndarray)
  if b is None:
    return b
  if isinstance(b,list):
    assert len(b)==dim
  if isinstance(b,np.ndarray):
    assert b.shape[0]==dim
  for i in range(dim):
    b[i]=check_data(b[i])
  return b

def check_matrix(A,nl,nc):
  assert A is None or isinstance(A,list)
  if A is None:
    return A
  assert len(A)==nl
  for i in range(nl):
    A[i]=check_vector(A[i],nc)
  return A

class Loperator:
  def __init__(self,**kwargs):
    self.A=None
    self.b=None
    self.c=None
    self.a0=None
    self.dim=kwargs.get('dim', 2)
    self.d=kwargs.get('d', self.dim)
    assert(self.dim>=self.d)
    self.m=1
    #type=kwargs.get('type', None)
    fill=kwargs.get('fill', False)
    self.name=kwargs.get('name', None)
    #self.order=0;
    #if (type=='fill'):
    if fill:
      A =kwargs.get('A', NoneMatrix(self.dim,self.dim))
      b =kwargs.get('b', NoneVector(self.dim))
      c =kwargs.get('c', NoneVector(self.dim))
    else:
      A =kwargs.get('A', None)
      b =kwargs.get('b', None)
      c =kwargs.get('c', None)
    a0=kwargs.get('a0', None)
    self.A=check_matrix(A,self.dim,self.dim)
    self.b=check_vector(b,self.dim)
    self.c=check_vector(c,self.dim)
    self.a0=check_data(a0)
    
  def get_order(self):
    if self.A is not None:
      return 2
    if self.b is not None or self.c is not None :
      return 1
    return 0
      
  def __repr__(self,**kwargs):
    indent=kwargs.pop('indent','')
    full=kwargs.pop('full',True) 
    strret =  'Loperator'
    if isinstance(self.name,str):
      strret =  '[name=%s]'%(self.name)
    strret += ' : (dim,d,order) = (%d,%d,%d)\n'%(self.dim,self.d,self.get_order())
    if full:
      strret += indent+'      A : %s\n'%field2str(self.A)
      strret += indent+'      b : %s\n'%field2str(self.b)
      strret += indent+'      c : %s\n'%field2str(self.c)
      strret += indent+'     a0 : %s'%field2str(self.a0)
      return strret
    isEmpty=True
    if self.A is not None:
      isEmpty=False
      strret += indent+'      A : %s\n'%field2str(self.A)
    if self.b is not None:
      isEmpty=False
      strret += indent+'      b : %s\n'%field2str(self.b)
    if self.c is not None:
      isEmpty=False
      strret += indent+'      c : %s\n'%field2str(self.c)
    if self.a0 is not None:
      isEmpty=False
      strret += indent+'     a0 : %s\n'%field2str(self.a0)
    if isEmpty:
      strret += indent+'     Empty operator\n'
    return strret[:-1]
    
  def __str__(self,**kwargs):      
    return self.__repr__(**kwargs)
  
  def apply(self,Th,u):
    assert( isinstance(Th,siMesh) )
    assert self.A==None and self.b==None, "A and b must be None"
    dim=self.dim
    tmpOp=Loperator(dim=dim,d=self.d,c=self.c,a0=self.a0)
    U=Th.eval(u)
    bvpRHS=BVP(Th,PDEelt(tmpOp))
    A,b=bvpRHS.Assembly(local=True,Robin=False,Dirichlet=False)
    Lop=Loperator(dim=dim,d=self.d,a0=1)
    bvpLHS=BVP(Th,PDEelt(Lop))
    M,b=bvpLHS.Assembly(local=True,Robin=False,Dirichlet=False)
    res=spsolve(M,A*U) # part <Grad(u),c>+a0*u
    ## computation of div(b*u)
    #if self.b is not None:
      #for i in range(dim):
        #if self.b[i] is not None:
          #c=dim*[None];c[i]=1
          #tmpOp=Loperator(dim=dim,d=self.d,c=c)
          #bvpRHS=BVP(Th,PDEelt(tmpOp))
          #A,b=bvpRHS.Assembly(local=True,Robin=False,Dirichlet=False)
          #f=Th.eval(self.b[i])*U
          #res+=spsolve(M,A*f)
    #if self.A is not None:
      ## Compute V=Grad(u)
      #V=[]
      #for i in range(dim):
        #c=dim*[None];c[i]=1
        #tmpOp=Loperator(dim=dim,d=self.d,c=c)
        #bvpRHS=BVP(Th,PDEelt(tmpOp))
        #A,b=bvpRHS.Assembly(local=True,Robin=False,Dirichlet=False)
        #V.append(spsolve(M,A*U))
      #for i in range(dim):
        #if self.A[i] is not None:
          #c=dim*[None];c[i]=1
          #tmpOp=Loperator(dim=dim,d=self.d,c=c)
          #bvpRHS=BVP(Th,PDEelt(tmpOp))
          #A,b=bvpRHS.Assembly(local=True,Robin=False,Dirichlet=False)
          #for j in range(dim):
            #if self.A[i][j] is not None:
              #f=Th.eval(self.A[i][j])*V[j]
              #res+=spsolve(M,A*f)
    
    return res
  
  #def AssemblyP1(self,Th,**kwargs):
    #return FEM.Assembly(Th,self,**kwargs)
    
def check_H(H,m):
  assert isinstance(H,list) and len(H)==m
  for i in range(m):
    assert isinstance(H[i],list) and len(H[i])==m
    for j in range(m):
      assert isinstance(H[i][j],Loperator) or (H[i][j] is None)
  return H

class Hoperator:
  def __init__(self,**kwargs):
    self.dim=kwargs.get('dim', 2)
    self.d=kwargs.get('d', self.dim)
    assert(self.dim>=self.d)
    self.m=kwargs.get('m', 2)
    H=kwargs.get('H', NoneMatrix(self.m,self.m))
    self.name=kwargs.get('name', '')
    self.params=kwargs.get('params', None)
    #self.order=0
    self.H=check_H(H,self.m)
    
  def get_order(self):
    if self.H is None:
      return 0
    order=0
    for i in range(self.m):
      if self.H[i] is not None:
        for j in range(self.m):
          if self.H[i][j] is not None:
            assert isinstance(self.H[i][j],Loperator)
            order=max(order,self.H[i][j].get_order())
            if order==2:
              return order
    return order
  
  def set(self,i,j,Lop):
    assert( i>=0 and i<self.m)
    assert( j>=0 and j<self.m)
    assert is_Loperator(Lop) or Lop is None
    self.H[i][j]=Lop
  
  def apply(self,Th,u):
    assert( isinstance(Th,siMesh) )
    for i in range(self.m):
      for j in range(self.m):
        if self.H[i][j] is not None:
          assert self.H[i][j].A==None and self.H[i][j].b==None, "A and b must be None in all Lopetator"
    bvp=BVP(Th,pde=PDE(Op=self))
    [A,b]=bvp.Assembly()
    Lop=Loperator(dim=self.dim,a0=1)
    Hop=Hoperator(dim=self.dim,m=self.m)
    for i in range(self.m):
      Hop.H[i][i]=Lop
    bvp=BVP(Th,pde=PDE(Op=Hop))
    [M,b]=bvp.Assembly()
    if isinstance(u,list):
      U=np.concatenate(u)
    else:
      U=u
    f=spsolve(M,A*U)
    return bvp.splitsol(f)
  
  def __repr__(self,**kwargs):
    indent=kwargs.pop('indent','')
    strret =  'Hoperator %s: \n'%(self.name)
    strret += indent+'  (dim,d,m) : (%d,%d,%d)\n'%(self.dim,self.d,self.m)
    strret += indent+'      order : %d\n'%self.get_order()
    for i in range(self.m):
      for j in range(self.m):
        strret+= indent+'    H[%d][%d] : '%(i,j)
        if self.H[i][j] is None:
          strret+= 'None\n'
        else:
          strret += self.H[i][j].__str__(indent=(6+len(indent))*' ',full=False) +'\n'
    return strret[:-1]
    
  def __str__(self,*args):      
    return self.__repr__()
    
def isoperatorL(operator):
  return isinstance(operator,Loperator)
  
def isoperatorH(operator):
  return isinstance(operator,Hoperator)

def is_Loperator(operator):
  return isinstance(operator,Loperator)
  
def is_Hoperator(operator):
  return isinstance(operator,Hoperator)

def NoneVector(dim):
  V=[]
  for i in range(dim):
    V.append(None)
  return V
  
def NoneMatrix(m,n):
  M=[]
  for i in range(m):
    M.append(NoneVector(n))
  return M


# Operateurs predefinis
#######################

def Lmass(dim,a0):
  return Loperator(dim=dim,a0=a0,name='MassW')
  
def Lstiff(dim):
  A=NoneMatrix(dim,dim)
  for i in range(dim):
    A[i][i]=1.
  return Loperator(dim=dim,A=A,name='Stiff')
    
def StiffElasHoperator(dim,lam,mu):
  assert dim==2 or dim==3
  assert is_function(lam) or np.isscalar(lam)
  assert is_function(mu) or np.isscalar(mu)
  Hop=Hoperator(dim=dim,m=dim,name='StiffElas',params={'lam':lam,'mu':mu})
  #Hop.order=2;
  gam=None
  if np.isscalar(lam) and np.isscalar(mu):
    gam=lam+2*mu
  if is_function(lam) and np.isscalar(mu):
    if (dim==2): gam=lambda x1,x2 :lam(x1,x2) + 2*mu
    if (dim==3): gam=lambda x1,x2,x3 :lam(x1,x2,x3) + 2*mu
  if is_function(mu) and np.isscalar(lam):
    if (dim==2): gam=lambda x1,x2 :lam + 2*mu(x1,x2)
    if (dim==3): gam=lambda x1,x2,x3 :lam + 2*mu(x1,x2,x3)
  if is_function(mu) and is_function(lam):
    if (dim==2): gam=lambda x1,x2 :lam(x1,x2) + 2*mu(x1,x2)
    if (dim==3): gam=lambda x1,x2,x3 :lam(x1,x2,x3) + 2*mu(x1,x2,x3)
  assert(gam!=None)
    
  if dim==2:
    Hop.H[0][0]=Loperator(dim=dim,A=[[gam,None],[None,mu]]) 
    Hop.H[0][1]=Loperator(dim=dim,A=[[None,lam],[mu,None]]) 
    Hop.H[1][0]=Loperator(dim=dim,A=[[None,mu],[lam,None]]) 
    Hop.H[1][1]=Loperator(dim=dim,A=[[mu,None],[None,gam]])
  if dim==3:
    Hop.H[0][0]=Loperator(dim=dim,A=[[gam,None,None],[None,mu,None],[None,None,mu]]) 
    Hop.H[0][1]=Loperator(dim=dim,A=[[None,lam,None],[mu,None,None],[None,None,None]]) 
    Hop.H[0][2]=Loperator(dim=dim,A=[[None,None,lam],[None,None,None],[mu,None,None]]) 
    Hop.H[1][0]=Loperator(dim=dim,A=[[None,mu,None],[lam,None,None],[None,None,None]]) 
    Hop.H[1][1]=Loperator(dim=dim,A=[[mu,None,None],[None,gam,None],[None,None,mu]])
    Hop.H[1][2]=Loperator(dim=dim,A=[[None,None,None],[None,None,lam],[None,mu,None]])
    Hop.H[2][0]=Loperator(dim=dim,A=[[None,None,mu],[None,None,None],[lam,None,None]])
    Hop.H[2][1]=Loperator(dim=dim,A=[[None,None,None],[None,None,mu],[None,lam,None]])
    Hop.H[2][2]=Loperator(dim=dim,A=[[mu,None,None],[None,mu,None],[None,None,gam]])
  return Hop

def opfunc2str(f):
  if f is None:
    return 'None' # 
  if is_function(f):
    return 'Function'
  if np.isscalar(f):
    return 'Scalar'
  if isinstance(f,np.ndarray):
    return 'Array'
  return 'Unknow'
  
def field2str(f):
  if isinstance(f,list):
    L=[]
    for x in f:
      L.append(field2str(x))
    return str(L).replace("'","")
  return opfunc2str(f)
  
#from fc_vfemp1.PDEelt import PDEelt 
from fc_vfemp1.BVP import BVP,PDE
#from fc_vfemp1 import FEM