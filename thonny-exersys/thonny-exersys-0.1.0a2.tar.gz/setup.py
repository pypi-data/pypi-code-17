from setuptools import setup
import os.path
import sys

setupdir = os.path.dirname(__file__)

requirements = []
for line in open(os.path.join(setupdir, 'requirements.txt'), encoding="ASCII"):
    if line.strip() and not line.startswith('#'):
        requirements.append(line)

setup(
      name="thonny-exersys",
      version="0.1.0a2",
      description="Exercise management plug-in for Thonny",
      long_description="""Thonny is a simple Python IDE with features useful for learning programming. See http://thonny.org for more info.
thonny-exersys adds infrastructure for opening programming exercises.""",
      url="https://bitbucket.org/plas/thonny-exersys/",
      author="Aivar Annamaa",
      license="MIT",
      classifiers=[
        "Development Status :: 3 - Alpha",
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
        "Topic :: Text Editors",
      ],
      keywords="IDE education programming exercises",
      platforms=["Windows", "macOS", "Linux"],
      python_requires=">=3.4",
      install_requires=requirements,
      py_modules=["thonnycontrib.exersys",
                "thonnycontrib.moodle_vpl"],
)