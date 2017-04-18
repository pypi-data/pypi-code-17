# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""Functional security tests."""

from cubicweb.devtools.testlib import CubicWebTC

import testutils


class NonManagerUserTC(CubicWebTC):
    """Tests checking that a user in "users" group only can do things.

    Most of the times, we do not call any assertion method and only rely on no
    error being raised.
    """
    assertUnauthorized = testutils.assertUnauthorized

    login = u'bob'

    def setup_database(self):
        with self.admin_access.cnx() as cnx:
            self.create_user(cnx, self.login, ('users', ))
            authority = testutils.authority_with_naa(cnx)
            cnx.execute('SET U authority O WHERE U login %(login)s, O eid %(o)s',
                        {'login': self.login, 'o': authority.eid})
            cnx.commit()

        self.authority_eid = authority.eid

    def test_create_update_authorityrecord(self):
        with self.new_access(self.login).cnx() as cnx:
            arecord = testutils.authority_record(cnx, name=u'a')
            cnx.commit()
            arecord.cw_set(record_id=u'123')
            cnx.commit()

            # can change kind (unless used in constrained relation, but this is tested in
            # unittest_schema)
            arecord.cw_set(agent_kind=cnx.find('AgentKind', name=u'authority').one())
            cnx.commit()

    def test_create_update_sedaprofile(self):
        with self.new_access(self.login).cnx() as cnx:
            profile = testutils.setup_profile(cnx)
            cnx.commit()
            profile.cw_set(user_annotation=u'meh')
            cnx.commit()
            profile.cw_adapt_to('IWorkflowable').fire_transition('publish')
            cnx.commit()
            testutils.setup_profile(cnx, title=u'Clone', new_version_of=profile)
            cnx.commit()

    def test_create_update_vocabulary(self):
        with self.admin_access.cnx() as cnx:
            admin_scheme = testutils.scheme_for_type(cnx, u'seda_keyword_type_to', None,
                                                     u'type1')
            cnx.commit()
            type_concept = admin_scheme.reverse_in_scheme[0]

        with self.new_access(self.login).cnx() as cnx:
            scheme = testutils.setup_scheme(cnx, u'my scheme',
                                            u'lab1', u'lab2', code_keyword_type=type_concept)
            cnx.commit()
            scheme.add_concept(u'lab3')
            cnx.commit()
            scheme.cw_set(code_keyword_type=None)
            cnx.commit()

            admin_scheme = cnx.entity_from_eid(admin_scheme.eid)
            admin_scheme.cw_set(title=u'code keyword types')
            cnx.commit()
            admin_scheme.add_concept(u'type2')
            cnx.commit()
            admin_scheme.cw_set(code_keyword_type=type_concept)
            cnx.commit()

    def test_create_update_agent_in_own_organization(self):
        with self.admin_access.cnx() as cnx:
            other_authority = testutils.authority_with_naa(cnx, name=u'other authority')
            other_agent = testutils.agent(cnx, u'bob', authority=other_authority)
            cnx.commit()
            other_authority_eid = other_authority.eid
            other_agent_eid = other_agent.eid

        with self.new_access(self.login).cnx() as cnx:
            agent = testutils.agent(cnx, u'bob', authority=self.authority_eid)
            cnx.commit()
            agent.cw_set(name=u'bobby')
            cnx.commit()
            agent.cw_delete()
            cnx.commit()
            arecord = testutils.authority_record(cnx, name=u'bobby', kind=u'person')
            agent.cw_set(authority_record=arecord)
            cnx.commit()

            with self.assertUnauthorized(cnx):
                testutils.agent(cnx, u'other bob', authority=other_authority_eid)

            other_agent = cnx.entity_from_eid(other_agent_eid)
            with self.assertUnauthorized(cnx):
                other_agent.cw_set(name=u'bobby')
            with self.assertUnauthorized(cnx):
                other_agent.cw_delete()
            with self.assertUnauthorized(cnx):
                other_arecord = testutils.authority_record(cnx, name=u'other bob', kind=u'person')
                other_agent.cw_set(authority_record=other_arecord)

    def test_create_update_organizationunit_in_own_organization(self):
        with self.admin_access.cnx() as cnx:
            other_authority = testutils.authority_with_naa(cnx, name=u'other authority')
            other_unit = testutils.organization_unit(
                cnx, u'arch', archival_roles=[u'archival'], authority=other_authority)
            cnx.commit()
            other_authority_eid = other_authority.eid
            other_unit_eid = other_unit.eid

        with self.new_access(self.login).cnx() as cnx:
            unit = testutils.organization_unit(
                cnx, u'arch', archival_roles=[u'archival'], authority=self.authority_eid)
            cnx.commit()
            unit.cw_set(name=u'archi')
            cnx.commit()
            unit.cw_delete()
            cnx.commit()
            arecord = testutils.authority_record(cnx, name=u'arch', kind=u'authority')
            unit.cw_set(authority_record=arecord)
            cnx.commit()

            with self.assertUnauthorized(cnx):
                testutils.organization_unit(
                    cnx, u'other arch', archival_roles=[u'archival'], authority=other_authority_eid)

            other_unit = cnx.entity_from_eid(other_unit_eid)
            with self.assertUnauthorized(cnx):
                other_unit.cw_set(name=u'archi')
            with self.assertUnauthorized(cnx):
                other_unit.cw_delete()
            with self.assertUnauthorized(cnx):
                other_arecord = testutils.authority_record(cnx, name=u'other arch',
                                                           kind=u'authority')
                other_unit.cw_set(authority_record=other_arecord)

    def test_cannot_modify_activities(self):
        with self.new_access(self.login).cnx() as cnx:
            arecord = testutils.authority_record(cnx, name=u'a')
            cnx.commit()

            activity = arecord.reverse_used[0]

            with self.assertUnauthorized(cnx):
                activity.cw_set(description=u'hacked')

            with self.assertUnauthorized(cnx):
                activity.cw_set(associated_with=cnx.find('CWUser', login='admin').one())

            with self.assertUnauthorized(cnx):
                activity.cw_set(generated=None)

            with self.assertUnauthorized(cnx):
                activity.cw_delete()

    def test_cannot_create_activities(self):
        with self.new_access(self.login).cnx() as cnx:
            scheme = testutils.setup_scheme(cnx, u'my scheme')
            concept = scheme.add_concept(u'lab3')
            profile = testutils.setup_profile(cnx)
            cnx.commit()

            for entity in (scheme, concept, profile):
                with self.assertUnauthorized(cnx):
                    cnx.create_entity('Activity', generated=entity)
                with self.assertUnauthorized(cnx):
                    cnx.create_entity('Activity', used=entity)

            with self.assertUnauthorized(cnx):
                cnx.create_entity('Activity', associated_with=cnx.user)

    def test_cannot_create_update_organization(self):
        with self.new_access(self.login).cnx() as cnx:
            with self.assertUnauthorized(cnx):
                testutils.authority_with_naa(cnx, u'new')

            org = testutils.authority_with_naa(cnx)
            with self.assertUnauthorized(cnx):
                org.cw_set(name=u'uh')
            with self.assertUnauthorized(cnx):
                arecord = testutils.authority_record(cnx, name=u'a', kind=u'authority')
                org.cw_set(authority_record=arecord)

    def test_cannot_create_update_naa(self):
        with self.new_access(self.login).cnx() as cnx:
            with self.assertUnauthorized(cnx):
                cnx.create_entity('ArkNameAssigningAuthority',
                                  who=u'123', what=u'443')

            test_naa = testutils.naa(cnx)
            with self.assertUnauthorized(cnx):
                test_naa.cw_set(who=u'1')

    def test_can_create_authorityrecord_activities(self):
        with self.new_access(self.login).cnx() as cnx:
            arecord = testutils.authority_record(cnx, name=u'a')
            cnx.commit()
            # EAC import expect user may create activity
            cnx.create_entity('Activity', generated=arecord)
            cnx.commit()


class ManagerUserTC(CubicWebTC):
    """Tests checking that a user in "managers" group only can do things.

    Most of the times, we do not call any assertion method and only rely on no
    error being raised.
    """

    def test_create_update_organization(self):
        with self.admin_access.cnx() as cnx:
            org = testutils.authority_with_naa(cnx)
            cnx.commit()
            org.cw_set(name=u'uh')
            cnx.commit()
            arecord = testutils.authority_record(cnx, name=u'a', kind=u'authority')
            org.cw_set(authority_record=arecord)
            cnx.commit()

    def test_create_update_naa(self):
        with self.admin_access.cnx() as cnx:
            test_naa = testutils.naa(cnx)
            cnx.commit()
            test_naa.cw_set(who=u'1')
            cnx.commit()
            naa = cnx.create_entity('ArkNameAssigningAuthority',
                                    who=u'123', what=u'443')
            cnx.commit()
            naa.cw_set(what=u'987')
            cnx.commit()


if __name__ == '__main__':
    import unittest
    unittest.main()
