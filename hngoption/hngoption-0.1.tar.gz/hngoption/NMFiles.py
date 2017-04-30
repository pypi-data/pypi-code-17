###Nelder Mead minimization algorithm


###Function to calculate the mean value of
###a set of n vectors each of dimension n
###namely a (n x n) matrix

def VMean(X, n):
	meanX = [0.0]*n
	for i in range(0, n):
		meanX[i] = 0.0
		for j in range(0, n):
			meanX[i] +=X[i][j]
		meanX[i] = meanX[i]/n
	return meanX
	
# Function to add two vectors together
def VAdd(x, y):
	n = len(x)
	z = [0.0]*n
	for i in range(0, n):
		z[i] = x[i] + y[i]
	return z

# Function to subtract two vectors
def VSub(x, y):
	n = len(x)
	z = [0.0]*n
	for i in range(0, n):
		z[i] = x[i] - y[i]
	return z

# Function to multiply a vector by a constant
def VMult(x, a):
	n = len(x)
	z = [0.0]*n
	for i in range(0, n):
		z[i] = a*x[i]
	return z
	
# Nelder Mead Algorithm
def NelderMeadStep0(f, N, NumIters, x, r):
	# Value of the function at the vertices
	F = [[0 for i in range(2)] for i in range(N+1)]
	
	#Step 0.  Ordering and Best and Worst points
	#Order according to the functional values, compute the best and worst points
	NumIters += 1
	for j in range(N+1):
		z = [0]*N
		for i in range(N):
			z[i] = x[i][j]
		F[j][0] = f(z, r)
		F[j][1] = j
	F.sort()
	#New vertices order first N best initial vectors and
	# last (N+1)st vertice is the worst vector
	# y is the matrix of vertices, ordered so that the worst vertice is last
	
	y = [[0 for i in range(N+1)] for j in range(N)]
	for j in range(N+1):
		for i in range(N):
			y[i][j] = x[i][F[j][1]]
		
	#First best vector y(1) and function value f1
	x1 = [y[i][0] for i in range(N)]
	f1 = f(x1, r)
		
	#Last best vector y(N) and function value fn
	xn = [y[i][N-1] for i in range(N)]
	fn = f(xn, r)
		
	#Worst vector y(N+1) and function value fn1
	xn1 = [y[i][N] for i in range(N)]
	fn1 = f(xn1, r)
		
	#z is the first N vectors from y, excludes the worst y(N+1)
	z = [[0 for i in range(N)] for j in range(N)]
	for j in range(N):
		for i in range(N):
			z[i][j] = y[i][j]
		
	#Mean of best N values and function value fm
	xm = VMean(z, N)
	fm = f(xm, r)
		
	#Reflection point xr and function fr
	xr = VSub(VAdd(xm, xm), xn1)
	fr = f(xr, r)
		
	#Expansion point xe and function fe
	xe = VSub(VAdd(xr, xr), xm)
	fe = f(xe, r)
		
	#Outside contraction point and function foc
	xoc = VAdd(VMult(xr, 0.5), VMult(xm, 0.5))
	foc = f(xoc, r)
		
	#Inside contraction point and function foc
	xic = VAdd(VMult(xm, 0.5), VMult(xn1, 0.5))
	fic = f(xic, r)
	
	#Necessary parameters for steps 1-5 
	return NumIters, y, x1, f1, fn, fn1, xr, fr, xe, fe, xoc, foc, xic, fic
	
def NelderMead(f, N, NumIters, MaxIters, Tolerance, x, r):
	
	#Step0
	NumIters, y, x1, f1, fn, fn1, xr, fr, xe, fe, xoc, foc, xic, fic = NelderMeadStep0(f, N, NumIters, x, r)
	
	while ((NumIters <= MaxIters) and (abs(f1-fn1) >= Tolerance)):
		#Step1. Reflection Rule
		if ((f1 <= fr) and (fr < fn)):
			for j in range(N):
				for i in range(N):
					x[i][j] = y[i][j]
			for i in range(N):
				x[i][N] = xr[i]
			
				
			#go to step 0
			NumIters, y, x1, f1, fn, fn1, xr, fr, xe, fe, xoc, foc, xic, fic = NelderMeadStep0(f, N, NumIters, x, r)
			continue
			
		#Step2. Expansion Rule
		if fr < f1:
			for j in range(N):
				for i in range(N):
					x[i][j] = y[i][j]
			if fe < fr:
				for i in range(N):
					x[i][N] = xe[i]
			else:
				for i in range(N):
					x[i][N] = xr[i]
			#goto step0
			NumIters, y, x1, f1, fn, fn1, xr, fr, xe, fe, xoc, foc, xic, fic = NelderMeadStep0(f, N, NumIters, x, r)
			continue
		#Step3.	Outside contraction Rule
		if ( (fn <= fr) and (fr < fn1) and (foc <= fr) ):
			for j in range(N):
				for i in range(N):
					x[i][j] = y[i][j]
			for i in range(N):
				x[i][N] = xoc[i]
			#goto step 0
			NumIters, y, x1, f1, fn, fn1, xr, fr, xe, fe, xoc, foc, xic, fic = NelderMeadStep0(f, N, NumIters, x, r)
			continue
			
		#Step4. Inside contraction Rule
		if ( (fr >= fn1) and (fic < fn1) ):
			for j in range(N):
				for i in range(N):
					x[i][j] = y[i][j]
			for i in range(N):
				x[i][N] = xic[i]
			#!!! goto step0
			NumIters, y, x1, f1, fn, fn1, xr, fr, xe, fe, xoc, foc, xic, fic = NelderMeadStep0(f, N, NumIters, x, r)
			continue
			
		#Step 5. Shrink Step
		for i in range(N):
			x[i][0] = y[i][0]
		for i in range(N):
			for j in range(N+1):
				x[i][j] = 0.5*(y[i][j] + x[i][0])
		
		#goto step0
		NumIters, y, x1, f1, fn, fn1, xr, fr, xe, fe, xoc, foc, xic, fic = NelderMeadStep0(f, N, NumIters, x, r)
		continue
	
	#Output component
	#Return N parameter values, value of objective function, and number of iterations
	out = [x1[i] for i in range(N)]
	out.append(f1)
	out.append(NumIters)
	return out
	