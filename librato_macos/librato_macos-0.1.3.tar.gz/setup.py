from setuptools import setup

setup(name="librato_macos",
      version="0.1.3",
      description="A library to submit measurements to Librato for a MAC OS instance",
      url="http://www.librato.com",
      author="librato",
      author_email="support@librato.com",
      scripts=["bin/librato-macos"],
      license="MIT",
      packages=["librato_macos"],
      install_requires=[
          "psutil>=5.0.1",
          "cement>=2.10.2",
          "librato-metrics>=2.1.2",
          "six>=1.10.0"
      ],
      zip_safe=False)
