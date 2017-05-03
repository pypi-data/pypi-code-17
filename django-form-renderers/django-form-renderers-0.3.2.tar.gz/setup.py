from setuptools import setup, find_packages


setup(
    name="django-form-renderers",
    version="0.3.2",
    description="Sometimes form.as_p doesn't cut it. This app adds more render methods to all forms. It also adds BEM style CSS classes to all form widgets and inputs.",
    long_description = open("README.rst", "r").read() + open("AUTHORS.rst", "r").read() + open("CHANGELOG.rst", "r").read(),
    author="Praekelt Consulting",
    author_email="dev@praekelt.com",
    license="BSD",
    url="http://www.jmbo.org",
    packages=find_packages(),
    install_requires=[
        "django",
    ],
    tests_require=[
        "tox",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
