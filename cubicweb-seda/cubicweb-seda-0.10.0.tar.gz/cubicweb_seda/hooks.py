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
"""cubicweb-seda hooks"""

from collections import defaultdict
import itertools

from yams import ValidationError
from yams.schema import role_name

from cubicweb import _
from cubicweb.predicates import is_instance, score_entity
from cubicweb.server import hook

from .entities import rule_type_from_etype, diag
from .entities.generated import CHOICE_RTYPE


SEDA_PARENT_RTYPES = {}
CHOICE_RTYPE_ROLE = dict(itertools.chain(*CHOICE_RTYPE.values()))
CHOICE_RTYPES = set(CHOICE_RTYPE_ROLE)


class SetContainerOp(hook.DataOperationMixIn, hook.Operation):
    def precommit_event(self):
        cnx = self.cnx
        # build a mapping <eid>: <container eid>
        containers = {}
        data = dict(self.get_data())  # data is a 2-uple (eid, parent eid)
        for eid in data:
            # search for the container from the parent
            peid = data[eid]
            # climb up to the uppermost parent
            while peid in data:
                peid = data[peid]
            entity = cnx.entity_from_eid(peid)
            # we may run into caching issue if this operation is triggered several times in a
            # transaction
            entity.cw_clear_all_caches()
            adapter = entity.cw_adapt_to('IContained')
            if adapter is None:  # we reached the container
                containers[eid] = peid
            else:  # the adapter must know the container at this point
                if adapter.container is not None:
                    containers[eid] = adapter.container.eid
                else:
                    assert entity.cw_adapt_to('IContainer'), \
                        "can't retrieve container for entity %s" % entity
                    containers[eid] = peid
        # turn previous mapping into <container eid>: [<list of contained eids>]
        contained = defaultdict(list)
        for eid, ceid in containers.items():
            contained[ceid].append(eid)
        # and uses it to insert data using raw SQL for performance
        cursor = cnx.cnxset.cu
        for ceid, eids in contained.items():
            args = [{'x': eid} for eid in eids]
            cursor.executemany('INSERT INTO container_relation(eid_from, eid_to)'
                               ' SELECT %%(x)s, %(c)s'
                               ' WHERE NOT EXISTS(SELECT 1 FROM container_relation'
                               ' WHERE eid_from=%%(x)s AND eid_to=%(c)s)' % {'c': ceid}, args)


class SetContainerHook(hook.Hook):
    __regid__ = 'seda.graph.updated'
    __select__ = hook.Hook.__select__ & hook.match_rtype_sets(SEDA_PARENT_RTYPES)
    events = ('before_add_relation',)
    category = 'metadata'

    def __call__(self):
        if SEDA_PARENT_RTYPES[self.rtype] == 'subject':
            SetContainerOp.get_instance(self._cw).add_data((self.eidfrom, self.eidto))
        else:
            SetContainerOp.get_instance(self._cw).add_data((self.eidto, self.eidfrom))


class CheckRefNonRuleIdCodeListHook(hook.Hook):
    """Watch for addition of concept through seda_ref_non_rule_id_to relation, to ensure it belongs
    to the scheme specified on the transfer

    This depends on the parent entity type and can not properly be handled with a rql constraint,
    since it would require several disjoint constraints, while cw's semantic is that all constraints
    should be matched.
    """
    __regid__ = 'seda.schema.ref_non_rule_id'
    __select__ = hook.Hook.__select__ & hook.match_rtype('seda_ref_non_rule_id_to')
    events = ('after_add_relation',)

    def __call__(self):
        CheckRefNonRuleIdCodeListOp(self._cw, parent=self.eidfrom, concept=self.eidto)


# Late operation to be called once `container` relation is set
class CheckRefNonRuleIdCodeListOp(hook.LateOperation):

    def precommit_event(self):
        parent = self.cnx.entity_from_eid(self.parent, etype='SEDARefNonRuleId')
        # generate constraint on the concept's scheme depending on the parent's parent type
        parent_parent = parent.cw_adapt_to('IContained').parent
        rule_type = rule_type_from_etype(parent_parent.cw_etype)
        rql = ('Any C WHERE C eid %(c)s, C in_scheme CS, X eid %(x)s, X container AT, '
               'CACLV seda_{0}_rule_code_list_version_from AT, '
               'CACLV seda_{0}_rule_code_list_version_to CS'.format(rule_type))
        if not self.cnx.execute(rql, {'c': self.concept, 'x': parent_parent.eid}):
            msg = _("this concept doesn't belong to scheme specified on the profile")
            raise ValidationError(parent.eid,
                                  {role_name('seda_ref_non_rule_id_to', 'subject'): msg})


