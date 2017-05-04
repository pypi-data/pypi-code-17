from setuptools import setup, find_packages
import djprogress


setup(
    name='django-progress',
    version=djprogress.__version__,
    url='http://github.com/vikingco/django-progress',
    license='BSD',
    description='Django Progress',
    long_description=open('README.md','r').read(),
    author='Jef Geskens, Unleashed NV',
    author_email='operations@unleashed.be',
    packages=find_packages('.'),
    package_data={'djprogress': [
                    'templates/*.html',
                    'templates/*/*.html',
                    'templates/*/*/*.html'
                    ],
                 },
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
