# This file is part of caucase
# Copyright (C) 2017  Nexedi
#     Alain Takoudjou <alain.takoudjou@nexedi.com>
#     Vincent Pelletier <vincent@nexedi.com>
#
# caucase is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# caucase is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with caucase.  If not, see <http://www.gnu.org/licenses/>.
import os
import argparse
from caucase.web import app, db

def parseArguments():
  """
  Parse arguments for Certificate Authority cli instance.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--db-file', required=True,
                      help='Certificate authority data base file path')
  return parser

def housekeeping(config):
  """
    Start Storage housekeep method to cleanup garbages
  """
  app.config.update(
    DEBUG=False,
    CSRF_ENABLED=True,
    TESTING=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///%s' % config.db_file
  )
  from caucase.storage import Storage
  storage = Storage(db)
  storage.housekeep()

def main():
  parser = parseArguments()
  config = parser.parse_args()
  
  housekeeping(config)