class EnsureChoiceNotEmptyOp(hook.DataOperationMixIn, hook.Operation):
    """Make sure that, when a choice element is created/updated, it is not empty."""

    def precommit_event(self):
        for entity in self.get_data():
            if self.cnx.deleted_in_transaction(entity.eid):
                continue
            rtype_roles = CHOICE_RTYPE[entity.cw_etype]
            for rtype, role in rtype_roles:
                if entity.related(rtype, role=role):
                    break
            else:
                msg = _('An alternative cannot be empty')
                raise ValidationError(entity.eid, {'': msg})


class EnsureChoiceNotEmptyAtCreationHook(hook.Hook):
    """Make sure that, when a choice element is created, it is not empty."""

    __regid__ = 'seda.choice.creation.ensure-not-empty'
    __select__ = hook.Hook.__select__ & score_entity(lambda x: x.cw_etype.startswith('SEDAAlt'))
    events = ('before_add_entity',)

    def __call__(self):
        EnsureChoiceNotEmptyOp.get_instance(self._cw).add_data(self.entity)


class EnsureChoiceNotEmptyAtRTypeDeletionHook(hook.Hook):
    """Make sure that, when a relation with a choice element is deleted, the choice remains not
    empty."""

    __regid__ = 'seda.choice.relation-deletion.ensure-not-empty'
    __select__ = hook.Hook.__select__ & hook.match_rtype_sets(CHOICE_RTYPES)
    events = ('before_delete_relation',)

    def __call__(self):
        eid = {'object': self.eidto, 'subject': self.eidfrom}[CHOICE_RTYPE_ROLE[self.rtype]]
        choice = self._cw.entity_from_eid(eid)
        if choice.cw_etype in CHOICE_RTYPE:
            # Else this is an ambiguous relation, which in this case isn't
            # targetting a choice.
            EnsureChoiceNotEmptyOp.get_instance(self._cw).add_data(choice)


class SetDefaultCodeListVersionsHook(hook.Hook):
    """Hook triggering an operation to set sensible default values for a transfer's code list
    versions.
    """
    __regid__ = 'seda.transfer.default-code-lists'
    __select__ = hook.Hook.__select__ & is_instance('SEDAArchiveTransfer')
    events = ('after_add_entity',)

    def __call__(self):
        SetDefaultCodeListVersionsOp(self._cw, transfer_eid=self.entity.eid)


class SetDefaultCodeListVersionsOp(hook.Operation):
    """Set sensible default values for a transfer's code list versions."""
    # XXX factorize with data structure in dataimport
    complex_rtypes = [
        ('seda_file_format_code_list_version', 'seda_format_id_to', None),
        ('seda_message_digest_algorithm_code_list_version', 'seda_algorithm',
         'SEDABinaryDataObject'),
        ('seda_mime_type_code_list_version', 'seda_mime_type_to', None),
        ('seda_encoding_code_list_version', 'seda_encoding_to', None),
        ('seda_data_object_version_code_list_version', 'seda_data_object_version_to', None),
        ('seda_relationship_code_list_version', 'seda_type_relationship', None),
        ('seda_access_rule_code_list_version', 'seda_rule', 'SEDASeqAccessRuleRule'),
        ('seda_appraisal_rule_code_list_version', 'seda_rule', 'SEDASeqAppraisalRuleRule'),
        ('seda_dissemination_rule_code_list_version', 'seda_rule', 'SEDASeqDisseminationRuleRule'),
        # 'seda_compression_algorithm_code_list_version',
        # 'seda_classification_rule_code_list_version',
        # 'seda_reuse_rule_code_list_version',
        # 'seda_storage_rule_code_list_version',
        # 'seda_acquisition_information_code_list_version',
    ]

    def precommit_event(self):
        transfer = self.transfer_eid
        cnx = self.cnx
        for rtype, ref_rtype, ref_etype in self.complex_rtypes:
            etype = 'SEDA' + ''.join(word.capitalize() for word in rtype.split('_')[1:])
            rql = ('INSERT {etype} X: X {rtype}_from T, X {rtype}_to CS '
                   'WHERE NOT Y {rtype}_from T, T eid %(t)s, '
                   'CS scheme_relation_type RT, RT name %(rt)s')
            if ref_etype is not None:
                rql += ', CS scheme_entity_type ET, ET name %(et)s'
            cnx.execute(rql.format(etype=etype, rtype=rtype),
                        {'t': transfer, 'rt': ref_rtype, 'et': ref_etype})


