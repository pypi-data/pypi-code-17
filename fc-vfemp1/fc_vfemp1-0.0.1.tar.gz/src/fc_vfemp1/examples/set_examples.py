
import fc_oogmsh
from fc_vfemp1.operators import Loperator,Hoperator
from fc_vfemp1.BVP import BVP,PDE
from fc_vfemp1.sys import get_geo
from fc_simesh.siMesh import siMesh,HyperCube
from fc_vfemp1.common import PrintCopyright 

import inspect,types,os

import numpy as np
from numpy import cos,sin,exp,pi
import time,socket
import matplotlib.pyplot as plt
from math import * 

def func2str(u):
  if isinstance(u,types.LambdaType):
    Str=inspect.getsource(u).replace('\n','')
    i=Str.find('=')+1
    return Str[i::]
    #return Str
  else:
    return str(u)

def setBVPStationaryConvectionDiffusion2D01(N,**kwargs):
  env=fc_oogmsh.sys.environment()
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  geodir=kwargs.get('geodir',env.geo_dir)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  geofile='disk3holes'
  af=lambda x,y: 0.1+(y-0.5)*(y-0.5)
  Vx=lambda x,y: -10*y
  Vy=lambda x,y: 10*x
  b=0.01;g2=4;g4=-4;
  f=lambda x,y: -200.0*exp(-((x-0.75)**2+y**2)/(0.1))
  
  if verbose>1:
    PrintCopyright()
    print('------------------------------------------------------') 
    print('      2D stationary convection-diffusion BVP')
    print('         on GMSH mesh from %s.geo\n'%geofile)
    print('               - div(a grad u) + <V,grad u> + b u = f')
    print(' and boundary conditions :')
    print('   * Dirichlet on [2,4,20,21]')
    print('       u = 4 on [2], -4 on [4] and 0 on [20,21]  ')
    print('   * Neumann on [1,3,10]')
    print('       du/dn = 0 on [2,3,10]')
    print(' with ')
    print('   a = %s'%func2str(af))
    print('   V = [%s,%s] '%(func2str(Vx),func2str(Vy)))
    print('   b = %g'% b)
    print('   f = %s'%func2str(f))
    print('------------------------------------------------------\n')
    if verbose>=10:
      return
  if verbose>=2:
    print('*** Building the mesh using GMSH')
  
  meshfile=fc_oogmsh.gmsh.buildmesh2d(geofile,N,force=True,verbose=0)
  Th=siMesh(meshfile)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('*** Setting 2D Condenser BVP problem')
 
  pde=PDE(Op=Loperator(dim=2,d=2,A=[[af,None],[None,af]],c=[Vx,Vy],a0=b),f=f)
  bvp=BVP(Th,pde=pde)
  bvp.setDirichlet(2,g2)
  bvp.setDirichlet(4,g4)
  bvp.setDirichlet(20,0)
  bvp.setDirichlet(21,0)
  info=dict(solex=None,geofile=geofile)
  return bvp,info

