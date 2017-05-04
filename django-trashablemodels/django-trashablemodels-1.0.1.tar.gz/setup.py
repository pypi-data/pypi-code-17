from setuptools import setup, find_packages
import trashable


setup(
    name='django-trashablemodels',
    version=trashable.__version__,
    url='https://github.com/vikingco/django-trashablemodels',
    license='MIT License',
    description='Implements a soft delete option for model instances',
    long_description=open('README.md', 'r').read(),
    author='Unleashed NV',
    author_email='operations@unleashed.be',
    packages=find_packages('.'),
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
    install_requires=[
        'Django'
    ]
)
