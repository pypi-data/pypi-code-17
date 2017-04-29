from setuptools import setup, find_packages
import os.path

def get_version():
    """Returns the package version taken from version.py.
    """
    root = os.path.dirname(__file__)
    version_path = os.path.join(root, "rorocloud/version.py")
    with open(version_path) as f:
        code = f.read()
        env = {}
        exec(code, env, env)
        return env['__version__']

__version__ = get_version()

setup(
    name='rorocloud',
    version=__version__,
    author='rorodata',
    author_email='rorodata.team@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==6.7',
        'requests==2.13.0',
        'web.py>=0.40.dev',
        'tabulate==0.7.7'
    ],
    entry_points='''
        [console_scripts]
        rorocloud=rorocloud.cli:main
        rorocloud-dev=rorocloud.cli:main_dev
    ''',
)
