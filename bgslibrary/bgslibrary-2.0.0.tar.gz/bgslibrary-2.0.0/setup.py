#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of BGSLibrary.
# BGSLibrary is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# BGSLibrary is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with BGSLibrary.  If not, see <http://www.gnu.org/licenses/>.

"""
Python package for bgslibrary.
Please see https://github.com/andrewssobral/bgslibrary
"""

from glob import glob
from setuptools import setup, Extension

LIBRARIES = [
    'boost_python',
    'boost_thread',
    'opencv_videostab',
    'opencv_video',
    'opencv_ts',
    'opencv_superres',
    'opencv_stitching',
    'opencv_photo',
    'opencv_ocl',
    'opencv_objdetect',
    'opencv_ml',
    'opencv_legacy',
    'opencv_imgproc',
    'opencv_highgui',
    'opencv_gpu',
    'opencv_flann',
    'opencv_features2d',
    'opencv_core',
    'opencv_contrib',
    'opencv_calib3d',
    ]

SOURCES = [
    source for sources in (
        [
            "VideoAnalysis.cpp",
            "FrameProcessor.cpp",
            "Main.cpp",
            "VideoCapture.cpp",
            "PreProcessor.cpp"
        ],
        glob("package_bgs/*.cpp"),
        glob("package_bgs/*.c"),
        glob("package_bgs/*/*.cpp"),
        glob("package_bgs/*/*/*.cpp"),
        glob("package_bgs/*/*/*.c"),
        glob("package_bgs/*/*.c"),
        glob("package_analysis/*.cpp"),
        glob("wrapper_python/*.cpp"),
        glob("wrapper_python/*/*.cpp"),
        ) for source in sources
    ]

LIBBGS = Extension(
    name='libbgs',
    libraries=LIBRARIES,
    extra_compile_args=["-std=c99", "-std=gnu++0x"],
    sources=SOURCES
    )

setup(name="bgslibrary",
      version="2.0.0",
      author="Andrews Sobral",
      description="The bgslibrary python bindings",
      license="GNU General Public License v3 (GPLv3)",
      install_requires=[
          "numpy",
      ],
      ext_modules=[LIBBGS],
     )
