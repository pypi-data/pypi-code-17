from distutils.core import setup

setup(
    name='bbridge_sdk',
    packages=['bbridge_sdk', 'bbridge_sdk.entity', 'bbridge_sdk.entity.enum', 'bbridge_sdk.entity.request',
              'bbridge_sdk.entity.response', 'bbridge_sdk.entity.serialize'],
    version='0.3',
    description='The library enables you to make requests such as user profiling, image object detection, etc.',
    author='bBridge Team',
    author_email='support@bbridge.net',
    license='MIT',
    url='https://github.com/bbridge-team/bbridge-sdk-python',
    download_url='https://github.com/bbridge-team/bbridge-sdk-python/archive/v0.3.tar.gz',
    keywords=['bbridge', 'sdk', 'user profiling', 'nlp', 'image processing'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
