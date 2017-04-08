# -*- coding: utf-8 -*-
from __future__ import absolute_import
"""
Package Description
"""
import os
import sys
import logging
import json
from functools import wraps

from .base import NimbusPipeline

from .image import NimbusImagesPipeline
from .image import NimbusExtendImagesPipeline

from .file import NimbusFilesPipeline

from .media import NimbusMediaPipeline

from .qiniu import NimbusQiniuPipeline


