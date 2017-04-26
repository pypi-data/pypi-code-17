from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ryurest',
      version='0.1',
      description='An unofficial Python library to interact with the REST API of the Ryu SDN Controller.',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='ryu sdn rest api controller python',
      url='https://github.com/nathancatania/ryurest',
      author='Nathan Catania',
      author_email='nathan@nathancatania.com',
      license='Apache 2.0',
      packages=['ryurest'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
