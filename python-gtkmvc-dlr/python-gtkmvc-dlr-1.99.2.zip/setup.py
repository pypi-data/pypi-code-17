#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author: Ionutz Borcoman <borco@go.ro>
#
# ----------------------------------------------------------------------

try:
    from setuptools import setup

except:
    from distutils.core import setup
    pass

from gtkmvc import get_version


setup(name="python-gtkmvc-dlr",
      version=".".join(map(str, get_version())), 
      description="Model-View-Controller and Observer patterns for developing pygtk-based applications -- mainly written by Roberto Cavada"
                  "and for minor changes forked by the Institute of Robotics and Mechatronics of the German Aerospace Center (DLR-RM). "
                  "In order to release a full installation chain for other tools DLR-RM put it on pypi even so "
                  "the previous versions were only hosted on sourceforge.net.",
      author="Roberto Cavada and Rico Belder (DLR-RM)",
      maintainer='Rico Belder',
      author_email="roboogle@gmail.com, rico.belder@dlr.de",
      maintainer_email='rico.belder@dlr.de',
      license="LGPL",
      url='https://github.com/DLR-RM/gtkmvc3/tree/gtkmvc_dlr',
      download_url='https://github.com/DLR-RM/gtkmvc3/releases/download/gtkmvc_dlr_1.99.2/python-gtkmvc-dlr-1.99.2.tar.gz',
      packages=['gtkmvc', 'gtkmvc.support', 'gtkmvc.adapters', 'gtkmvc.progen'],
      package_data={'gtkmvc.progen': ['progen.glade']},
      scripts=['scripts/gtkmvc-progen'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: GTK Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          ],
      
     )
