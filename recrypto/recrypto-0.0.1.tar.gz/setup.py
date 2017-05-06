from setuptools import setup

librecrypto = ('recrypto', {
    'sources': ['cppsrc/crypto.cpp', 'cppsrc/tools.cpp'],
    'cflags': ['-fno-exceptions',
               '-fno-rtti',
               '-ffast-math',
               '-fsigned-char',
               '-fomit-frame-pointer']
})

setup(
    name="recrypto",
    version="0.0.1",
    description="Python module for Red Eclipse cryptography",
    author="zaquest",
    packages=['recrypto'],
    scripts=["bin/genkey.py"],
    libraries=[librecrypto],
    license="zlib",
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["recrypto_build.py:ffibuilder"],
    install_requires=["cffi>=1.0.0"]
)
