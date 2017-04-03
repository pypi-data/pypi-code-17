# -*- coding: utf-8 -*-

# import netbase
version = "0.1.17"
# from netbase import world, the, net, Netbase
# from netbase import Netbase
from .netbase import Netbase, All, The, purge_caches
# from netbase import Netbase, All, The, reload

# from netbase import net, Netbase
# if py3:
# 	from alle import All
#
world = net = Netbase()
the = The()
alle= All()


#
#
# class Alle(type):
# 	def __getattr__(self, name):
# 		return net._all(name, False, False)
#
#
# class All:
# 	__metaclass__ = Alle

# print(All.USA)
# print(the.USA)

# net = netbase.net
# the = netbase.world
# cache = netbase.cache
# import netbase
# import netbase
