# copyright 2016-2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""Miscellaneous test utilities."""


def create_archive_unit(parent, **kwargs):
    """Create an archive unit and its mandatory children, return a 3-uple

         (archive unit, alternative, sequence)
    """
    cnx = kwargs.pop('cnx', getattr(parent, '_cw', None))
    kwargs.setdefault('user_annotation', u'archive unit title')
    au = cnx.create_entity('SEDAArchiveUnit', seda_archive_unit=parent, **kwargs)
    alt = cnx.create_entity('SEDAAltArchiveUnitArchiveUnitRefId',
                            reverse_seda_alt_archive_unit_archive_unit_ref_id=au)
    last = cnx.create_entity(
        'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement',
        reverse_seda_seq_alt_archive_unit_archive_unit_ref_id_management=alt)
    cnx.create_entity('SEDATitle', seda_title=last)

    return au, alt, last


def create_authority_record(cnx, name, kind=u'person', **kwargs):
    """Return an AuthorityRecord with specified kind and name."""
    kind_eid = cnx.find('AgentKind', name=kind)[0][0]
    record = cnx.create_entity('AuthorityRecord', agent_kind=kind_eid, **kwargs)
    cnx.create_entity('NameEntry', parts=name, form_variant=u'authorized',
                      name_entry_for=record)
    return record
