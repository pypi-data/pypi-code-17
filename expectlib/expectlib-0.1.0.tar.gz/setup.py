from setuptools import setup, find_packages

setup(
    name='expectlib',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/testingrequired/expectlib',
    license='MIT',
    author='Kylee Tilley',
    author_email='kyleetilley@gmail.com',
    description='An expect style assertion library',
    python_requires=">=3.6",
    test_suite="tests"
)
