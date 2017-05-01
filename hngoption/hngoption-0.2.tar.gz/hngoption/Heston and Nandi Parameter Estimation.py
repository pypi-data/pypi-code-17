# Python implementation by Dustin Zacharias (2017), method based on Fabrice Rouah (volopta.com)

#Log Likelihood Estimation

from LogLikelihood import LogLike
from NMFiles import NelderMead

def main():
	
	#Settings for Nelder Mead Algorithm
	NumIters = 1		#First Iteration
	MaxIters = 1e3		#Maximum number of iterations
	Tolerance = 1e-5    #Tolerance on best and worst function values
	N = 5				#Number of Heston and Nandi parameters
	r  = 0.05 / 252.0   #Risk Free Rate
	
	#Heston and Nandi parameter starting values (vertices) in vector form
	
	x = [[0 for i in range(N+1)] for j in range(N)]
	x[0][0]= 5.02e-6;  x[0][1]= 5.12e-6;  x[0][2]= 5.00e-6;  x[0][3]= 4.90e-6;  x[0][4]= 4.95e-6;  x[0][5]= 4.99e-6   # omega
	x[1][0]= 1.32e-6;  x[1][1]= 1.25e-6;  x[1][2]= 1.35e-6;  x[1][3]= 1.36e-6;  x[1][4]= 1.30e-6;  x[1][5]= 1.44e-6   # alpha
	x[2][0]= 0.79;     x[2][1]= 0.80;     x[2][2]= 0.78;     x[2][3]= 0.77;     x[2][4]= 0.81;     x[2][5]= 0.82      # beta
	x[3][0]= 427.0;    x[3][1]= 421.0;    x[3][2]= 425.0;    x[3][3]= 419.1;    x[3][4]= 422.1;    x[3][5]= 430.0     # gamma
	x[4][0]= 0.21;     x[4][1]= 0.20;     x[4][2]= 0.22;     x[4][3]= 0.19;     x[4][4]= 0.18;     x[4][5]= 0.205     # lambda
	
	
	#Run Nelder Mead and output Nelder Mead results
	B = NelderMead(LogLike, N, NumIters, MaxIters, Tolerance, x, r)
	
#	print("Nelder Mead Minimization of Log-Likelihood for Heston and Nandi parameters")
#	print("---------------------------------")
#	print("omega  = ", B[0])
#	print("alpha  = ", B[1])
#	print("beta   = ", B[2])
#	print("gamma  = ", B[3])
#	print("lambda = ", B[4])
#	print("Value of Objective Function = ", B[N])
#	print("Number of Iterations = ", B[N+1])
#	print("Persistence ", B[2]+B[1]*(B[3]**2) )
#	print("---------------------------------")

	#alpha,beta,gamma,omega,lambda
	return [B[1],B[2],B[3],B[0],B[4]]
	
if __name__ == '__main__':
	main()