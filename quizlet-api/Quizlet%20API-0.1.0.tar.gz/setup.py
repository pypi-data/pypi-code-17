from setuptools import setup
from pip import req


def parse_requirements(filename):
    return [str(ir.req) for ir in req.parse_requirements(filename, session=False)]

__version__ = __import__('quizlet').__version__

setup(
    author_email='pipy@answer,ky',
    author='Answerky',
    description='Python wrapper for Quizlet HTTP API.',
    install_requires=parse_requirements('requirements.txt'),
    name='Quizlet API',
    packages=['quizlet'],
    test_suite="test",
    tests_require=parse_requirements('requirements-test.txt'),
    url='https://github.com/Answerky/quizlet-python',
    version='0.1.0',
)
