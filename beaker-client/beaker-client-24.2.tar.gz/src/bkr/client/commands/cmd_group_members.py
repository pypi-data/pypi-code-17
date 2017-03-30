
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

"""
bkr group-members: List members of a group
==========================================

.. program:: bkr group-members

Synopsis
--------

| :program:`bkr group-members` [*options*] <group-name>

Description
-----------

List the members of an existing group.

Options
-------

.. option:: --format list, --format json

   Display results in the given format. ``list`` lists one user per
   line and is useful to be fed as input to other command line
   utilities. The default format is ``json``, which returns the users
   as a JSON array.

Common :program:`bkr` options are described in the :ref:`Options
<common-options>` section of :manpage:`bkr(1)`.

Exit status
-----------

Non-zero on error, otherwise zero.

:manpage:`bkr(1)`

"""

from bkr.client import BeakerCommand
import bkr.client.json_compat as json

class Group_Members(BeakerCommand):
    """List group members"""
    enabled = True
    requires_login = False

    def options(self):
        self.parser.usage = "%%prog %s <group-name>" % self.normalized_name
        self.parser.add_option(
            '--format',
            type='choice',
            choices=['list', 'json'],
            default='json',
            help='Results display format: list, json [default: %default]',
        )

    def run(self, *args, **kwargs):

        if len(args) != 1:
            self.parser.error('Exactly one group name must be specified.')

        format = kwargs['format']
        group = args[0]

        self.set_hub(**kwargs)
        members = self.hub.groups.members(group)

        if format == 'list':
            for m in members:
                if m['owner']:
                    output_tuple = (m['username'],m['email'], 'Owner')
                else:
                    output_tuple = (m['username'],m['email'], 'Member')

                print '%s %s %s' % output_tuple

        if format == 'json':
            print json.dumps(members)
