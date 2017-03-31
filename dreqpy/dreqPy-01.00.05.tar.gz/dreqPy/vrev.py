"""This module has a class which will analyse the usage of variables in the data request"""
import operator
import collections

class checkVar(object):
  """checkVar
--------
Class to analyse the usage of variables in the data request.
"""
  def __init__(self,dq):
    self.dq = dq
    self.mips = set( [i.label for i in  dq.coll['mip'].items] )
    for i in ['PDRMIP', 'DECK', 'VIACSAB', 'SolarMIP', 'CMIP6' ]:
      self.mips.discard(i)

  def chk2(self,vn,byExpt=False, byBoth=False):
    dq = self.dq
    ks = [i for i in dq.coll['var'].items if i.label == vn ]

    v = ks[0]
    cc = {}
    l = dq.inx.iref_by_sect[v.uid].a['CMORvar']
    for i in l:
      r = dq.inx.uid[i]
      kk = '%s.%s' % (r.mipTable, r.label )
      cc[i] = (kk,self.chkCmv( i, byExpt=byExpt, byBoth=byBoth ) )

    return cc

  def chk(self,vn):
    ks = [i for i in dq.coll['var'].items if i.label == vn ]

    v = ks[0]
    l = dq.inx.iref_by_sect[v.uid].a['CMORvar']

## set of all request variables 
    s = set()
    for i in l:
      for j in dq.inx.iref_by_sect[i].a['requestVar']:
        s.add(j)

## filter out the ones which link to a remark
    s0 = set( [i for i in s if dq.inx.uid[dq.inx.uid[i].vgid]._h.label != 'remarks' ] )

## set of request groups

    s1  = set( [dq.inx.uid[i].vgid for i in s0 ] )

    #s2 = set()
#for i in s1:
  #for j in dq.inx.iref_by_sect[i].a['requestLink']:
    #s2.add(j)
    s2 = reduce( operator.or_, [set(dq.inx.iref_by_sect[i].a['requestLink']) for i in s1 if 'requestLink' in dq.inx.iref_by_sect[i].a] )

    mips = set( [dq.inx.uid[i].mip for i in s2 ] )
    self.missing = self.mips.difference( mips )
    self.inc = mips

#############
  def chkCmv(self,cmvid, byExpt=False, byBoth=False):
    dq = self.dq
    s = set( dq.inx.iref_by_sect[cmvid].a['requestVar'] )

## filter out the ones whch link to a remark

# s0: set of requestVars

    s0 = set( [i for i in s if dq.inx.uid[dq.inx.uid[i].vgid]._h.label != 'remarks' ] )

## set of request groups
## dictionary, keyed on variable group uid, with values set to priority of variable
##

    cc1 = collections.defaultdict( set )
    for i in s0:
      cc1[ dq.inx.uid[i].vgid ].add( dq.inx.uid[i].priority )
    ##s1  = set( [dq.inx.uid[i].vgid for i in s0 ] )
    
    s2 = set()
    for i in cc1:
      if 'requestLink' in dq.inx.iref_by_sect[i].a:
        for l in dq.inx.iref_by_sect[i].a['requestLink']:
          lr = dq.inx.uid[l]
          if lr.opt == 'priority':
            p = int( float( lr.opar ) )
            if max( cc1[i] ) <= p:
              s2.add(l)
          else:
            s2.add( l )
    ##ll = [set(dq.inx.iref_by_sect[i].a['requestLink']) for i in cc1 if 'requestLink' in dq.inx.iref_by_sect[i].a]
    ##if len(ll) == 0:
      ##return set()
##
    ##s2 = reduce( operator.or_, ll) 
    if len( s2 ) == 0:
      if byBoth:
        return (set(),set())
      else:
        return s2

    if byBoth or not byExpt:
      mips0 = set( [dq.inx.uid[i].mip for i in s2] )
    if byExpt or byBoth:

##  set of esid values
      esids = set()
      for i in s2:
        for u in dq.inx.iref_by_sect[i].a['requestItem']:
          esids.add( dq.inx.uid[u].esid )
      mips = set()
      for e in esids:
        if e == '':
          ##print 'WARNING: empty esid encountered'
          pass
        else:
          r = dq.inx.uid[e]
          if r._h.label == 'mip':
            mips.add(e)
          else:
            if r._h.label == 'exptgroup':
              if 'experiment' in dq.inx.iref_by_sect[e].a:
                r = dq.inx.uid[  dq.inx.iref_by_sect[e].a['experiment'][0] ]
              else:
                ei = dq.inx.uid[e]
                print ( 'ERROR.exptgroup.00001: empty experiment group: %s: %s' % (ei.label, ei.title) )
            if r._h.label in [ 'remarks','exptgroup']:
              ##print 'WARNING: link to remarks encountered'
              pass
            else:
              assert r._h.label == 'experiment', 'LOGIC ERROR ... should have an experiment record here: %s' % r._h.label
              mips.add(r.mip)
      if byBoth:
        return (mips0,mips)
      else:
        return mips
    else:
      return mips0

if __name__ == '__main__':
  try:
    import dreq
  except:
    import dreqPy.dreq as dreq
  dq = dreq.loadDreq()
  c = checkVar(dq)
  c.chk( 'tas' )
  print ( '%s, %s' % (c.inc, c.missing))
