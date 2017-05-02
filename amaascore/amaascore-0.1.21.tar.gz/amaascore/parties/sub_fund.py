from __future__ import absolute_import, division, print_function, unicode_literals

from amaascore.parties.party import Party


class SubFund(Party):

    def __init__(self, asset_manager_id, party_id, description='', base_currency=None, party_status='Active',
                 addresses=None, comments=None, emails=None, links=None, references=None,
                 *args, **kwargs):
        super(SubFund, self).__init__(asset_manager_id=asset_manager_id, party_id=party_id,
                                      base_currency=base_currency, description=description,
                                      party_status=party_status, addresses=addresses, comments=comments,
                                      emails=emails, links=links, references=references, *args, **kwargs)
