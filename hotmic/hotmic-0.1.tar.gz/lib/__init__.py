#!/usr/bin/env python

import math
import random

from hotmic import polynomials
from polynomials import *

def lfsr(size, seed=None):
    '''Creates a generator using the Galois linear feedback shift register
algorithm. The *size* corresponds to the entries in
:py:class:`hotmic.polynomials.all_polys`, which represents the bitspace of the
shift register. The *seed* is the initial value to pass to the algorithm.'''
    
    if not size in polynomials.all_polys:
        raise ValueError('bitsize not found in polynomial map')
    
    poly = polynomials.all_polys[size]

    if seed is None:
        seed = 0xACE1 & (2 ** size - 1)
        
    register = seed

    while 1:
        lsb = register & 1
        register >>= 1

        if lsb:
            register ^= poly

        yield register

def xrandrange(start=None, stop=None):
    '''
Produces an iterator similiar to xrange with the interface of range. 
The iterator yields random numbers from 0 <= x < *start* if *stop* is not
specified, or *start* <= x < *stop* if it is. Here's an example of xrandrange::

   >>> list(xrandrange(10))
   [2, 1, 0, 7, 4, 3, 8, 5, 9, 6]
   >>> list(xrandrange(10, 20))
   [11, 10, 16, 13, 12, 17, 14, 18, 15, 19]

'''

    if start is None and stop is None:
        raise ValueError('no stop point specified')

    if not start is None and stop is None:
        stop = start
        start = 0

    if start is None:
        start = 0

    rand_range = stop - start
    
    if rand_range <= 0:
        raise ValueError('empty range given')

    # +/-1 compensates for the fact that 0 is not generated by the lfsr
    bitsize = int(math.floor(math.log(rand_range+1, 2)))+1
    seed = random.randrange(0, 2 ** bitsize - 1)
    lfsr_gen = lfsr(bitsize, seed)

    for value in lfsr_gen:
        if not value > rand_range:
            yield value - 1 + start

        if value == seed:
            break

def randiter(iterable):
    '''
Create an iterator that yields random elements from the iterable object 
*iterable*. It expects the iterable object to implement __getitem__ and __len__.'''

    iter_len = len(iterable)

    for index in xrandrange(iter_len):
        yield iterable[index]


__all__ = ['lfsr', 'xrandrange', 'tap2_polys', 'tap4_polys', 'all_polys', 'polygen']
