#!/usr/bin/env python3
# this script gets executed at startup of interactive Python session

from gtcms.core import *
from gtcms.core.db import db, engine
engine.echo = True

from gtcms.models import *
