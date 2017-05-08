from distutils.core import setup

setup(
    name="ppt-time-referee",
    version='0.1',
    py_modules=['referee'],
    description='Simple time-awareness tool for PowerPoint presentations',
    author="Troy Larson",
    author_email='troylar@gmail.com',
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ppt-ref=referee:cli
    ''',
)
