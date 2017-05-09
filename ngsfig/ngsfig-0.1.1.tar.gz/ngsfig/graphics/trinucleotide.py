
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Fri Apr 21 15:15:15 EDT 2017 -0400 (Week 16)
## 
## 
## Reference: 
## 
## ************************************************************************

import warnings

import pandas as pd
import numpy as np
import re
import os
  
import itertools
import matplotlib.pyplot as plt
from tabulate import tabulate
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
from matplotlib import font_manager as fm


from xmisc.utils.logging import logsave
from xmisc.utils.list import *
from xmisc.graphics.lego import LegoBrick,LegoBrickSet
from ngsfig.utils.dna import *


def get_bar3d_pos(n):
  xpos = np.arange(0,n,1)
  ypos = np.arange(0,n,1)
  xpos, ypos = np.meshgrid(xpos, ypos)
  xpos = xpos.flatten()
  ypos = ypos.flatten()
  zpos = np.zeros(n*n)
  ret=[xpos,ypos,zpos]
  return(ret)


  
class TriNucleotide:
  def __init__(self,x,id=None):
    self.x=x
    self.id=id
    self.basesubstitution=self.get_basesubstitution()
    self.basesubstitutioncolor=self.get_basesubstitutioncolor()
    self.baseflanking=self.get_baseflanking()
    self.basetriplet=self.get_basetriplet()
    self.prepData=self.prep_data()
    self.procData=self.proc_data()
    self.n=sum(self.prepData['count'])
    self.basesubstitutionlabel=self.get_basesubstitutionlabel()
    
    
  def get_basesubstitution(self):
    ret=("C>T","C>A","C>G","A>G","A>C","A>T")
    # # ret=("C>T","A>G","C>A","A>C","C>G","A>T")
    return(ret)
  
  def get_basesubstitutionlabel(self):
    # ret=dict(zip(
    #   self.basesubstitution,
    #   [" or ".join([e, revcomp_basesubstitution([e])[0]]) for e in self.basesubstitution]
    #   ))
    # ret=dict(zip(self.basesubstitution,self.basesubstitution))
    
    pie_=self.pie()
    dict_=dict(zip(pie_['basesubstitution'],pie_['freq_']))
    print("dict_",dict_)
    ret=dict(zip(
      self.basesubstitution,
      ["%s (%.2f)" % (e,dict_[e]) if e in dict_ else 0 for e in self.basesubstitution]))
    return(ret)
  
  def get_basesubstitutioncolor(self):
    ret={"C>T":"#ffff00","C>A":"#009999","C>G":"#ff0000","A>G":"#00cc00","A>C":"#0033cc","A>T":"#663399"}
    return(ret)

  def get_baseflanking(self):
    _nucl=("T","C","A","G")
    ret=[["_".join((x,y)) for y in  reversed(_nucl)] for x in _nucl]
    # # ret=[["_".join((y,x)) for y in  (_nucl)] for x in reversed(_nucl)]
    ret=np.array(ret).flatten().tolist()
    return(ret)

  def get_basetriplet(self):
    ret=list(itertools.product(self.basesubstitution, self.baseflanking))
    return(ret)
    
  def prep_data(self):
    ret=self.x.copy()
    loc_=[not e in self.basesubstitution for e in ret['basesubstitution']]
    ret.loc[loc_,'basesubstitution']=revcomp_basesubstitution(ret.loc[loc_,'basesubstitution'].tolist())
    ret.loc[loc_,'baseflanking']=revcomp_baseflanking(ret.loc[loc_,'baseflanking'].tolist())
    # print(ret)
    ret=ret.loc[[e in self.basesubstitution for e in ret['basesubstitution']]]
    ret=ret.loc[[e in self.baseflanking for e in ret['baseflanking']]]
    ret['freq_']=ret['count']/sum(ret['count'])
    return(ret)

  def proc_data(self):
    res=self.prepData
    n_=4
    xpos,ypos,zpos=get_bar3d_pos(n=n_)
    blocklist_=[]
    for e_ in self.basesubstitution:
      ires=res.loc[[e in e_ for e in res['basesubstitution']]]
      idict_freq=dict(zip(ires['baseflanking'], ires['freq_']))
      data_=lreshape([idict_freq[e] if e in idict_freq else 0 for e in self.baseflanking],nrow=n_,ncol=n_,byrow=False)
      color_=self.basesubstitutioncolor[e_]
      ##
      metadata_={"color":color_}
      block_=LegoBrick(data=data_,metadata=metadata_)
      blocklist_.append(block_)
    
    ##
    blocklist_=lreshape(blocklist_,3,2,byrow=False)
    ret=LegoBrickSet(blocklist_)
    return(ret)

  def pie(self):
    df=self.prep_data()
    dg=df.groupby(['basesubstitution'])['count'].sum()
    tmp=dg.reset_index()
    
    dict_=dict(zip(tmp['basesubstitution'],tmp['count']))
    for e in self.basesubstitution:
      if not e in dict_:
        dict_[e]=0.0
    ##
    # print("dict_",dict_)
    df=pd.DataFrame(dict_.items(),columns=['basesubstitution','count'])
    df['freq_']=df['count']/sum(df['count'])
    return(df)

  def pieplot(self,ax=None,pctdistance=1.2,verbose=False):
    pie_=self.pie()
    if verbose:
      print(tabulate(pie_, headers='keys', tablefmt='psql'))
    
    dict_=dict(zip(pie_['basesubstitution'],pie_['count']))
    ##
    if ax is None:
      fig, ax = plt.subplots()
    ##
    ax.text(0.5,1,"Percent of\nBase Substitution")
    patches, texts, autotexts = ax.pie(
      [dict_[e] for e in self.basesubstitution],
      colors=[self.basesubstitutioncolor[e] for e in self.basesubstitution],
      autopct="", #'%1.1f%%',
      pctdistance=pctdistance,
      startangle=140
      )
    ## change fontsize
    proptease = fm.FontProperties()
    proptease.set_size('xx-small')
    plt.setp(autotexts, fontproperties=proptease)
    plt.setp(texts, fontproperties=proptease)
    ax.axis('equal')
    # plt.show()

    
  def legend(self):
    handles_=[plt.Rectangle((0, 0), 1, 1, fc=self.basesubstitutioncolor[e], edgecolor="gray") for e in self.basesubstitution]
    labels_=[self.basesubstitutionlabel[e] for e in self.basesubstitution]
    legend_={'handles':handles_, 'labels':labels_}
    return(legend_)

  def legend2(self,ax,n=4):
    
    xpos = np.arange(0,4,1)
    ypos = np.arange(0,4,1)
  
    xpos, ypos = np.meshgrid(xpos, ypos)
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(4*4)
    dx = 0.9 * np.ones_like(zpos)
    dy = dx.copy()
  
    ax.view_init(elev=45, azim=60) #XB
    ax.set_zlim3d(0, 0.01)
    # Get rid of the panes                          
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 
    
    # Get rid of the spines                         
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the ticks                          
    ax.set_xticks([])                               
    ax.set_yticks([])                               
    ax.set_zticks([])

    gray95="#f2f2f2"
    ax.bar3d(xpos,ypos,zpos,dx,dy,zpos, alpha=1, color=gray95, shade=False, edgecolor="gray",linewidth=0.5)
    for x,y,label in zip(xpos,ypos,self.baseflanking):
      ax.text(x+0.8,y+1.05,0,label,'x',horizontalalignment='center', verticalalignment='bottom',fontsize=7)

    return(None)
    
  def legoplot(self,legend=None,ax=None,**kwargs):
    ret=self.procData.plot(legend=self.legend(),ax=ax,**kwargs)
    return(ret)

  def combplot(self,pdfFpath=None,figsize=(10,7),title=None,legend2=True,verbose=False,**kwargs):
    
    title="%s\nn=%d"%(self.id,self.n)

    pp = PdfPages(pdfFpath)
    fig = plt.figure(figsize=figsize)

    if not legend2:
      gs = gridspec.GridSpec(2, 3, height_ratios=[1, 3],hspace=-0.35)
    else:      
      gs = gridspec.GridSpec(
        4, 4,
        width_ratios=[0.35,0.35,0.9,0.8],
        height_ratios=[0.2,0.5,1,0.5],
        hspace=-0.5)
    ax1 = fig.add_subplot(gs[1,1])
    ax2 = fig.add_subplot(gs[1:,:], projection='3d')
    if legend2:
      ax3 = fig.add_subplot(gs[3,3], projection='3d')
    
    fig.suptitle(title)
    self.pieplot(ax=ax1,verbose=verbose)
    self.legoplot(ax=ax2,verbose=verbose,**kwargs)
    if legend2:
      self.legend2(ax=ax3)
    pp.savefig(bbox_inches='tight',transparent=True)
    pp.close()
    




