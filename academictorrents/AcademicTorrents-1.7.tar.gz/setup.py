from setuptools import setup
from setuptools.command.install import install
from distutils import log

import six, urllib, os, tarfile, sys, logging
import subprocess as sub
import shutil as sh

def message(code, phase):
    if (code == 0):
        six.print_(phase + " successful")
    else:
        six.print_(phase+ " with errors. See install.log")    

def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info('%r', line)

class BuildingLibtorrent(install):
    def run(self):
        ORIGIN = os.getcwd()
        if ('--user' in sys.argv):
            AT_HOME = os.path.join(os.environ['HOME'],".local")
            os.chdir(AT_HOME)
            logging.basicConfig(filename='install.log', filemode='w', level=logging.DEBUG)
            PKG = os.path.join(os.environ['HOME'],"at-pkg")
            os.mkdir(PKG)
            os.chdir(PKG)    
        
            six.print_("Preparing Boost")
            _BOOST_URL = 'https://sourceforge.net/projects/boost/files/boost/1.63.0/boost_1_63_0.tar.gz'
            _BOOST_TB = 'boost_1_63_0.tar.gz'
            _BOOST_DIR='boost_1_63_0'
            urllib.urlretrieve(_BOOST_URL, _BOOST_TB)
            
            six.print_("Preparing Openssl")
            _OPENSSL_URL = 'https://www.openssl.org/source/openssl-1.1.0e.tar.gz'
            _OPENSSL_TB = 'openssl-1.1.0e.tar.gz'
            _OPENSSL_DIR = 'openssl-1.1.0e'
            urllib.urlretrieve(_OPENSSL_URL, _OPENSSL_TB)
            
            six.print_("Preparing Libtorrent")
            _LIBTORRENT_URL = 'https://github.com/arvidn/libtorrent/releases/download/libtorrent-1_1_3/libtorrent-rasterbar-1.1.3.tar.gz'
            _LIBTORRENT_TB = 'libtorrent-rasterbar-1.1.3.tar.gz'
            _LIBTORRENT_DIR = 'libtorrent-rasterbar-1.1.3'
            urllib.urlretrieve(_LIBTORRENT_URL, _LIBTORRENT_TB)
            
            six.print_("Uncompressing libraries")
            for lib in [_BOOST_TB,_OPENSSL_TB,_LIBTORRENT_TB]:
                six.print_("Uncompressing " + lib)
                tar = tarfile.open(lib)
                tar.extractall()
            tar.close()
            WITH_PYTHON = os.popen('which python2.7').read()
            six.print_("Python executable to use is: " + WITH_PYTHON)
            
            six.print_("Configuring Openssl")
            os.chdir(os.path.join(PKG,_OPENSSL_DIR))
        
            cmd = ['./config','--prefix=%s'%AT_HOME,'--openssldir=%s'%os.path.join(AT_HOME,"ssl")]
        
            p = sub.Popen(cmd, stdout=sub.PIPE)
            with p.stdout:
                log_subprocess_output(p.stdout)    
            p.wait()
            message(p.returncode,six.text_type("Openssl"))
            
            six.print_("Make Openssl")
            os.chdir(os.path.join(PKG,_OPENSSL_DIR))
            p = sub.Popen(['make'], stdout=sub.PIPE, stderr=sub.STDOUT)
            with p.stdout:
                log_subprocess_output(p.stdout)
            p.wait()
            message(p.returncode,six.text_type("Make Openssl"))
            
            six.print_("Make test Openssl")
            os.chdir(os.path.join(PKG,_OPENSSL_DIR))
            p = sub.Popen(['make', 'test'], stdout=sub.PIPE, stderr=sub.STDOUT)
            with p.stdout:
                log_subprocess_output(p.stdout)
            p.wait()
            message(p.returncode,six.text_type("Make test Openssl"))             
            
            six.print_("Make install Openssl")
            os.chdir(os.path.join(PKG,_OPENSSL_DIR))
            p = sub.Popen(['make', 'install'], stdout=sub.PIPE, stderr=sub.STDOUT)
            with p.stdout:
                log_subprocess_output(p.stdout)
            p.wait()
            message(p.returncode,six.text_type("Make install Openssl"))            
            
            six.print_("Bootstrapping Boost")
            os.chdir(os.path.join(PKG,_BOOST_DIR))
            
            cmd = ['./bootstrap.sh','--with-python=%s'%WITH_PYTHON,'--prefix=%s'%AT_HOME]
            
            p = sub.Popen(cmd, stdout=sub.PIPE)
            with p.stdout:
                log_subprocess_output(p.stdout)    
            p.wait()
            message(p.returncode,six.text_type("Bootstrap"))
            
            six.print_("Building Boost C++ libraries")
            cmd = ['./b2','-s','NO_BZIP2=1','--with-system','--with-date_time','--with-python','--with-chrono',
                   '--with-random','install','--prefix=%s'%AT_HOME]
            
            p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT)
            with p.stdout:
                log_subprocess_output(p.stdout)
            p.wait()
            message(p.returncode,six.text_type("Building"))
            
            six.print_("Configuring Libtorrent")
            os.chdir(os.path.join(PKG,_LIBTORRENT_DIR))
            cmd = ['./configure','--enable-python-binding','--disable-dependency-tracking','--disable-silent-rules',
                   'PYTHON=%s'%WITH_PYTHON,'--prefix=%s'%AT_HOME,'--with-boost=%s'%AT_HOME,'--with-libiconv',
                   '--with-boost-python=boost_python','--with-openssl=%s'%AT_HOME,'BOOST_ROOT=%s'%os.path.join(PKG,_BOOST_DIR)]
                
            p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT)
            with p.stdout:
                log_subprocess_output(p.stdout)
            p.wait()
            message(p.returncode,six.text_type("Configuring Libtorrent"))
            
            six.print_("Making Libtorrent")
            os.chdir(os.path.join(PKG,_LIBTORRENT_DIR))
            p = sub.Popen(['make'], stdout=sub.PIPE, stderr=sub.STDOUT)
            with p.stdout:
                log_subprocess_output(p.stdout)
            p.wait()
            message(p.returncode,six.text_type("Making Libtorrent"))
            
            six.print_("Make install Libtorrent")
            os.chdir(os.path.join(PKG,_LIBTORRENT_DIR))
            p = sub.Popen(['make', 'install'], stdout=sub.PIPE, stderr=sub.STDOUT)
            with p.stdout:
                log_subprocess_output(p.stdout)
            p.wait()
            message(p.returncode,six.text_type("Making install Libtorrent"))  
            
            sh.rmtree(PKG)
            six.print_("Building of all C++ libraries finished")
            
            six.print_("Creating .at_profile")
            with open(os.path.join(os.environ['HOME'],".at_profile"), "w") as outfile:
                outfile.write("export LD_LIBRARY_PATH=" + os.path.join(AT_HOME,"lib") + "\n")
                outfile.write("export PKG_CONFIG_PATH=" + os.path.join(AT_HOME,"lib","pkgconfig")) 
            
            six.print_("Finished custom install")
            os.chdir(ORIGIN)        
        
        install.run(self)
        import pip
        required_packages = self.distribution.install_requires
        for package in required_packages:
            self.announce('Installing %s...' % package, log.INFO)
            pip.main(['install','--user',package])
        self.announce('Dependencies installed.')        

setup(
    name = 'AcademicTorrents',
    version = '1.7',
    author = 'Ronald Barrios',
    author_email = 'ronald.degmar@gmail.com',
    packages = ['urwid'],
    include_package_data = True,
    keywords = 'torrent bittorrent p2p fileshare filesharing',
    long_description = """AcademicTorrents is a bittorrent client that has
        been developed in order to be used in servers where you cannot sudo. 
        AcademicTorrents uses libtorrent in it's backend to handle the 
        bittorrent protocol. Console User Interface has been developed by
        using urwid, curses, and npyscreen python libraries""",
    license = 'GPLv3',
    py_modules = ['menu', 'console', 'academictorrents','view','prior'],
    entry_points = {
        'console_scripts': ['at-console = console:main'],
    },
    install_requires=[
        'npyscreen',
    ],    
    cmdclass = {
        'install': BuildingLibtorrent
    }    
)