def setBVPStationaryConvectionDiffusion3D01(N,**kwargs):
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  geofile='cylinder3holes'
  af=lambda x,y,z: 0.7+z/10
  Vx=lambda x,y,z: -10*y;Vy=lambda x,y,z: 10*x;Vz=lambda x,y,z: 10*z
  f=lambda x,y,z: -800.0*np.exp(-10*((x-0.65)**2+y*y+(z-0.5)**2))+\
                   800.0*np.exp(-10*((x+0.65)**2+y*y+(z-0.5)**2))
  b=0.01              
  
  (geodir,geofile)=get_geo(3,3,geofile)
  env=fc_oogmsh.sys.environment()
  geodir=kwargs.get('geodir',geodir)#env.geo_dir)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  
  if verbose>1:
    PrintCopyright()
    print('------------------------------------------------------') 
    print('      3D stationary convection-diffusion BVP')
    print('         on GMSH mesh from %s.geo\n'%geofile)
    print('               - div(a grad u) + <V,grad u> + b u = f')
    print(' and boundary conditions :')
    print('   * Robin on [20,21]')
    print('       du/dn + u= +0.05 on [20]')
    print('       du/dn + u= -0.05 on [21]')
    print('   * Neumann otherwise')
    print('       du/dn = 0')
    print(' with ')
    print('   a = %s'%func2str(af))
    print('   V = [%s,%s,%s] '%(func2str(Vx),func2str(Vy),func2str(Vz)))
    print('   b = %g'% b)
    print('   f = %s'%func2str(f))
    print('------------------------------------------------------\n')
    if verbose>=10:
      return
  if verbose>=2:
    print('1. Building the mesh using GMSH')
  import os
  meshfile=fc_oogmsh.gmsh.buildmesh3d(geodir+os.sep+geofile+'.geo',N, force=True,verbose=0,meshdir=meshdir)
  Th=siMesh(meshfile)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('2. Setting 3D Stationary convection/diffusion BVP problem')
 
  pde=PDE(Op=Loperator(dim=3,d=3,A=[[af,None,None],[None,af,None],[None,None,af]], c=[Vx,Vy,Vy],a0=b),f=f)
  bvp=BVP(Th,pde=pde)
  bvp.setRobin(20,+0.05,ar=1)
  bvp.setRobin(21,-0.05,ar=1)
  info=dict(solex=None,geofile=geofile)
  return bvp,info

def setBVPPoisson2D_ex01(N,**kwargs):
  env=fc_oogmsh.sys.environment()
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  geodir=kwargs.get('geodir',env.geo_dir)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  uex=lambda x,y: cos(x-y)*sin(x+y)+exp(-(x**2+y**2))
  f=lambda x,y: -4*x**2*exp(-x**2-y**2) - 4*y**2*exp(-x**2-y**2) + 4*cos(x-y)*sin(x+y) + 4*exp(-x**2-y**2)
  
  if verbose>=1:
    PrintCopyright()
    print('------------------------------------------------------')
    print('      2D Poisson B.V.P. problem on unit square:')
    print('               -Laplacien(u) = f')
    print(' with  ')
    print('    * Dirichlet boundary conditions on [1,2,3,4]')
    print(' Exact solution :\n   %s'%func2str(uex))
    print('------------------------------------------------------')
    if verbose>=10:
      return

  if verbose>=2:
    print('1. Setting the mesh using HyperCube function')
  
  Th=HyperCube(2,N)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('2. Setting 2D Condenser BVP problem')
    
  Lop=Loperator(dim=2,d=2,A=[[1,None],[None,1]])
  pde=PDE(Op=Lop,f=f)
  bvp=BVP(Th,pde=pde)
  bvp.setDirichlet( 1, uex)
  bvp.setDirichlet( 2, uex)
  bvp.setDirichlet( 3, uex)
  bvp.setDirichlet( 4, uex)
  
  info=dict(solex=uex,f=f)
  return bvp,info

