from setuptools import setup

setup(
    name='statdials',
    description="LaTeX and Python library to create cute graphical metric dials.",
    version="0.1.2",  # remove git revision if present
    author="Matthew Wardrop",
    author_email="mister.wardrop@gmail.com",
    packages=['statdials'],
    zip_safe=False,
    package_data = {'statdials': ['statdials.sty'],},
    install_requires=[
        'pylatex',
        'wand',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
