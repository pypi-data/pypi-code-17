from setuptools import setup

setup(name='sspyrs',
      version='0.1a0',
      description='Lightweight interface for SSRS reports to python',
      url='',
      author='James Nix',
      author_email='jnix@garretsongroup.com',
      license='MIT',
      packages=['sspyrs'],
      dependency_links=['https://github.com/requests/requests-ntlm'],
      install_requires=[
           'pandas>=0.18.1',
           'xmltodict==0.10.2'
      ],
      keywords=['ssrs', 'reporting', 'sql server'],
      zip_safe=False)
