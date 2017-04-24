import os
from setuptools import find_packages, setup
from setuptools import setup, find_packages
from distutils.util import convert_path

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

main_ns = {}
ver_path = convert_path('orchestrator/version.py')
with open(ver_path) as ver_file:
    exec (ver_file.read(), main_ns)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='hedgehog-field-agent',
    version=main_ns['__version__'],
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0 License',  # example license
    description='Hedgehog station controller.',
    long_description=README,
    url='https://github.com/lordoftheflies/hedgehog-station-controller/',
    author='lordoftheflies',
    author_email='laszlo.hegedus@cherubits.hu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Database',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: System :: Monitoring',
        'Development Status :: 2 - Pre-Alpha'
    ],
    install_requires=[
        "amqp==2.1.4",
        "appdirs==1.4.3",
        "asn1crypto==0.22.0",
        "billiard==3.5.0.2",
        "celery==4.0.2",
        "cffi==1.10.0",
        "cryptography==1.8.1",
        "Django==1.11",
        "django-celery-beat==1.0.1",
        "django-celery-results==1.0.1",
        "django-filter==1.0.2",
        "djangorestframework==3.6.2",
        "docutils==0.13.1",
        "enum34==1.1.6",
        "Fabric==1.13.1",
        "idna==2.5",
        "ipaddress==1.0.18",
        "kombu==4.0.2",
        "Markdown==2.6.8",
        "packaging==16.8",
        "paramiko==2.1.2",
        "psycopg2==2.7.1",
        "pyasn1==0.2.3",
        "pycparser==2.17",
        "pyparsing==2.2.0",
        "pyserial==3.3",
        "pytz==2017.2",
        "pyusb==1.0.0",
        "PyVISA==1.8",
        "PyVISA-py==0.2",
        "PyVISA-sim==0.3",
        "PyYAML==3.12",
        "six==1.10.0",
        "SQLAlchemy==1.1.9",
        "stringparser==0.4.1",
        "vine==1.1.3",
        "netifaces",
        "numpy",
        "scipy",
        "matplotlib",
        "mpld3"

        # 'django',
        # 'channels',
        # 'djangorestframework',
        # 'cronlikescheduler',
        # 'pyyaml',
        # 'pyusb',
        # 'pyserial',
        # 'pyvisa',
        # 'pyvisa-py',
        # 'pyvisa-sim',
        # 'pika',
        # 'jinja2',

    ],
    # entry_points={
    #     'console_scripts': [
    #         'hedgehog-sc-scheduler = orchestrator.celery:main',
    #         'hedgehog-sc-orchestrator = assetadapter.main:main',
    #     ]
    # }
)
