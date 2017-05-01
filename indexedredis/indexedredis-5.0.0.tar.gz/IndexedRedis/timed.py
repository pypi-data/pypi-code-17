# Copyright (c) 2016 Timothy Savannah under LGPL version 2.1. See LICENSE for more information.
#
# deprecated - Mark things as deprecated.
#

# vim: set ts=8 shiftwidth=8 softtabstop=8 noexpandtab :

import time
import sys

__all__ = ('funcTimeMap', 'timeFunc', 'getFuncTimes')

global funcTimeMap
funcTimeMap = {}


def timeFunc(func):

	if func not in funcTimeMap:
		funcTimeMap[func] = 0.0

	def _timeFunc_wrapper(*args, **kwargs):
		t1 = time.time()
		_exc = None
		try:
			ret = func(*args, **kwargs)
			t2 = time.time()
		except Exception as e:
			t2 = time.time()
			_exc = e

		funcTimeMap[func] += (t2 - t1)
		if _exc is not None:
			raise _exc

		return ret
	return _timeFunc_wrapper


def getFuncTimes():
	
	global funcTimeMap

	ret = []

	for func, totalTime in funcTimeMap.items():
		ret.append ( (func.__qualname__, func, totalTime) )

	ret.sort(key = lambda x : x[2])

	ret.reverse()


	return ret

def printTopTimes(funcTimes, numTop=10):

	topTimes = funcTimes[:numTop]

	ret = []

	maxFirstString = max( [len(x[0]) for x in topTimes ] )

	formatStr = "%-" + str(maxFirstString + 1) + "s    "

	headerLine = (formatStr + "%s") % ( "Func Name", "Total Time" )

	print (headerLine )
	print ( "-" * len(headerLine) )
	print ( "" )

	formatStr += "%.5f"

	for item in topTimes:
		print ( formatStr % (item[0], item[2]) )
		

# vim: set ts=8 shiftwidth=8 softtabstop=8 noexpandtab :