class SetDefaultDataObjectRefCardinalityHook(hook.Hook):
    """Hook triggering an operation to set cardinality to 1 on creation of a data object 'typed'
    reference.
    """
    __regid__ = 'seda.doref.default'
    __select__ = hook.Hook.__select__ & is_instance('SEDADataObjectReference')
    events = ('after_add_entity',)

    def __call__(self):
        SetDefaultDataObjectRefCardinalityOp(self._cw, do_ref_eid=self.entity.eid)


class SetDefaultDataObjectRefCardinalityOp(hook.Operation):
    """Set cardinality to 1 on creation of a data object 'typed' reference."""

    def precommit_event(self):
        do_ref = self.cnx.entity_from_eid(self.do_ref_eid)
        parent = do_ref.seda_data_object_reference[0]
        if parent.cw_etype != 'SEDASeqAltArchiveUnitArchiveUnitRefIdManagement':
            do_ref.cw_set(user_cardinality=u'1')


class SimplifiedProfileSyncDORefCardOnCreateHook(hook.Hook):
    """Hook triggering an operation to keep in sync user_cardinality of data object reference and
    its associated data object for simplified profiles, on creation of the relation between them.
    """
    __regid__ = 'seda.doref.default'
    __select__ = hook.Hook.__select__ & hook.match_rtype('seda_data_object_reference_id')
    events = ('after_add_relation',)

    def __call__(self):
        ref = self._cw.entity_from_eid(self.eidfrom)
        bdo = self._cw.entity_from_eid(self.eidto)
        if ref.cw_etype == 'SEDADataObjectReference' and bdo.cw_etype == 'SEDABinaryDataObject':
            SimplifiedProfileSyncDORefCardOp(self._cw, do_ref=ref, do=bdo)


class SimplifiedProfileSyncDORefCardOnUpdateHook(hook.Hook):
    """Hook triggering an operation to keep in sync user_cardinality of data object reference and
    its associated data object for simplified profiles, on update of the data object's cardinality.
    """
    __regid__ = 'seda.doref.default'
    __select__ = hook.Hook.__select__ & is_instance('SEDABinaryDataObject')
    events = ('after_update_entity',)

    def __call__(self):
        if 'user_cardinality' in self.entity.cw_edited:
            references = self.entity.reverse_seda_data_object_reference_id
            if len(references) == 1:  # else it can't be a simplified profile
                SimplifiedProfileSyncDORefCardOp(self._cw, do_ref=references[0], do=self.entity)


class SimplifiedProfileSyncDORefCardOp(hook.Operation):
    """Keep in sync user_cardinality of data object reference and its associated data object for
    simplified profiles.
    """

    def precommit_event(self):
        container = self.do.seda_binary_data_object[0] if self.do.seda_binary_data_object else None
        if container and container.simplified_profile:
            self.do_ref.cw_set(user_cardinality=self.do.user_cardinality)