def setBVPPoisson2D_ex02(N,**kwargs):
  env=fc_oogmsh.sys.environment()
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  geodir=kwargs.get('geodir',env.geo_dir)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  uex=lambda x,y: cos(4*pi*(x**2 + y**2))*exp(-2*(x**2 +y**2))
  f=lambda x,y: ( 64*pi**2*x**2*cos(4*pi*(x**2 + y**2))*exp(-2*x**2 - 2*y**2) +
                  64*pi**2*y**2*cos(4*pi*(x**2 + y**2))*exp(-2*x**2 - 2*y**2) - 
                  64*pi*x**2*exp(-2*x**2 - 2*y**2)*sin(4*pi*(x**2 + y**2)) -
                  64*pi*y**2*exp(-2*x**2 - 2*y**2)*sin(4*pi*(x**2 + y**2)) - 
                  16*x**2*cos(4*pi*(x**2 + y**2))*exp(-2*x**2 - 2*y**2) - 
                  16*y**2*cos(4*pi*(x**2 + y**2))*exp(-2*x**2 - 2*y**2) +
                  16*pi*exp(-2*x**2 - 2*y**2)*sin(4*pi*(x**2 + y**2)) +
                  8*cos(4*pi*(x**2 + y**2))*exp(-2*x**2 - 2*y**2)
                )
  if verbose>=1:
    PrintCopyright()
    print('------------------------------------------------------')
    print('      2D Poisson B.V.P. problem on unit square:')
    print('               -Laplacien(u) = f')
    print(' with  ')
    print('    * Dirichlet boundary conditions on [1,2,3,4]')
    print(' Exact solution :\n   %s'%func2str(uex))
    print('------------------------------------------------------')
    if verbose>=10:
      return

  if verbose>=2:
    print('*** Setting the mesh using HyperCube function')
  
  Th=HyperCube(2,N)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('*** Setting 2D Condenser BVP problem')
    
  Lop=Loperator(dim=2,d=2,A=[[1,None],[None,1]])
  pde=PDE(Op=Lop,f=f)
  bvp=BVP(Th,pde=pde)
  bvp.setDirichlet( 1, uex)
  bvp.setDirichlet( 2, uex)
  bvp.setDirichlet( 3, uex)
  bvp.setDirichlet( 4, uex)
  
  info=dict(solex=uex,f=f)
  return bvp,info

def setBVPPoisson2D_ex03(N,**kwargs):
  env=fc_oogmsh.sys.environment()
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  geodir=kwargs.get('geodir',env.geo_dir)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  uex=lambda x,y: cos(2*x+y)
  f=lambda x,y: 5*cos(2*x+y)
  gradu=[lambda x,y: -2*sin(2*x+y),lambda x,y: -sin(2*x+y)]
  ar3 = lambda x,y: 1+x**2+y**2
  if verbose>=1:
    PrintCopyright()
    print('------------------------------------------------------')
    print('      2D Poisson B.V.P. problem on unit square:')
    print('               -Laplacien(u) = f')
    print(' with  ')
    print(' Exact solution : %s'%func2str(uex))
    print(' and boundary conditions :')
    print('   * Dirichlet on [1,2]')
    print('       u = gD')
    print('   * Robin boundary condition on [3]')
    print('       du/dn + ar*u = gR')
    print('         with ar=%s'%func2str(ar3))
    print('   * Neumann boundary condition on [4]')
    print('       du/dn = gN')
    print('------------------------------------------------------');
    if verbose>=10:
      return

  if verbose>=2:
    print('*** Setting the mesh using HyperCube function')
  
  Th=HyperCube(2,N)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('*** Setting 2D Condenser BVP problem')
    
  Lop=Loperator(dim=2,d=2,A=[[1,None],[None,1]])
  pde=PDE(Op=Lop,f=f)
  bvp=BVP(Th,pde=pde)
  bvp.setDirichlet( 1, uex)
  bvp.setDirichlet( 2, uex)
  bvp.setRobin( 3,lambda x,y: -gradu[1](x,y)+ar3(x,y)*uex(x,y) , ar=ar3)
  bvp.setRobin( 4, gradu[1])
  
  info=dict(solex=uex,f=f)
  return bvp,info

