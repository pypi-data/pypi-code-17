# -*- coding: utf-8 -*-

"""
Module used for determining non-user-configurable paths.
"""

#external imports
import os
import inspect
import sys
#internal imports

home = os.path.expanduser("~")

def upNDirsInPath(path,n):
  if n > 0:
    return os.path.dirname(upNDirsInPath(path,n-1))
  else:
    return path

def getPttDir():
  """
  Get the toplevel directory for ptt.
  """
  pathToThisSourceFile = os.path.abspath(inspect.getfile(inspect.currentframe()))
  return upNDirsInPath(pathToThisSourceFile,3)

sys.path.append(os.path.join(getPttDir(),"logic","pttlib"))

def getPttExecutable():
  executable = os.path.join(getPttDir(),"logic","ptt")
  return executable

def getData(filename):
  dataFile = os.path.join(getPttDir(),"logic","pttlib","data",filename)
  if os.path.exists(dataFile):
    with open(dataFile, "rb") as fd:
      return fd.read()
  else:
    import pkgutil
    return pkgutil.get_data("pttlib",os.path.join("data",filename))
