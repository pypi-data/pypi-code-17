# -*- coding: utf-8 -*-
nets=[0]
try: # py Three only
  class Alle(type):
  	def __getattr__(self, name):
  		# import netbase
  		# from netbase import net
  		return nets[0]._all(name, False, False)

  class All(metaclass=Alle):
  	# @classmethod
  	def setNet(nett):
  		nets[0]=nett
except Exception as ex:
  pass
