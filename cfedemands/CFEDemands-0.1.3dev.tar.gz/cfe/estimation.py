
# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::*Expenditure%20Shares][agg_shares_and_mean_shares]]

# Tangled on Fri Apr 28 15:06:54 2017
import pylab as pl 
import pandas as pd
import numpy as np
from cfe.df_utils import broadcast_binary_op

def expenditure_shares(df):

    aggshares=df.groupby(level='t').sum()
    aggshares=aggshares.div(aggshares.sum(axis=1),axis=0).T
    meanshares=df.div(df.sum(axis=1),level='j',axis=0).groupby(level='t').mean().T

    mratio=(np.log(meanshares)-np.log(aggshares))
    sharesdf=pd.Panel({'Mean shares':meanshares,'Agg. shares':aggshares})

    return sharesdf,mratio

def agg_shares_and_mean_shares(df,figname=None,ConfidenceIntervals=False,ax=None):
    """Figure of log mean shares - log agg shares.

    Input df is a pd.DataFrame of expenditures, indexed by (t,j).

    ConfidenceIntervalues is an optional argument.  
    If True, the returned figure will have 95% confidence intervals.  
    If a float in (0,1) that will be used for the size of the confidence 
    interval instead.
    """

    shares,mratio=expenditure_shares(df)
    meanshares=shares['Mean shares']

    tab=shares.to_frame().unstack()
    tab.sort_values(by=('Agg. shares',meanshares.columns[0]),ascending=False,inplace=True)

    if ax is None:
        fig, ax = pl.subplots()

    mratio.sort_values(by=mratio.columns[0],inplace=True)
    ax.plot(range(mratio.shape[0]),mratio.as_matrix(), 'o')
    ax.legend(mratio.columns,loc=2)
    ax.set_ylabel('Log Mean shares divided by Aggregate shares')

    v=ax.axis()

    if  len(mratio)>=12:
        i=0
        for i in range(len(mratio)):
            name=mratio.ix[i].name # label of expenditure item

            if mratio.iloc[i,0]>0.2:
                #pl.text(i,mratio.T.iloc[0][name],name,fontsize='xx-small',ha='right')

                # The key option here is `bbox`. 
                ax.annotate(name, xy=(i,mratio.T.iloc[0][name]), xytext=(-20,10), 
                            textcoords='offset points', ha='right', va='bottom',
                            bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.25', 
                            color='red'),fontsize='xx-small')

            if mratio.iloc[i,0]<-0.2:
                #pl.text(i,mratio.T.iloc[0][name],name,fontsize='xx-small')
                ax.annotate(name, xy=(i,mratio.T.iloc[0][name]), xytext=(20,-10), 
                            textcoords='offset points', ha='left', va='top',
                            bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.25', 
                            color='red'),fontsize='xx-small')
    else: #Put labels on xaxis
        ax.set_xticklabels(mratio.index.values.tolist(),rotation=45)
      

    if ConfidenceIntervals>0: # Bootstrap some confidence intervals
        if ConfidenceIntervals==1: ConfidenceIntervals=0.95
        current=0
        last=1
        M=np.array([],ndmin=3).reshape((mratio.shape[0],mratio.shape[1],0))
        i=0
        mydf=df.loc[:,mratio.index]
        while np.max(np.abs(current-last))>0.001 or i < 1000:
            last=current
            # Sample households in each  round with replacement
            bootdf=mydf.iloc[np.random.random_integers(0,df.shape[0]-1,df.shape[0]),:]
            bootdf.reset_index(inplace=True)
            bootdf['j']=range(bootdf.shape[0])
            bootdf.set_index(['t','j'],inplace=True)
            shares,mr=expenditure_shares(bootdf)
            M=np.dstack((M,mr.as_matrix()))
            M.sort(axis=2)
            a=(1-ConfidenceIntervals)/2.
            lb= mratio.as_matrix() - M[:,:,np.floor(M.shape[-1]*a)]
            ub=M[:,:,np.floor(M.shape[-1]*(ConfidenceIntervals+a))] - mratio.as_matrix()
            current=np.c_[lb,ub]
            i+=1
        T=mratio.shape[1]
        for t in range(T):
            ax.errorbar(np.arange(mratio.shape[0]),mratio.as_matrix()[:,t],yerr=current[:,[t,t-T]].T.tolist())
            tab[(df.index.levels[0][t],'Upper Int')]=current[:,t-T]
            tab[(df.index.levels[0][t],'Lower Int')]=current[:,t]

    ax.axhline()

    if figname:
        pl.savefig(figname)

    return tab,ax

