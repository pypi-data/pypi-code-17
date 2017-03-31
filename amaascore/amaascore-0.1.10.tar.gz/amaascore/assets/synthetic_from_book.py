from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import date

from amaascore.assets.asset import Asset


class SyntheticFromBook(Asset):
    """ A synthetic asset whose value is based on the value of the assets in a referenced book """

    def __init__(self, asset_id, asset_manager_id, book_id=None, asset_issuer_id=None, asset_status='Active',
                 country_id=None, currency=None, description='', fungible=True, issue_date=date.min,
                 maturity_date=date.max, links=None, references=None, *args, **kwargs):
        if not hasattr(self, 'asset_class'):  # A more specific child class may have already set this
            self.asset_class = 'Synthetic'
        self.book_id = book_id
        super(SyntheticFromBook, self).__init__(asset_manager_id=asset_manager_id, asset_id=asset_id,
                                                fungible=fungible, asset_issuer_id=asset_issuer_id,
                                                asset_status=asset_status, currency=currency,
                                                issue_date=issue_date, maturity_date=maturity_date,
                                                country_id=country_id, description=description,
                                                links=links, references=references, *args, **kwargs)
