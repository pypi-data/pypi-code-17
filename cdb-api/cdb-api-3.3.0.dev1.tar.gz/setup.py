#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

from setuptools import setup
import os

projectRootPath = os.environ['CDB_ROOT_DIR']
projectVersionPath = 'etc/version'
fullVersionPath = '%s/%s' % (projectRootPath, projectVersionPath)

versionFile = open(fullVersionPath)
version = versionFile.read()

setup(name='cdb-api',
      version='3.3.0.dev1',
      license='Copyright (c) UChicago Argonne, LLC. All rights reserved.',
      packages=['cdb.cdb_web_service.api',
                'cdb.common.utility',
                'cdb.common.exceptions',
                'cdb.common.objects'],
      description='Python APIs used to communicate with Component Database',
      maintainer='Dariusz Jarosz',
      maintainer_email='djarosz@aps.anl.gov',
      url='https://github.com/AdvancedPhotonSource/ComponentDB'
      )