# agg_shares_and_mean_shares ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::*Expenditure%20Shares][group_expenditures]]

# Tangled on Fri Apr 28 15:06:54 2017
def group_expenditures(df,groups):
    myX=pd.DataFrame(index=df.index)
    for k,v in groups.iteritems():
        myX[k]=df[['$x_{%d}$' % i for i in v]].sum(axis=1)
            
    return myX

# group_expenditures ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::*Rank%201%20Approximation][svd_rank1_approximation_with_missing_data]]

# Tangled on Fri Apr 28 15:06:54 2017
import pandas as pd
import numpy as np

def missing_inner_product(X,min_obs=None):
  n,m=X.shape

  if n<m: 
      axis=1
      N=m
  else: 
      axis=0
      N=n

  xbar=X.mean(axis=axis)

  if axis:
      C=(N-1)*X.T.cov(min_periods=min_obs)
  else:
      C=(N-1)*X.cov(min_periods=min_obs)

  return C + N*np.outer(xbar,xbar)

def drop_columns_wo_covariance(X,min_obs=None,VERBOSE=False):
    """Drop columns from pd.DataFrame that lead to missing elements of covariance matrix."""

    m,n=X.shape
    assert(m>n)

    HasMiss=True
    while HasMiss:
        foo = X.cov(min_periods=min_obs).count()
        if np.sum(foo<X.shape[1]):
            badcol=foo.argmin()
            del X[badcol] # Drop  good with  most missing covariances
            if VERBOSE: print("Dropping %s." % badcol)
        else:
            HasMiss=False

    return X

def svd_missing(A,max_rank=None,min_obs=None):

    P=missing_inner_product(A,min_obs=min_obs)

    sigmas,u=np.linalg.eig(P)

    order=np.argsort(-sigmas)
    sigmas=sigmas[order]

    # Truncate rank of representation using Kaiser criterion (positive eigenvalues)
    u=u[:,order]
    u=u[:,sigmas>0]
    s=np.sqrt(sigmas[sigmas>0])

    if max_rank is not None and len(s) > max_rank:
        u=u[:,:max_rank]
        s=s[:max_rank]

    r=len(s)
    us=np.matrix(u)*np.diag(s)

    v=np.zeros((len(s),A.shape[1]))
    for j in range(A.shape[1]):
        a=A.iloc[:,j].as_matrix().reshape((-1,1))
        x=np.nonzero(~np.isnan(a))[0] # non-missing elements of vector a
        if len(x)>=r:
            v[:,j]=(np.linalg.pinv(us[x,:])*a[x]).reshape(-1)
        else:
            v[:,j]=np.nan

    return np.matrix(u),s,np.matrix(v).T

def svd_rank1_approximation_with_missing_data(x,return_usv=False,max_rank=None,min_obs=None,VERBOSE=True):
    """
    Return rank 1 approximation to a pd.DataFrame x, where x may have
    elements which are missing.
    """
    x=x.copy()
    m,n=x.shape

    if n<m:  # If matrix 'thin', make it 'short'
        x=x.T
        TRANSPOSE=True
    else:
        TRANSPOSE=False

    x=x.dropna(how='all',axis=1) # Drop any column which is /all/ missing.
    x=x.dropna(how='all',axis=0) # Drop any row which is /all/ missing.

    x=drop_columns_wo_covariance(x.T,min_obs=min_obs).T
    u,s,v = svd_missing(x,max_rank=max_rank,min_obs=min_obs)
    if VERBOSE:
        print("Estimated singular values: ",)
        print(s)

    xhat=pd.DataFrame(v[:,0]*s[0]*u[:,0].T,columns=x.index,index=x.columns).T

    if TRANSPOSE: xhat=xhat.T

    if return_usv:
        return xhat,u,s,v
    else: return xhat

