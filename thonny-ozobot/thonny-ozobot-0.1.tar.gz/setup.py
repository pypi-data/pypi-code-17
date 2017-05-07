from setuptools import setup
import os.path

setupdir = os.path.dirname(__file__)

requirements = []
for line in open(os.path.join(setupdir, 'requirements.txt'), encoding="UTF-8"):
    if line.strip() and not line.startswith('#'):
        requirements.append(line)

setup(
      name="thonny-ozobot",
      version="0.1",
      description="A thonny plugin that adds Ozobot programming support",
      long_description="""This is a Thonny plugin that adds Ozobot programming support via a pyhton like language.
      More info about the pyhton like language: https://github.com/Kaarel94/Ozobot-Python.
      More info about Thonny: http://thonny.org.""",
      url="https://bitbucket.org/kaarel94/thonny-ozobot",
      author="Kaarel Maidre",
	  author_email="kaarel.maidre@gmail.com",
      license="MIT",
      classifiers=[
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: Freeware",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Education",
        "Topic :: Software Development",
      ],
      keywords="IDE education programming ozobot",
      platforms=["Windows", "macOS", "Linux"],
      python_requires=">=3.4",
      install_requires=requirements,
      packages=["thonnycontrib.ozobot"],
)