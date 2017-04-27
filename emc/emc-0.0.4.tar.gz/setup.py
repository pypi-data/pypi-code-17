'''
Distutils setups file for C++ library for EMC genetic string manipulation.
@author: Csaba Sulyok
'''

from distutils.core import setup, Extension
from os import walk, environ, getcwd, remove
from os.path import dirname, exists, abspath, isfile
from platform import system
from re import search
from shutil import copy, rmtree
from sys import argv

import numpy

from emc.helper.processes import killOtherPys

module_name = 'emcpp'

numpy_include = numpy.get_include()

'''
On Windows, FFTW must be put in a folder signalled by the env variable FFTW_HOME.
On Linux, simply apt-get install libfftw3-dev.
'''
if system() is 'Windows':
    fftw_dir = environ['fftw_home']
    fftw_libname = 'libfftw3f-3'
else:
    fftw_dir = '/usr'
    fftw_libname = 'fftw3f'

fftw_include = fftw_dir + '/include'
fftw_libdir = fftw_dir + '/lib'


def findSources():
    '''
    Find all source files to SWIG.
    These are the files ending in ".cpp" but not "_wrap"
    '''
    ret = ['emc/cpp/swig/emcpp.i']
    for root, _, filenames in walk('emc/cpp'):
        for filename in filenames:
            match = search('(.*)\\.cpp$', filename)
            if match and not match.group(1).endswith('_wrap'):
                ret.append("%s/%s" %(root, filename))
    print 'Using following sources:', ret
    return ret


def findPackages():
    rootDir = 'emc'
    packages = []
    for dirName, _, fileList in walk(rootDir):
        hasinit = False
        for fname in fileList:
            if fname == '__init__.py':
                hasinit = True
                
        if hasinit:
            packages.append(dirName.replace('/', '.'))
    return packages


def main():
    killOtherPys()

    print len(argv)
    if len(argv) < 2:
        print 'No arguments, using default: build'
        argv.append('build')

    extension = Extension('_emcpp',
                          sources = findSources(),
                          swig_opts = ['-c++'],
                          include_dirs = [numpy_include, fftw_include],
                          libraries = [fftw_libname],
                          library_dirs = [fftw_libdir])
    
    setup(name = 'emc',
          packages=findPackages(),
          version='0.0.4',
          description='evolutionary music composition.',
          author='Csaba Sulyok',
          author_email='csaba.sulyok@gmail.com',
          url='https://bitbucket.org/csabasulyok/emc',
          keywords=['emc'],
          ext_modules = [extension],
          install_requires=['psutil==5.1.3', 'numpy==1.9.2', 'tymed==0.0.2'])
    
    if 'clean' in argv:
        cleanExtra()

    if 'build' in argv or 'build_ext' in argv or 'install' in argv:
        '''
        currentDir = abspath(dirname(__file__))
        srcDir =  abspath("%s/../src/cpp/swig" %currentDir)
        movePyWrappers(srcDir)
        '''
        copyBinary()



def cleanExtra():
    '''
    Extra clean steps not done by distutils.
    Remove SWIG interface, wrapper C class and full build folder.
    '''
    print 'Removing extra files'
    cd = getcwd()
    
    swigInt = "%s/%s.py" %(cd, module_name)
    buildDir = "%s/build" %(cd)
    pyd = "%s/_%s.pyd" %(cd, module_name)
    so = "%s/_%s.so" %(cd, module_name)
    
    for f in [swigInt, pyd, so]:
        if isfile(f):
            print "Removing '%s'" %(f)
            remove(f)
        else:
            print "'%s' doesn't exist. Remove aborted." %(f)
        
    if exists(buildDir):
        print "Removing '%s'" %(buildDir)
        rmtree(buildDir)
    else:
        print "'%s' doesn't exist. Remove aborted." %(buildDir)


def copyBinary():
    print ''
    print "Post-build script"
    print "================="

    if system() is 'Windows':
        binaryDir = 'build/lib.win-amd64-2.7'
        binaryName = '_emcpp.pyd'
    else:
        binaryDir = 'build/lib.linux-x86_64-2.7'
        binaryName = '_emcpp.so'

    currentDir = abspath(dirname(__file__))
    srcFile = "%s/%s/%s" %(currentDir, binaryDir, binaryName)
    destFile = "%s/%s" %(currentDir, binaryName)

    if not exists(srcFile):
        print 'Warning: compilation of %s failed. See logs.' % srcFile
        return

    print "Moving binary %s to current folder" % binaryName
    if exists(destFile):
        print "Already exists, overwriting"
        remove(destFile)
    copy(srcFile, destFile)

    print "================"
    print ''

    
if __name__ == "__main__":
    main()
