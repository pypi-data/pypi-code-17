import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django_ip2country",
    version = "1.0.4",
    author = "saeed Auditore",
    author_email = "saeed.auditore@gmail.com",
    description = ("Find User Country From IP Address"),
    license = "WTFPL",
    keywords = "django ip2country ipcountry",
    url = "https://github.com/sauditore/django-ip2country",
    packages=find_packages(),
    include_package_data=True,
    data_files=[('',('ip2country/fixtures/data.json',))],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