# svd_rank1_approximation_with_missing_data ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::*Estimation%20of%20reduced%20form][estimate_reduced_form]]

# Tangled on Fri Apr 28 15:06:57 2017
import pandas as pd
import warnings
import sys
from collections import OrderedDict
from cfe.df_utils import drop_missing, ols, arellano_robust_cov, broadcast_binary_op, use_indices

def estimate_reduced_form(y,z,return_v=False,return_se=False,VERBOSE=False):
  """Estimate reduced-form Frisch expenditure/demand system.

  Inputs:
      - y : pd.DataFrame of log expenditures or log quantities, indexed by (j,t,mkt), 
            where j indexes the household, t the period, and mkt the market.  
            Columns are different expenditure items.

      - z : pd.DataFrame of household characteristics; index should match that of y.

  Outputs:
      - b : Estimated good-time-market fixed effects; will sum to  zero.

  Ethan Ligon                                            February 2017
  """
  try: # Be a little forgiving if t or mkt index is missing.
      assert y.index.names==['j','t','mkt'], "Indices should be (j,t,mkt)?"
  except AssertionError:
      y = y.reset_index()
      if not 'mkt' in y.columns: y['mkt']=1
      if not 't' in y.columns: y['t']=1
      y = y.set_index(['j','t','mkt'])

  try:
      assert z.index.names==['j','t','mkt'], "Indices should be (j,t,mkt)?"
  except AssertionError:
      z = z.reset_index()
      if not 'mkt' in z.columns: z['mkt']=1
      if not 't' in z.columns: z['t']=1
      z = z.set_index(['j','t','mkt'])

  periods = list(set(y.index.get_level_values('t')))
  mkts = list(set(y.index.get_level_values('mkt')))

  # Time-market dummies
  DateLocD = use_indices(y,['t','mkt'])
  DateLocD = pd.get_dummies(zip(DateLocD['t'],DateLocD['mkt']))
  DateLocD.index = y.index

  sed = pd.DataFrame(columns=y.columns)
  a = pd.Series(index=y.columns)
  b = OrderedDict() #pd.DataFrame(index=y.columns)
  d = OrderedDict() #pd.DataFrame(index=y.columns,columns=z.columns).T
  ce = pd.DataFrame(index=y.index,columns=y.columns)
  V = pd.Panel(items=y.columns,major_axis=z.columns,minor_axis=z.columns)

  for i,Item in enumerate(y.columns):
      if VERBOSE: print(Item)

      lhs,rhs=drop_missing([y.iloc[:,[i]],pd.concat([z,DateLocD],axis=1)])
      rhs=rhs.loc[:,rhs.std()>0] # Drop  any X cols with no variation
      useDateLocs=list(set(DateLocD.columns.tolist()).intersection(rhs.columns.tolist()))

      # Calculate deviations
      lhsbar=lhs.mean(axis=0)
      assert ~np.any(np.isnan(lhsbar)), "Missing data in lhs?"
      lhs=lhs-lhsbar
      lhs=lhs-lhs.mean(axis=0)

      rhsbar=rhs.mean(axis=0)
      assert ~np.any(np.isnan(rhsbar)), "Missing data in rhs?"
      rhs=rhs-rhsbar
      rhs=rhs-rhs.mean(axis=0)

      # Need to make sure time-market effects sum to zero; add
      # constraints to estimate restricted least squares
      ynil=pd.DataFrame([0],index=[(-1,0,0)],columns=lhs.columns)
      znil=pd.DataFrame([[0]*z.shape[1]],index=[(-1,0,0)],columns=z.columns)
      timednil=pd.DataFrame([[1]*DateLocD.shape[1]],index=[(-1,0,0)],columns=DateLocD.columns)

      X=rhs.append(znil.join(timednil))
      X=X.loc[:,X.std()>0] # Drop  any X cols with no variation

      # Estimate d & b
      myb,mye=ols(X,lhs.append(ynil),return_se=False,return_v=False,return_e=True) # Need version of pandas >0.14.0 (?) for this use of join
      ce[Item]=mye.iloc[:-1,:] # Drop constraint that sums time-effects to zero

      if return_v or return_se:
          V[Item]=arellano_robust_cov(z,ce[Item])
          sed[Item]=pd.Series(np.sqrt(np.diag(V[Item])), index=z.columns) # reduced form se on characteristics

      d[Item]=myb[z.columns] # reduced form coefficients on characteristics

      b[Item] = myb[useDateLocs].squeeze()  # Terms involving prices
      a[Item] = y[Item].mean() - d[Item].dot(z.mean(axis=0)) - np.array(b[Item]).dot(DateLocD[useDateLocs].mean().values)

  b = pd.DataFrame(b,index=y.groupby(level=['t','mkt']).mean().index)
  #b.index=pd.MultiIndex.from_tuples(b.index,names=['t','mkt'])
  b = b.T

  if b.shape[1]==1: # Only a single time-market
    assert np.all(np.isnan(b)), "Only one good-time effect should mean b not identified"
    b[:]=0

  d = pd.concat(d.values())

  out = [b.add(a,axis=0),ce,d]
  if return_se:
      out += [sed]
  if return_v:
      out += [V]
  return out

