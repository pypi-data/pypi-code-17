import datetime

from molo.yourwords.models import (
    YourWordsCompetition,
    YourWordsCompetitionEntry,
)
from molo.yourwords.tests.base import BaseYourWordsTestCase


class TestWagtailAdminActions(BaseYourWordsTestCase):

    def test_export_csv(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        comp = YourWordsCompetition(
            title='Test Competition',
            description='This is the description')
        self.competition_index.add_child(instance=comp)
        comp.save_revision().publish()

        YourWordsCompetitionEntry.objects.create(
            competition=comp,
            user=self.user,
            story_name='test',
            story_text='test body',
            terms_or_conditions_approved=True,
            hide_real_name=True
        )

        response = self.client.post('/admin/yourwords/'
                                    'yourwordscompetitionentry/')

        date = str(datetime.datetime.now().date())

        expected_output = (
            'competition,submission_date,user,story_name,story_text,'
            'terms_or_conditions_approved,hide_real_name,is_read,'
            'is_shortlisted,is_winner\r\n'
            '{0},{1},1,test,test body,1,1,0,0,0'.format(comp.pk, date)
        )
        self.assertContains(response, expected_output)
