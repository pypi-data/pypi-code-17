from setuptools import setup

setup(name='kerutils',
    version='1.23',
    description='Keras utilities',
    url='http://github.com/samyzaf/kerutils',
    author='Samy Zafrany',
    author_email='admin@samyzaf.com',
    license='MIT',
    packages=['kerutils'],
    install_requires=['keras', 'ezprogbar', 'numpy', 'scipy', 'matplotlib', 'h5py'],
    zip_safe=False,
)

