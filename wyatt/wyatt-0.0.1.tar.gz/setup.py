from distutils.core import setup
from setuptools.command.install import install
import shutil
import os
print(os.getcwd())
DEST="/usr/local/bin/"
def setCommands():
    print(os.getcwd())
#    shutil.copy("get", DEST+"get")
#    shutil.copy("send", DEST+"send")    
    return

class PostInstallCommand(install):
    def run(self):
        setCommands()
        install.run(self)
setup(name='wyatt',
      version='0.0.1',
      description='A way to talk to will wyatt.',
      author='wyatt',
      author_email='goFuck@your.self',
      url='https://iex.ist',
      packages=['will',],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
                ],
      cmdclass={'install': PostInstallCommand,},
     )
