import setuptools
import logging

log = logging.getLogger(__name__)
long_description = open('README.md').read().strip()

try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError) as err:
    log.error('cannot convert README.md', err)

setuptools.setup(name='callfire-api-client-python',
                 version='0.0.7',
                 description='CallFire API v2 Python client. Connect voice and text services to your application.',
                 long_description=long_description,
                 author='Vladimir Mikhailov',
                 author_email='vmikhailov@callfire.com',
                 url='https://github.com/CallFire/callfire-api-client-python',
                 packages=['callfire'],
                 install_requires=[
                     "bravado"
                 ],
                 package_data={
                     'readme': ['README.md']
                 },
                 license='MIT License',
                 zip_safe=False,
                 keywords='CallFire API v2 Python SDK messaging sms mms dialing calls texts',
                 classifiers=[
                     'Development Status :: 4 - Beta',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.6'
                 ])