# estimate_reduced_form ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::*Extraction%20of%20Frisch%20Elasticities%20and%20Neediness][get_loglambdas]]

# Tangled on Fri Apr 28 15:07:00 2017
import pandas as pd

def get_loglambdas(e,TEST=False,time_index='t',max_rank=1,min_obs=None):
    """
    Use singular-value decomposition to compute loglambdas and price elasticities,
    up to an unknown factor of proportionality phi.

    Input e is the residual from a regression of log expenditures purged
    of the effects of prices and household characteristics.   The residuals
    should be arranged as a matrix, with columns corresponding to goods. 
    """ 

    assert e.shape[0]>e.shape[1], "More goods than observations."

    chat = svd_rank1_approximation_with_missing_data(e,VERBOSE=False,max_rank=max_rank,min_obs=min_obs)

    R2 = chat.var()/e.var()

    # Possible that initial elasticity b_i is negative, if inferior goods permitted.
    # But they must be positive on average.
    if chat.iloc[0,:].mean()>0:
        b=chat.iloc[0,:]
    else:
        b=-chat.iloc[0,:]

    loglambdas=(-chat.iloc[:,0]/b.iloc[0])

    # Find phi that normalizes first round loglambdas
    phi=loglambdas.groupby(level=time_index).std().iloc[0]
    loglambdas=loglambdas/phi

    loglambdas=pd.Series(loglambdas,name='loglambda')
    bphi=pd.Series(b*phi,index=e.columns,name=r'\phi\beta')

    if TEST:
        foo=pd.DataFrame(-np.outer(bphi,loglambdas).T,index=loglambdas.index,columns=bphi.index)
        assert df_norm(foo-chat)<1e-4
        #print "blogL norm: %f" % np.linalg.norm(foo-chat)

    return bphi,loglambdas

def iqr(x):
    """The interquartile range of a pd.Series of observations x."""
    q=x.quantile([0.25,0.75])
 
    try:
        return q.diff().iloc[1]
    except AttributeError:
        return np.nan

