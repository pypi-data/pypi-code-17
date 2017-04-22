from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name='cydtw',
    ext_modules=cythonize("dtw.pyx"),
    include_dirs=[numpy.get_include()],
    version="0.1.1",
    url="https://github.com/rtavenar/cydtw",
    author="Romain Tavenard",
    author_email="romain.tavenard@univ-rennes2.fr"
)
