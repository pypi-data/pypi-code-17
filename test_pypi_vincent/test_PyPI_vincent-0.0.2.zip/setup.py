# encoding=utf-8

from setuptools import setup

setup(
    name='test_PyPI_vincent',
    version='0.0.2',
    author='vincent',
    author_email='szxwpp@163.com',
    url='https://zhuanlan.zhihu.com/p/26159930',
    description=u'吃枣药丸',
    packages=['test_PyPI_vincent'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'test=test_PyPI_vincent:test',
            'run=test_PyPI_vincent:run'
        ]
    }
)

# console_scripts提供终端命令，test执行 test_PyPI_vincent 包下（__init__ 中）的 test 函数

# python setup.py register sdist upload 三个命令
# sdist 压缩格式，可以用pip安装，bdist_egg 支持 easy_install 安装