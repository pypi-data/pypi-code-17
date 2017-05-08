from __future__ import division

import numpy as np


def gaussian(t, p):                 #parameter: amplitude, t0, spread (2*pi*bandwidth)
    return p[0] * np.exp(-0.5 * ((p[1] - t) / p[2]) ** 2.)


def sin(t, p):                   #parameter: amplitude, frequency
    if p[2] <= t:
        p[2] = t
    return p[0] * np.cos(2. * np.pi * p[1] * (t-p[2])) \
                * np.exp(-0.5 * ((p[2] - t) / p[3]) ** 2.)


def modulated_gaussian(t, p):           #parameter: amplitude, frequency, t0, spread
    return p[0] * np.cos(2. * np.pi * p[1] * (t-p[2])) \
                * np.exp(-0.5 * ((p[2] - t) / p[3]) ** 2.)


def dirac(t, p):                     #parameter: amplitude, t0
    if t != p[1]:
        return 0
    elif t == p[1]:
        return p[0]


def rcn(t, p): #parameter: amplitude, frequency, t0, order
    '''
        Raised cosine pulse of order n.
    '''

    a = p[0]
    f = p[1]
    t0 = p[2]
    n = p[3]

    omega_0 = 2.*np.pi*f

    if 0. < (t-t0) < n*2*np.pi/omega_0:
        return a*(-1.)**n/2.*(1.-np.cos(omega_0/n*(t-t0)))*np.cos(omega_0*(t-t0))
    else:
        return 0.


def ricker(t, p):

    a = p[0]
    fp = p[1]
    t0 = p[2]

    return a*(1.-2.*(np.pi*fp*(t-t0))**2)*np.exp(-(np.pi*fp*(t-t0))**2.)
