from setuptools import setup

setup(name='D3GB',
      version='1.1',
      description='Creates an interactive genome browser with python',
      long_description='D3GB is an interactive Web genome browser that can be easily integrated in analysis protocols and shared on the Web. It is distributed as a Python module to facilitate its integration in pipelines and the utilization of platform capabilities.',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Free for non-commercial use',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
      keywords='genome browser d3',
      url='http://d3gb.usal.es/',
      author='Carlos Prieto, David Barrios',
      author_email='bioinfo@usal.com',
      license='CC BY-NC-SA 4.0',
      packages=['D3GB'],
      include_package_data=True,
      zip_safe=False)
