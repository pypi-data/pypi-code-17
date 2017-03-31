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
"""cubicweb-seda application package

Data Exchange Standard for Archival
"""
from functools import partial

from cubicweb_compound import skip_rtypes_set, CompositeGraph

# data structure allowing control of the compound graph:
#
# SEDAArchiveTransferGraph.keywords['skipetypes'].append('SomeEtype')
# SEDAArchiveTransferGraph.keywords['skiprtypes'].append('some_rtype')
SEDAArchiveTransferGraph = partial(CompositeGraph, skipetypes=[], skiprtypes=[])


def seda_profile_container_def(schema):
    """Define container for SEDAArchiveTransfer, as a list of (etype, parent_rdefs)."""
    graph = SEDAArchiveTransferGraph(schema)
    return [(child, set(relinfo))
            for child, relinfo in graph.parent_structure('SEDAArchiveTransfer').items()]


def iter_external_rdefs(eschema, skip_rtypes=skip_rtypes_set(['container'])):
    """Return an iterator on (rdef, role) of external relations from entity schema (i.e.
    non-composite relations).
    """
    for rschema, targets, role in eschema.relation_definitions():
        if rschema in skip_rtypes:
            continue
        for target_etype in targets:
            rdef = eschema.rdef(rschema, role, target_etype)
            if rdef.composite:
                continue
            yield rdef, role


def iter_all_rdefs(schema, container_etype):
    """Return an iterator on (rdef, role) of all relations of the compound graph starting from the
    given entity type, both internal (composite) and external (non-composite).
    """
    graph = SEDAArchiveTransferGraph(schema)
    stack = [container_etype]
    visited = set(stack)
    while stack:
        etype = stack.pop()
        for (rtype, role), targets in graph.child_relations(etype):
            rschema = schema.rschema(rtype)
            for target in targets:
                if role == 'subject':
                    rdef = rschema.rdefs[(etype, target)]
                else:
                    rdef = rschema.rdefs[(target, etype)]
                yield rdef, role

                if target not in visited:
                    visited.add(target)
                    stack.append(target)
        for rdef, role in iter_external_rdefs(schema[etype]):
            yield rdef, role
