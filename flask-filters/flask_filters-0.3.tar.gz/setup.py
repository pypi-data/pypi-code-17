# setup file for flask filters

from setuptools import setup

setup(name='flask_filters',
      version='0.3',
      description='The Flask Filter to use with flask-restful and Relational DB',
      url='https://gitlab.com/yogeshkamble/flask-filters',
      author='Yogesh Kamble',
      author_email='yogesh.kamble102@gmail.com',
      license='MIT',
      packages=['flask_filters'],
      install_requires=[
            'Flask-RESTful',
            'SQLAlchemy',
            'nose'
      ],
      zip_safe=False)