def bootstrap_elasticity_stderrs(e,clusterby=['t','mkt'],tol=1e-2,minits=30,return_samples=False,VERBOSE=False,outfn=None,TRIM=True):
    """Bootstrap estimates of standard errors for \phi\beta.

    Takes pd.DataFrame of residuals as input.

    Default is to `cluster' by (t,mkt) via a block bootstrap.

    If optional parameter TRIM is True, then calculations are
    performed using the interquartile range (IQR) instead of the
    standard deviation, with the standard deviation computed as
    IQR*0.7416 (which is a good approximation provided the
    distribution is normal).

    Ethan Ligon                              January 2017
    """
    #bhat,Lhat=get_loglambdas(e)
    def resample(e):
        e = e.iloc[np.random.random_integers(0,e.shape[0]-1,size=e.shape[0]),:]
        e = e - e.mean()
        return e

    if outfn: outf=open(outfn,'a')

    delta=1.
    old=np.array(1)
    new=np.array(0)
    i=1
    L=[]
    while delta>tol or i < minits:
        delta=np.nanmax(np.abs(old.reshape(-1)-new.reshape(-1)))
        if VERBOSE and (i % 2)==0 and i>2: 
            print "Iteration %d, delta=%5.4f.  Measure of non-normality %6.5f." % (i, delta,np.nanmax(np.abs(std0.reshape(-1)-std1.reshape(-1))))
        old=new
        if clusterby:
            S=e.reset_index().groupby(clusterby,as_index=True)[e.columns].apply(resample)
        else:
            S=resample(e)

        bs,ls=get_loglambdas(S)
      
        if np.any(np.isnan(bs)):
            warnings.warn("Resampling draw with no data?")
        try:
            B=B.append(bs,ignore_index=True)
        except NameError:
            B=pd.DataFrame(bs).T # Create B

        L.append(ls)

        std0=B.std()
        std1=B.apply(iqr)*0.7416 # Estimate of standard deviation, with trimming
        if TRIM:
            new=std1
        else:
            new=std0

        if outfn: outf.write(','.join(['%6.5f' % b for b in bs])+'\n')
        i+=1

    if outfn: outf.close()
    if return_samples:
        B.dropna(how='all',axis=1,inplace=True) # Drop any goods always missing estimate
        return new,B
    else:
        return new

# get_loglambdas ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::*Direct%20estimation%20of%20price%20elasticities][direct_price_elasticities]]

# Tangled on Fri Apr 28 15:07:05 2017

def direct_price_elasticities(y,p,z,VERBOSE=True,return_se=False,return_v=False):
    """Estimate reduced-form Frisch expenditure/demand system.

       Inputs:
         - y : pd.DataFrame of log expenditures or log quantities, indexed by (j,t,mkt), 
               where j indexes the household, t the period, and mkt the market.  
               Columns are different expenditure items.

         - p : pd.DataFrame of log prices, indexed by (t,mkt), with
               prices for different goods across columns.

         - z : pd.DataFrame of household characteristics; index should match that of y.

      Ethan Ligon                                            March 2017
    """
    assert(y.index.names==['j','t','mkt'])
    assert(z.index.names==['j','t','mkt'])

    periods = list(set(y.index.get_level_values('t')))
    mkts = list(set(y.index.get_level_values('mkt')))
    sed = pd.DataFrame(columns=y.columns)
    a = pd.Series(index=y.columns)
    b = OrderedDict() #pd.DataFrame(index=y.columns)
    d = OrderedDict() #pd.DataFrame(index=y.columns,columns=z.columns).T
    ce = pd.DataFrame(index=y.index,columns=y.columns)
    V = pd.Panel(items=y.columns,major_axis=z.columns,minor_axis=z.columns)

    for i,Item in enumerate(y.columns):
        if VERBOSE: print(Item)
        if np.any(np.isnan(p[Item])): continue # Don't estimate with missing prices

        rhs = z.reset_index('j').join(p[Item]).reset_index().set_index(['j','t','mkt'])
        rhs.rename(columns={Item:'log p'},inplace=True)

        lhs,rhs=drop_missing([y.iloc[:,[i]],rhs])

        rhs['Constant']=1

        myb,mye=ols(rhs,lhs,return_se=False,return_v=False,return_e=True) # Need version of pandas >0.14.0 (?) for this use of join
        ce[Item]=mye

        if return_v or return_se:
            V[Item]=arellano_robust_cov(rhs,mye)
            sed[Item]=pd.Series(np.sqrt(np.diag(V[Item])), index=z.columns) # reduced form se on characteristics

        d[Item]=myb[z.columns] # reduced form coefficients on characteristics

        a[Item] = myb['Constant']
        b[Item] = myb['log p'].values[0]

    b = pd.Series(b)

    d = pd.concat(d.values())

    out = [a,b,ce,d]
    if return_se:
        out += [sed]
    if return_v:
        out += [V]
    return out

