from setuptools import setup, find_packages

setup(
    name='expectlib',
    version='0.2.0',
    packages=find_packages(),
    url='https://github.com/testingrequired/expect',
    license='MIT',
    author='Kylee Tilley',
    author_email='kyleetilley@gmail.com',
    description='An expect style assertion library',
    python_requires=">=3.6",
    install_requires=["coverage", "flake8"],
    test_suite="tests"
)
