from setuptools import setup


setup(
    name='siro_uma.hello',
    version='0.2.0',
    description='A sample Python project',
    long_description='This is a sample to say Hello!',
    url='https://github.com/sirouma/hello',
    author='siro_uma',
    author_email='sirouma.09@gmail.com',
    license='MIT',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Education',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    ],
    keywords='sample setuptools development',
    packages=['hello'],
    entry_points={
        'console_scripts': [
            'hello=hello.hello:hello',
        ],
    },
)
