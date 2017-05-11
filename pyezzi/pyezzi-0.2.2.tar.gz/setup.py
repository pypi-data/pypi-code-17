from setuptools import setup, Extension

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext

    extensions = cythonize([
        Extension(
            "pyezzi.laplace",
            ["pyezzi/laplace.pyx"],
        ),
        Extension(
            "pyezzi.yezzi",
            ["pyezzi/yezzi.pyx"],
        )
    ])
    cmdclass = {"build_ext": build_ext}
except ImportError:
    extensions = [
        Extension(
            "pyezzi.laplace",
            ["pyezzi/laplace.c"],
        ),
        Extension(
            "pyezzi.yezzi",
            ["pyezzi/yezzi.c"],
        )
    ]
    cmdclass = {}

setup(
    name="pyezzi",
    version="0.2.2",
    description="Thickness calculation on binary 3D images",
    long_description=long_description,
    ext_modules=extensions,
    license="GPL",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='medical image processing',
    packages=["pyezzi"],
    install_requires=['numpy'],
    cmdclass=cmdclass,
    url="https://gitlab.inria.fr/ncedilni/pyezzi",
    author="Nicolas Cedilnik",
    author_email="nicoco@nicoco.fr"
)
