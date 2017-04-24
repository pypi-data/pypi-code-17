from setuptools import setup, find_packages


setup(
    name='codeskeleton',
    description='General purpose code skeleton solution.',
    version='1.0.1',
    author='Appresso AS',
    author_email='post@appresso.no',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'termcolor',
        'fire',
        'Jinja2',
        'pyclip-copycat',
    ],
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    entry_points={
        "console_scripts": ['codeskeleton = codeskeleton.cli.codeskeleton_cli:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved',
        'Programming Language :: Python :: 3'
    ],
)
