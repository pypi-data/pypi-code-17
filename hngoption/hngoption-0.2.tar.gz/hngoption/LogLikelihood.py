# Log Likelihood function for Heston and Nandi Model
from math import log, sqrt
# Returns the sum of a vector's elements
def VecSum(x):
	n = len(x)
	Sum = 0.0
	for i in range(0, n):
		Sum += x[i]
	return Sum

# Returns the sample variance
def VecVar(x):
	n = len(x)
	mean = VecSum(x) / n
	sumV = 0.0
	for i in range(0, n):
		sumV += (x[i] - mean)**2
	return sumV / (n-1)



# Returns the log-likelihood based on S&P500 returns
def LogLike(B, r, Price=prices):
	#Price = prices
	#i  = 0
	#with open('SP500.txt', 'r') as inPrices:
	#	for line in inPrices:
	#		try:
	#			Price.append(float(line))
	#			i += 1
	#		except:
	#			continue
			
	N = len(Price)
	#Calculate S&P500 returns
	ret = [0.0]*(N-1)
	for i in range(0, N-1):
		ret[i]=(log(Price[i]/Price[i+1]) )
	
	Variance = VecVar(ret)
	h = [0*i for i in range(N-1)]
	Z = [0*i for i in range(N-1)]
	L = [0*i for i in range(N-1)]
	
	#Construct GARCH(1,1) process by working back in time
	h[N-2] = Variance
	Z[N-2] = (ret[N-2] - r - B[4]*h[N-2]) / h[N-2]**0.5
	L[N-2] = -log(h[N-2]) - (ret[N-2]**2) / h[N-2]
	
	for i in range(N-3, -1, -1):
		h[i] = B[0] + B[2]*h[i+1] + B[1]*pow(Z[i+1] - B[3]*sqrt(h[i+1]), 2)
		Z[i] = (ret[i] - r - B[4]*h[i]) / (h[i]**0.5)
		L[i] = -log(h[i]) - (ret[i]**2) / h[i]
	
	LogL = VecSum(L)
	if ((B[0]<0) | (B[1]<0) |(B[2]<0) |(B[3]<0) |(B[4]<0)):   #(B[2]+B[1]*pow(B[3],2)>=1))
		return 1e50
	else:
		return -LogL    #Minimize -Log-Like(Beta)