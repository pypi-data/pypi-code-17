from setuptools import setup, find_packages

from django_fast_test import __version__ as version_str



setup(
    name = "django-fast-test",
    version = version_str,
    license = "MIT",
    description = "Django fast test command.",
    author = "Mengjun Liu",
    author_email = "mengjun18@gmail.com",
    url = "https://github.com/liumengjun/django-fast-test",
    packages = find_packages(),
    install_requires = [
        "django>=1.7",
    ],
    extras_require = {
        "test": [
        ],
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Django",
    ],
)