def read_triNucleotide(inFpath,inFtype=None,colnames=None,**kwargs):
  if inFtype in ['demo']:
    ret=read_triNucleotide_demo(inFpath,colnames=["triplet","count"],**kwargs)
  elif inFtype in ['uncseq']:
    ret=read_triNucleotide_demo(inFpath,colnames=["triplet","count","freq"],**kwargs)
  else:
    ret=read_triNucleotide_demo(inFpath,colnames=colnames,**kwargs)
    ## raise ValueError('TBA for `inFtype="%s"`' % inFtype)
  return(ret)

def read_triNucleotide_demo(inFpath,colnames=["triplet","count"]):
  inData=pd.read_table(inFpath,comment="#",header=None,names=colnames)
  columns_=inData.columns
  # print("columns_",columns_)
  columns2_=[e for e in columns_ if not e in ["triplet", "count"]]
  if not "triplet" in columns_:
    raise Exception('`triplet` must be in the column')
  if not "count" in columns_:
    raise Exception('`count` must be in the column')
  if len(columns2_)>0:
    warnings.warn('Ignored extra columns: [%s]' % ", ".join(columns2_))
  p_=r"([ACGT])([ACGT])([ACGT])->([ACGT])"
  inData['basesubstitution']=[re.sub(p_,r"\2>\4",e) for e in inData['triplet']]
  inData['baseflanking']=[re.sub(p_,r"\1_\3",e) for e in inData['triplet']]
  return(inData)


