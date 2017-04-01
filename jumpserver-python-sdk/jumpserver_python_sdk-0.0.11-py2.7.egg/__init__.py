#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import sys

__version__ = '0.0.11'

from .config import API_URL_MAPPING
from .authentication import Auth
from .service import Request, AppService, UserService