def setBVPPoisson3D_ex01(N,**kwargs):
  env=fc_oogmsh.sys.environment()
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  geodir=kwargs.get('geodir',env.geo_dir)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  uex=lambda x,y,z: cos(4*x-3*y+5*z)
  f=lambda x,y,z: 50*uex(x,y,z)
  gradu=[lambda x,y,z: -4*sin(4*x-3*y+5*z), lambda x,y,z: 3*sin(4*x-3*y+5*z), lambda x,y,z: -5*sin(4*x-3*y+5*z)]
  ar = 1
  if verbose>=1:
    PrintCopyright()
    print('------------------------------------------------------')
    print('      3D Poisson B.V.P. problem on unit square:')
    print('               -Laplacien(u) = f')
    print(' with  ')
    print(' Exact solution : %s'%func2str(uex))
    print(' and boundary conditions :')
    print('   * Dirichlet on [1,3,5]')
    print('       u = gD')
    print('   * Robin boundary condition on [2,4]')
    print('       du/dn + ar*u = gR')
    print('         with ar=%s'%func2str(ar))
    print('   * Neumann boundary condition on [6]')
    print('       du/dn = gN')
    print('------------------------------------------------------');
    if verbose>=10:
      return

  if verbose>=2:
    print('1. Setting the mesh using HyperCube function')
  
  Th=HyperCube(3,N)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('2. Setting 3D Poisson B.V.P. problem')
    
  Lop=Loperator(dim=3,d=3,A=[[1,None,None],[None,1,None],[None,None,1]])
  pde=PDE(Op=Lop,f=f)
  bvp=BVP(Th,pde=pde)
  for lab in [1,3,5]:
    bvp.setDirichlet( lab, uex)
  bvp.setRobin( 2,lambda x,y,z: gradu[0](x,y,z)+ar*uex(x,y,z) , ar=ar)
  bvp.setRobin( 4,lambda x,y,z: gradu[1](x,y,z)+ar*uex(x,y,z) , ar=ar)
  bvp.setRobin( 6,gradu[2])
  
  info=dict(solex=uex,f=f)
  return bvp,info


def setBVPElasticity2d_ex01(N,**kwargs):
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  E=kwargs.get('E',21e5)
  nu=kwargs.get('nu',0.45)
  mu= E/(2*(1+nu))
  lam = E*nu/((1+nu)*(1-2*nu))
  gam=lam+2*mu
  uex=[lambda x,y: cos(2*x+y), lambda x,y: sin(x-3*y)]
  f=[lambda x,y: 4*lam*cos(2*x + y) + 9*mu*cos(2*x + y) + 3*lam*sin(-x + 3*y) + 3*mu*sin(-x + 3*y) ,
     lambda x,y: 2*lam*cos(2*x + y) + 2*mu*cos(2*x + y) - 9*lam*sin(-x + 3*y) - 19*mu*sin(-x + 3*y)]
  g2=[lambda x,y: -3*lam*cos(-x + 3*y) - 2*lam*sin(2*x + y) - 4*mu*sin(2*x + y), 
      lambda x,y: mu*(cos(-x + 3*y) - sin(2*x + y))]
  if verbose>=1:
    PrintCopyright()
    print('------------------------------------------------------') 
    print('      2D Elasticity B.V.P. problem on unit square:')
    print('         - div sigma(u) = f')
    print(' with  * Dirichlet boundary conditions on [1,3,4]')
    print('       * Neumann boundary conditions on [2]')
    print(' and Young modulus E=%g, Poisson ration nu=%g\n'%(E,nu)) 
    print(' exact sol. : [%s,%s]'%(func2str(uex[0]),func2str(uex[1])))
    print('------------------------------------------------------')
    if verbose==10: 
      return
  
  if verbose>=2:
    print('1. Setting the mesh using HyperCube function')
  
  Th=HyperCube(2,N)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('2. Setting 2D Elasticity B.V.P. problem')
  Hop=Hoperator(dim=2,d=2,m=2)
  Hop.H[0][0]=Loperator(d=2,A=[[gam,None],[None,mu]]) 
  Hop.H[0][1]=Loperator(d=2,A=[[None,lam],[mu,None]]) 
  Hop.H[1][0]=Loperator(d=2,A=[[None,mu],[lam,None]]) 
  Hop.H[1][1]=Loperator(d=2,A=[[mu,None],[None,gam]])
  
  pde=PDE(Op=Hop,f=f)
  bvp=BVP(Th,pde=pde)
  
  for lab in [1,3,4]:
    bvp.setDirichlet(lab,uex)
  bvp.setRobin(2,g2)
  
  info=dict(solex=uex,geofile='hypercube')
  return bvp,info