def main(
  inFpath,
  inFtype,
  colnames,
  id,
  pdfFpath,
  verbose=False
  ):  

  inData=read_triNucleotide(inFpath,inFtype=inFtype,colnames=colnames)
  
  if verbose:
    print(tabulate(inData, headers='keys', tablefmt='psql'))
   
  
  obj=TriNucleotide(inData,id=id)
  # print(obj.procData)
  # print("obj.basesubstitution",obj.basesubstitution)
  # print("obj.baseflanking",obj.baseflanking)
  
  # pdfFpath=re.sub(".txt",".pdf",inFpath)
  
  obj.combplot(
    elev=45,
    azim=60,
    verbose=verbose,
    shade=False,
    zsort=True,

    xlab=None,
    ylab=None,
    zlab="Frequency of Trinucleotide",
    
    pdfFpath=pdfFpath,
    figsize=(10,7),
    dx=0.8,
    dy=0.8,

    xticks=False,
    yticks=False
    
    )
  
  logsave(pdfFpath)
  return(None)
  

def demo(  
  inFpath,
  inFtype="demo",
  colnames=None,
  id="SKCM (Stage III/IV)",
  pdfFpath="trinucleotide_demo.pdf",
  *args,
  **kwargs
  ):
  
  # from pkg_resources import resource_stream, Requirement
  # input = resource_stream(Requirement.parse("ngsfig"), "data/trinucleotide_demo.txt")
  # if inFpath is None:
  #   inFpath=os.path.join("data", "trinucleotide_demo.txt")

  ## 
  main(
    inFpath=inFpath,
    inFtype=inFtype,
    colnames=colnames,
    id=id,
    pdfFpath=pdfFpath,
    *args,
    **kwargs    
    )
  return(None)



if __name__ == "__main__":
  
  # inFpath=os.path.join("data", "skcm356.triplet_count.txt")
  # id="SKCM (Stage III/IV)"  
  # inData=read_triNucleotide(inFpath,inFtype="demo")
  # print(inData)
  
  # obj=TriNucleotide(inData,id=id)
  # print(obj.prepData)
  # print("obj.basesubstitution",obj.basesubstitution)
  # print("obj.baseflanking",obj.baseflanking)
  # print(obj.procData)
  
  
  # demo(inFpath=os.path.join("data", "trinucleotide_demo.txt"))
  None
