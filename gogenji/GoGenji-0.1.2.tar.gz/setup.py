#python3 setup.py register
#python3 setup.py sdist bdist_wheel --universal upload
# use above in same directory of setup.py to upload to PYPI
from setuptools import setup, find_packages

setup(
    name='GoGenji',
    version='0.1.2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # platforms = 'any',
    include_package_data = True,
    description='GoGenji is a self helper, connecting the whole world within Wechat in peace',
    url='https://github.com/KayShenA/PythonProjects',
    author='Kay',
    author_email='skyluckyrrb@126.com',
    license='MIT',
    entry_points={
        'console_scripts': [
            'GoGenji = GoGenji:start'
        ]
    },
    install_requires=[
        'itchat==1.2.32',
        'requests',
        # 'wxpy',
        ##below for tushares
        'seaborn',
        'matplotlib',
        'python-docx',
        'tushare',
        'pandas',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Topic :: Utilities',
    ]
)
