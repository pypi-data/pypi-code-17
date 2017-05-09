
## ************************************************************************
## 
## 
## 
## (c) Xiaobei Zhao
## 
## Mon May 08 13:30:06 EDT 2017 -0400 (Week 19)
## 
## 
## Reference: 
## 
## 
## ************************************************************************
import re

def revcomp(x):
  dict_ = {'A':'T','C':'G','G':'C','T':'A'}
  ret=''.join([dict_[e] if e in dict_ else e for e in x][::-1])
  return(ret)



def revcomp_baseflanking(x):
  if not isinstance(x, list):
    raise TypeError('`x` must be a list')
  ret=[revcomp(e) for e in x]
  return(ret)
  
def revcomp_basesubstitution(x):
  if not isinstance(x, list):
    raise TypeError('`x` must be a list')
  p_=r"([ACGT])>([ACGT])"
  ret=[">".join([revcomp(re.sub(p_,r"\1",e)),revcomp(re.sub(p_,r"\2",e))]) for e in x]
  return(ret)

