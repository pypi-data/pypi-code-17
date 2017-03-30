#!/usr/bin/env python

# Copyright 2016 DIANA-HEP
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

__version__ = "1.0.8"

version = __version__

version_info = tuple(re.split(r"[-\.]", __version__))

specification = ".".join(version_info[:2])

def compatible(serializedVersion):
    selfMajor, selfMinor = map(int, version_info[:2])
    otherMajor, otherMinor = map(int, re.split(r"[-\.]", serializedVersion)[:2])
    if selfMajor >= otherMajor:
        return True
    elif selfMinor >= otherMinor:
        return True
    else:
        return False