# direct_price_elasticities ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::*Indirect%20estimation%20of%20price%20elasticities][Indirect\ estimation\ of\ price\ elasticities:1]]

# Tangled on Fri Apr 28 15:07:05 2017
def indirect_price_elasticities(a,p,zbar):
    """Estimate reduced-form Frisch expenditure/demand system.

       Inputs:
         - a : pd.DataFrame of good-time-market effects estimated by =estimate_reduced_form=,
               indexed by (t,mkt), where t indexes the period, and mkt the market.  
               Columns are different expenditure items.

         - p : pd.DataFrame of log prices, indexed by (t,mkt), with
               prices for different goods across columns.

         - zbar : pd.DataFrame of average household characteristics; index should match that of a.

      Ethan Ligon                                            March 2017
    """
    assert(a.index.names==['t','mkt'])
    assert(zbar.index.names==['t','mkt'])

    # Filter p
    X=zbar.copy()
    X['Constant'] = 1
    y = p.dropna(how='any',axis=1)

    # pe are filtered log prices
    bp,pe = ols(X,y,return_se=False,return_e=True)

    X = pe.copy()

    Xm=np.matrix((X-X.mean()).as_matrix())

    ym=np.matrix((a-a.mean()).as_matrix())
  
    B=OrderedDict()
    SE=OrderedDict()
    for i,Item in enumerate(y.columns):
        B[Item] = np.linalg.lstsq(Xm[:,i],ym[:,i])[0][0,0]
        e = ym[:,i] - Xm[:,i]*B[Item]
        SE[Item] = np.sqrt(np.var(e)/np.var(Xm[:,i]))

    B = pd.Series(B)
    SE = pd.Series(SE)
    return B,SE

# Indirect\ estimation\ of\ price\ elasticities:1 ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::*Distance%20between%20two%20estimates%20of%20\beta][elasticities_equal]]

# Tangled on Fri Apr 28 15:07:06 2017
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats.distributions import f as F

def elasticities_equal(b1,b2,v1,v2,N,N2,pvalue=False,criterion=False):

    assert N2<N, "N2 should be size of sub-sample of pooled sample."
    n=len(b1)

    assert n==len(b2), "Length of vectors must be equal"

    def Fcriterion(psi):
        try:
            psi=psi[0,0]
        except (TypeError, IndexError):
            pass

        d = np.matrix(psi*b1 - b2)
        if d.shape[0]<d.shape[1]: d = d.T

        #W = np.matrix((psi**2)*v1 + v2*(1-2*(psi**2)*N2/N)).I
        W = np.matrix((psi**2)*v1 + v2).I # Independent case
        #W = np.matrix(v1 + v2).I # Independent case

        F = N2*(N-n-1)/((N-1)*(n-1)) * d.T*W*d

        if ~np.isscalar(F):
            F=F[0,0]

        return F

    #result = minimize_scalar(Fcriterion,method='bounded',bounds=[0,10])
    result = minimize_scalar(Fcriterion)
    psi=np.abs(result['x'])
    Fstat=result['fun']

    assert result['success'], "Minimization failed?"

    outputs = [psi,Fstat]

    if pvalue:
        p = 1 - F.cdf(Fstat,n-1,N-n-1)
        outputs.append(p)

    if criterion:
        outputs.append(Fcriterion)
    
    return tuple(outputs)

# elasticities_equal ends here
