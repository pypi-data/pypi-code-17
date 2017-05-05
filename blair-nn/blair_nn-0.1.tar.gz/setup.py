from setuptools import setup

setup(name='blair_nn',
      version='0.1',
      description='Simple feed forward Neural Network',
      long_description='Feed forward Neural Network with a single hidden layer trained using vanilla back propogation and stochastic gradient descent',
      author='James Blair',
      author_email='james.blair09@gmail.com',
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.5'],
      install_requires=['numpy', 'pandas', 'matplotlib'],
      packages=['blair_nn'],
      test_suite='nose.collector',
      tests_require=['nose'],
      package_data={'': '*.csv'}
      )
