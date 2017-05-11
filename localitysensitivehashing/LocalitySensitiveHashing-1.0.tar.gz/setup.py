#!/usr/bin/env python

### setup.py

#from distutils.core import setup

from setuptools import setup, find_packages

setup(name='LocalitySensitiveHashing',
      version='1.0',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='https://engineering.purdue.edu/kak/distLSH/LocalitySensitiveHashing-1.0.html',
      download_url='https://engineering.purdue.edu/kak/distLSH/LocalitySensitiveHashing-1.0.tar.gz#md5=a59feac7509d8e3f323d170d470583a2',
      description='A Python implementation of Locality Sensitive Hashing for finding nearest neighbors and clusters in multidimensional numerical data',
      long_description='''


Consult the module API page at

    https://engineering.purdue.edu/kak/distLSH/LocalitySensitiveHashing-1.0.html

for all information related to this module, including
information regarding the latest changes to the code. The
page at the URL shown above lists all of the module
functionality you can invoke in your own code.

Locality Sensitive Hashing (LSH) is a computationally
efficient approach for finding nearest neighbors in large
datasets.  The main idea in LSH is to avoid having to
compare every pair of data samples in a large dataset in
order to find the nearest similar neighbors for the
different data samples.  With LSH, one can expect a data
sample and its closest similar neighbors to be hashed into
the same bucket with a high probability.  By treating the
data samples placed in the same bucket as candidates for
similarity checking, we significantly reduce the
computational burden associated with similarity detection in
large datasets.

While LSH algorithms have traditionally been used for
finding nearest neighbors, this module goes a step further
and explores using LSH for clustering the data.  Strictly
speaking, this violates the basic mandate of LSH, which is
to return just the nearest neighbors. (A being a nearest
neighbor of B and B being a nearest neighbor of C, in the
sense such nearest neighbors are defined in the context of
LSH, does not imply that A and C will always be sufficiently
close to be considered similar.)  Nonetheless, if you
believe that your datafile consists of non-overlapping data
clusters, this module may do a decent job of finding those
clusters.

Typical usage syntax for invoking LocalitySensitiveHashing
in your own code:

::

        from LocalitySensitiveHashing import *
        datafile = "data_for_lsh.csv"
        lsh = LocalitySensitiveHashing( 
                           datafile = datafile,
                           dim = 10,
                           r = 50,         
                           b = 100,        
                           expected_num_of_clusters = 10,
                  )
        lsh.get_data_from_csv()
        lsh.initialize_hash_store()
        lsh.hash_all_data()
        similarity_groups = lsh.lsh_basic_for_neighborhood_clusters()
        coalesced_similarity_groups = lsh.merge_similarity_groups_with_coalescence( similarity_groups )
        merged_similarity_groups = lsh.merge_similarity_groups_with_l2norm_sample_based( coalesced_similarity_groups )
        lsh.write_clusters_to_file( merged_similarity_groups, "clusters.txt" )


          ''',
      license='Python Software Foundation License',
      keywords='locality sensitive hashing, nearest neighbor calculation, hashing with hyperplanes, clustering',
      platforms='All platforms',
      classifiers=['Topic :: Utilities', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.5'],
      packages=['LocalitySensitiveHashing']
)
