from setuptools import setup, find_packages

setup(
    name="pylama_print",
    version='1.0',
    author="Tobias Schulmann",
    author_email="no@ema.il",
    description="A super-simple pylama linter to flag print() calls",
    url='https://github.com/GeoTob/pylama_print',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
    setup_requires=['pytest-runner', 'pylama'],
    tests_require=['pytest', 'pylama'],
    entry_points={
        'pylama.linter': ['print = pylama_print.linter_print:Linter'],
    }
)