class CheckProfileSEDACompatiblityOp(hook.DataOperationMixIn, hook.LateOperation):
    """Data operation that will check compatibility of a SEDA profile upon modification.

    This is a late operation since it has to be executed once the 'container' relation is set.
    """

    def precommit_event(self):
        cnx = self.cnx
        profiles = set()
        for eid in self.get_data():
            if cnx.deleted_in_transaction(eid):
                continue
            entity = cnx.entity_from_eid(eid)
            if entity.cw_etype == 'SEDAArchiveTransfer':
                profiles.add(entity)
            else:
                container = entity.cw_adapt_to('IContained').container
                if container is not None and container.cw_etype == 'SEDAArchiveTransfer':
                    profiles.add(container)
        with cnx.deny_all_hooks_but():
            for profile in profiles:
                adapter = profile.cw_adapt_to('ISEDACompatAnalyzer')
                supported_formats = adapter.diagnose()
                profile.cw_set(compat_list=u', '.join(sorted(supported_formats)))
                if profile.simplified_profile and 'simplified' not in supported_formats:
                    raise ValidationError(
                        profile.eid, {'': _("This profile can't be turned to simplified. "
                                            "See the diagnostic tab for more information")})

    def add_entity(self, entity):
        """Add entity, its parent entities (up to the container root) for update of their
        modification date at commit time.
        """
        self.add_data(entity.eid)
        while True:
            safety_belt = set((entity.eid,))
            contained = entity.cw_adapt_to('IContained')
            if contained is None:
                assert entity.cw_adapt_to('IContainer')
                break
            else:
                entity = contained.container
                if entity is None or entity.eid in safety_belt:
                    break
                self.add_data(entity.eid)
                safety_belt.add(entity.eid)


class CheckNewProfile(hook.Hook):
    """Instantiate operation checking for profile seda compat on its creation"""
    __regid__ = 'seda.transfer.created.checkcompat'
    __select__ = hook.Hook.__select__ & is_instance('SEDAArchiveTransfer')
    events = ('after_add_entity', )
    category = 'metadata'

    def __call__(self):
        CheckProfileSEDACompatiblityOp.get_instance(self._cw).add_entity(self.entity)


WATCH_RTYPES_SET = set().union(*((rtype for rtype in rule.watch
                                  # filter out (entity type, attribute)
                                  if not isinstance(rtype, tuple))
                                 for rule in diag.RULES.values()))


class AddOrRemoveChildrenHook(hook.Hook):
    """Some relation involved in diagnosis of the profile is added or removed."""
    __regid__ = 'seda.transfer.relupdated.checkcompat'
    __select__ = hook.Hook.__select__ & hook.match_rtype_sets(WATCH_RTYPES_SET)
    events = ('before_add_relation', 'before_delete_relation')
    category = 'metadata'

    def __call__(self):
        op = CheckProfileSEDACompatiblityOp.get_instance(self._cw)
        op.add_entity(self._cw.entity_from_eid(self.eidfrom))
        op.add_entity(self._cw.entity_from_eid(self.eidto))


WATCH_ETYPES = defaultdict(set)
for rule in diag.RULES.values():
    for etype_attr in rule.watch:
        if isinstance(etype_attr, tuple):
            WATCH_ETYPES[etype_attr[0]].add(etype_attr[1])

WATCH_ETYPES['SEDAArchiveTransfer'].add('simplified_profile')


class UpdateWatchedProfileElementHook(hook.Hook):
    """Some entity involved in diagnosis of the profile is created or updated."""
    __regid__ = 'seda.transfer.updated.checkcompat'
    __select__ = hook.Hook.__select__ & is_instance(*WATCH_ETYPES)
    events = ('before_add_entity', 'before_update_entity')
    category = 'metadata'

    def __call__(self):
        if WATCH_ETYPES[self.entity.cw_etype] & set(self.entity.cw_edited):
            CheckProfileSEDACompatiblityOp.get_instance(self._cw).add_entity(self.entity)


def registration_callback(vreg):
    from cubicweb.server import ON_COMMIT_ADD_RELATIONS
    from cubicweb_seda import seda_profile_container_def, iter_all_rdefs

    vreg.register_all(globals().values(), __name__)

    for etype, parent_rdefs in seda_profile_container_def(vreg.schema):
        for rtype, role in parent_rdefs:
            if SEDA_PARENT_RTYPES.setdefault(rtype, role) != role:
                raise Exception('inconsistent relation', rtype, role)
    for rdef, role in iter_all_rdefs(vreg.schema, 'SEDAArchiveTransfer'):
        ON_COMMIT_ADD_RELATIONS.add(str(rdef.rtype))
