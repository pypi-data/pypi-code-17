from unittest import TestCase
from uw_sws.section import get_section_by_label
from uw_pws import PWS
from uw_sws.util import fdao_sws_override
from uw_pws.util import fdao_pws_override
from uw_catalyst.util import fdao_catalyst_override
from uw_catalyst.gradebook import (
    get_participants_for_gradebook, get_participants_for_section)
from uw_catalyst.exceptions import InvalidGradebookID


@fdao_sws_override
@fdao_pws_override
@fdao_catalyst_override
class CatalystTestGradebook(TestCase):
    def test_invalid_gradebook_id(self):
        self.assertRaises(
            InvalidGradebookID, get_participants_for_gradebook, None)
        self.assertRaises(
            InvalidGradebookID, get_participants_for_gradebook, '')
        self.assertRaises(
            InvalidGradebookID, get_participants_for_gradebook, 'abc')
        self.assertRaises(
            InvalidGradebookID, get_participants_for_gradebook, 00000)
        self.assertRaises(
            InvalidGradebookID, get_participants_for_gradebook, 11111111111)

    def test_participants_for_gradebook(self):
        person = PWS().get_person_by_netid('bill')

        participants = get_participants_for_gradebook(12345, person)

        self.assertEquals(len(participants), 3, "Correct participant count")

    def test_participants_for_section(self):
        section = get_section_by_label('2013,summer,CSS,161/A')
        instructor = section.meetings[0].instructors[0]

        participants = get_participants_for_section(section, instructor)

        self.assertEquals(len(participants), 3, "Correct participant count")
