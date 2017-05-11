#!/usr/bin/env python


##  gen_data.py

##  This script demonstrates using the DataGenerator class that is included in the
##  LSH module for generating a CSV datafile for clustering experiments with the LSH
##  module.

##  The DataGenerator class generates N "balls" of multi-variate Gaussion data, where
##  N is the value for the parameter 'how_many_similarity_groups' shown in the
##  constructor call below. Consider an N dimensional cube in the positive quadrant
##  of an N-dimensional space.  Such a cube has 2^N vertices. The N Gaussian balls
##  are centered at the N vertices of the cube that are closest to the origin.


from LocalitySensitiveHashing import *
import numpy

dim = 10                              # data dimensionality
covar = numpy.diag([0.01] * dim)
output_file = 'data_for_lsh.csv'

data_gen = DataGenerator(
                          output_csv_file = output_file,
                          how_many_similarity_groups = 10,
                          dim = dim,
                          number_of_samples_per_group = 8,
                          covariance = covar,
                        )

data_gen.gen_data_and_write_to_csv()
