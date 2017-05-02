from setuptools import setup, find_packages

setup(
    name='patois-stop-words',
    version='0.0.1',
    description='A list of patois stop words.',
    long_description=open('README.md').read(),
    license='MIT',
    author='Alexander Nicholson',
    author_email='alexj.nich@hotmail.com',
    url='https://github.com/ANich/patois-stop-words',
    packages=find_packages(),
    package_data={
                'patois_stop_words': ['words.txt']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='patois'
)
