import math
import logging

class ComplexityResolver:

	@staticmethod
	def Resolve(points):
		minDifference = 100
		bestStr = None
		for exp in range (1,10):
			r = ComplexityResolver.CheckComplexity(points, exp, False)
			if r["dif"] < minDifference:
				minDifference = r["dif"]
				bestStr = r["str"]
			
			r = ComplexityResolver.CheckComplexity(points, exp, True)
			if r["dif"] < minDifference:
				minDifference = r["dif"]
				bestStr = r["str"]	
				
		return bestStr
	
	@staticmethod
	def CheckComplexity(points, exp, withLog):
		# Without logarithm
		listA = []
		for i in points:
			n = i["N"]
			t = i["time"]
			if withLog == True:
				listA.append(t/ComplexityResolver.ComputeExponent(n, exp)/math.log(n, 2))
			else:
				listA.append(t/ComplexityResolver.ComputeExponent(n, exp))
		
		avg = 0
		for i in listA:
			avg += i;
		avg /= len(listA)
		
		biggestDif = 0
		secondBiggestDif = 0
		
		for i in listA:
			dif = abs(i/avg*100.0 - 100.0)
			if dif > biggestDif:
				secondBiggestDif = biggestDif
				biggestDif = dif
			elif dif > secondBiggestDif:
				secondBiggestDif = dif
		
		logging.debug("Exponent: {0}, computing with logaritm: {1}".format(exp, withLog))
		logging.debug("Parameter values {0}".format(listA))
		logging.debug("Average: {0}, biggestDif: {1}\n".format(avg, biggestDif))
		
		if withLog == True:
			str = "n^{0}log(n)".format(exp)
		else:
			str = "n^{0}".format(exp)

		return { "dif": secondBiggestDif, "str": str }
	
	@staticmethod
	def ComputeExponent(N, i):
		res = 1;
		for t in range(1,i+1):
			res *= N
			
		return res