from setuptools import setup, find_packages

setup(
    name='BrosHelp',
    version='0.1.9',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    platforms = 'any',
    include_package_data = True,
    description='BrosHelp Bot',
    url='https://github.com/KayShenA/PythonProjects',
    author='Kay',
    author_email='skyluckyrrb@126.com',
    license='MIT',
    entry_points={
        'console_scripts': [
            'BrosHelp = BrosHelp:start'
        ]
    },
    install_requires=[
        'wxpy',
    ],)
