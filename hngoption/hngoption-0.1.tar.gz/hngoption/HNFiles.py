# Python implementation by Dustin Zacharias (2017), method based on Fabrice Rouah (volopta.com)

# HN Integral

import cmath  
import math

# Trapezoidal Rule passing two vectors
def trapz(X, Y):
	n = len(X)
	sum = 0.0
	for i in range(1, n):
		sum += 0.5*(X[i] - X[i-1])*(Y[i-1] + Y[i])
	return sum
	
# HNC_f returns the real part of the Heston & Nandi integral
def HNC_f(complex_phi, d_alpha, d_beta, d_gamma, d_omega, 
		d_lambda, d_V, d_S, d_K, d_r, i_T, i_FuncNum):
	
	A             = [x for x in range(i_T+1)]
	B             = [x for x in range(i_T+1)]
	complex_zero  = complex(0.0, 0.0)
	complex_one   = complex(1.0, 0.0)
	complex_i     = complex(0.0, 1.0)
	A[i_T]        = complex_zero
	B[i_T]        = complex_zero
	
	for t in range(i_T-1, -1, -1):
		if i_FuncNum == 1:
			A[t] = A[t+1] + (complex_phi + complex_one)*d_r + B[t+1]*d_omega\
				-0.5*cmath.log(1.0 - 2.0*d_alpha*B[t+1])
			B[t] = (complex_phi + complex_one)*(d_lambda + d_gamma) -0.5*d_gamma**2\
				+ d_beta*B[t+1] + (0.5*(complex_phi + complex_one - d_gamma )**2)\
				/(1.0 - 2.0*d_alpha*B[t+1])
		else:
			A[t] = A[t+1] + (complex_phi)*d_r + B[t+1]*d_omega\
					-0.5*cmath.log(1.0 - 2.0*d_alpha*B[t+1])
			B[t] = complex_phi*(d_lambda + d_gamma) -0.5*d_gamma**2 + d_beta*B[t+1]\
				 + (0.5*(complex_phi - d_gamma )**2)/(1.0 - 2.0*d_alpha*B[t+1])
	if i_FuncNum == 1:
		z = (d_K**(-complex_phi) )*(d_S**(complex_phi + complex_one) )\
			*cmath.exp(A[0] + B[0]*d_V)/complex_phi
		return z.real
	else:
		z = (d_K**(-complex_phi) )*(d_S**(complex_phi) )*cmath.exp(A[0] + B[0]*d_V)/complex_phi
		return z.real
		
# Returns the Heston and Nandi option price
def HNC(alpha, beta, gamma, omega, d_lambda, V, S, K, r, T, PutCall):
	
	const_pi  = 4.0*math.atan(1.0)
	High	  = 100
	Increment = 0.25
	NumPoints = int(High/Increment)
	X, Y1, Y2 = [], [], []
	i 		  = complex(0.0, 1.0)
	phi       = complex(0.0, 0.0)
	for j in range(0, NumPoints):
		if j == 0:
			X.append(0.0000001)
		else:
			X.append(j*Increment)
		phi = X[j]*i
		Y1.append(HNC_f(phi, alpha, beta, gamma, omega, d_lambda, V, S, K, r, T, 1 ) )
		Y2.append(HNC_f(phi, alpha, beta, gamma, omega, d_lambda, V, S, K, r, T, 2))
	
	int1 = trapz(X, Y1)
	int2 = trapz(X, Y2)
	P1   = 0.5 + math.exp(-r*T)*int1/S/const_pi
	P2   = 0.5 + int2/const_pi
	if P1 < 0:
		P1 = 0
	if P1 > 1:
		P1 = 1
	if P2 < 0:
		P2 = 0
	if P2 > 1:
		P2 = 1
	
	Call = S/2 + math.exp(-r*T)*int1/const_pi - K*math.exp(-r*T)*(0.5 + int2/const_pi)
	Put  = Call + K*math.exp(-r*T) - S
	if PutCall == 1:
		return Call
	else:
		return Put
	return 0