def setBVPElectrostatic2D01(N,**kwargs):
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  sigma1=kwargs.get('sigma1',1)
  sigma2=kwargs.get('sigma2',10)
  (geodir,geofile)=get_geo(2,2,'square4holes6dom')
  env=fc_oogmsh.sys.environment()
  geodir=kwargs.get('geodir',geodir)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  
  if verbose>1:
    PrintCopyright()
    print('------------------------------------------------------') 
    print('      2D electrostatic BVP problem ')
    print('        on square [-1,1]x[-1,1] with ')
    print('        4 holes and 6 domains ')
    print('------------------------------------------------------') 
    print(' PDE :')
    print('    * -div(sigma grad(phi)) = 0   on domain [2,4,6,8,10,20]')
    print(' Local electrical conductivity : ')
    print('    * sigma=sigma1=%g on domain [10]'%sigma1)
    print('    * sigma=sigma2=%g on domain [2,4,6,8,20]'%sigma2)
    print(' Dirichlet boundary condition on boundaries [1,3,5,7]')
    print('    * on [1,5] : phi = 12')
    print('    * on [3,7] : phi = 0')
    print(' Neumann boundary condition on boundary [20]')
    print('    * on [20] : sigma d(phi)/dn = 0')
    print('------------------------------------------------------') 
    if verbose>=10:
      return
  if verbose>=2:
    print('1. Building the mesh using GMSH')
  
  meshfile=fc_oogmsh.gmsh.buildmesh2d(geodir+os.sep+geofile+'.geo',N,force=True)
  Th=siMesh(meshfile)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('2. Setting 2D Electrostatic BVP')
 
  pde=PDE(Op=Loperator(dim=2,A=[[sigma2,None],[None,sigma2]]))
  bvp=BVP(Th,pde=pde)
  Lop=Loperator(dim=2,A=[[sigma1,None],[None,sigma1]])
  bvp.setPDE(PDE(Op=Lop),labels=10)              
  bvp.setDirichlet(1,12)
  bvp.setDirichlet(3,0)
  bvp.setDirichlet(5,12)
  bvp.setDirichlet(7,0)
  info=dict(solex=None,geofile=geofile,sigma1=sigma1,sigma2=sigma2)
  return bvp,info

def setBVPCondenser2D01(N,**kwargs):
  verbose=kwargs.get('verbose',0)
  if (N==0) and (verbose<10):
    verbose=10  
  u1=kwargs.get('u1',1)
  u2=kwargs.get('u2',-1)
  geofile='condenser'
  (geodir,geofile)=get_geo(2,2,geofile)
  env=fc_oogmsh.sys.environment()
  geodir=kwargs.get('geodir',geodir)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  
  if verbose>1:
    PrintCopyright()
    print('------------------------------------------------------') 
    print('      2D condenser BVP problem ')
    print('        on mesh build from gmsh and %s file '%geofile)
    print('------------------------------------------------------') 
    print(' PDE :')
    print('    * -Laplacian(u) = 0   on domain [1]')
    print(' Dirichlet boundary condition on boundaries [1,98,99]')
    print('    * on [0]  : u = 0')
    print('    * on [98] : u = %d'%u1)
    print('    * on [99] : u = %d'%u2)
    print('------------------------------------------------------') 
    if verbose>=10:
      return
  if verbose>=2:
    print('*** Building the mesh using GMSH')
  
  meshfile=fc_oogmsh.gmsh.buildmesh2d(geodir+os.sep+geofile+'.geo',N,force=True)
  Th=siMesh(meshfile)
  if verbose>=2:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    print('*** Setting 2D Condenser BVP')
 
  pde=PDE(Op=Loperator(dim=2,A=[[1,None],[None,1]]))
  bvp=BVP(Th,pde=pde)
  bvp.setDirichlet(1,0)
  bvp.setDirichlet(98,u1)
  bvp.setDirichlet(99,u2)
  info=dict(solex=None,geofile=geofile,u1=u1,u2=u2)
  return bvp,info