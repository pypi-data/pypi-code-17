from setuptools import setup
from douyu import __VERSION__

version = __VERSION__

setup(
    name='fitz-douyu',
    packages=['douyu', 'douyu.chat', 'douyu.chat.network'],
    version=version,
    description='Python Wrapper for DouyuTV APIs, including support for accessing ChatRoom, e.g. DanMu',
    author='Junkai Cao',
    author_email='caojunkaiv@gmail.com',
    url='https://github.com/caojunkai/douyu',
    download_url='https://github.com/douyu',
    keywords=['douyu', 'douyutv', 'danmu', 'chat'],
    classifiers=[],
)
