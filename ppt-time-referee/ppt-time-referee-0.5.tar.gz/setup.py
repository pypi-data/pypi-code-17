from distutils.core import setup

setup(
    name="ppt-time-referee",
    version='0.5',
    py_modules=['referee','time_referee'],
    description='Simple time-awareness tool for PowerPoint presentations',
    author="Troy Larson",
    author_email='troylar@gmail.com',
    install_requires=[
        'Click','arrow','time_referee'
    ],
    entry_points='''
        [console_scripts]
        ppt-ref=referee:cli
    ''',
)
