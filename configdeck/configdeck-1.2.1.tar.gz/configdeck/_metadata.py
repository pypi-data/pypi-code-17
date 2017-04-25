# -*- coding: utf-8; -*-
# configdeck/_metadata.py
# Part of Configdeck, a Python library for stacking configuration.
#
# Copyright © 2008–2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Package metadata for the ‘configdeck’ distribution. """

import os.path


distribution_name = "configdeck"

version_file_name = "VERSION"
version_file_path = os.path.join(
        os.path.dirname(__file__),
        version_file_name)


class DistributionVersionUnknown(ValueError):
    """ Exception raised when the version of this distribution is unknown. """


def get_version_text(datafile_path=version_file_path):
    """ Get the version string from the version data file.

        :param datafile_path: Filesystem path of the version data
            file.
        :return: The version string, as text.
        """
    try:
        with open(datafile_path) as infile:
            text = infile.read().strip()
    except (OSError, IOError) as exc:
        raise DistributionVersionUnknown(
                "could not read file {path!r}"
                " ({exc})"
                "".format(path=datafile_path, exc=exc)
                )

    return text


# Copyright © 2008–2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.GPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
