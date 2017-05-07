from setuptools import setup, find_packages
PACKAGES = find_packages()

opts = dict(name="nbfinder",
            version="1.0.1",

            maintainer="Hadrien Mary",
            maintainer_email="hadrien.mary@gmail.com",

            description="Import Jupyter Notebooks as Modules",
            long_description="Lightweight Python library to import Jupyter Notebook as module in Python file.",

            url="https://github.com/hadim/nbfinder",
            download_url="https://github.com/hadim/nbfinder",
            license="MIT",

            packages=PACKAGES,

            install_requires=[
                      'ipython',
                      'nbformat',
                      ],

            classifiers=(
                   'Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
               ),
            )


if __name__ == '__main__':
    setup(**opts)
