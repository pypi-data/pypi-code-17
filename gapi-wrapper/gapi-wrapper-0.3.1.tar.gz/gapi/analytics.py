# -*- coding: utf-8 -*-
import logging
import time

import httplib2
from googleapiclient import discovery
from oauth2client.client import OAuth2Credentials, AccessTokenRefreshError
from six.moves import http_client

from .core import GoogleService, customer_callable
from .exceptions import APINoData

__all__ = ['AnalyticsService']


class AnalyticsService(GoogleService):
    RETRY_SLEEP_SECS = 1
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    log = logging.getLogger('gapi_wrapper.analytics')

    def __init__(self, account, profile_id, cache=None, refresh=False):
        super(AnalyticsService, self).__init__(refresh=refresh)
        self.account = account
        self.profile_id = profile_id
        self._cache = cache

        credentials = OAuth2Credentials(
            access_token=self.account['access_token'],
            client_id=self.account['client_id'],
            client_secret=self.account['client_secret'],
            refresh_token=self.account['refresh_token'],
            token_expiry=self.account['token_expiry'],
            token_uri=self.TOKEN_URI,
            user_agent=self.USER_AGENT,
        )
        http = credentials.authorize(httplib2.Http())
        self.analytics = discovery.build('analytics', 'v3', http=http, cache_discovery=False)

    def _get_cache_key(self, name, params):
        return [self.account, self.profile_id, name, params]

    def _query(self, params):
        params = dict(params)
        params['ids'] = 'ga:{}'.format(self.profile_id)
        items = []
        headers = None
        iteration = 1

        while True:
            service_data = getattr(self.analytics.data(), 'ga')()
            api_query = service_data.get(**params)
            retries = 0
            results = None
            while retries < 3 and results is None:
                try:
                    results = api_query.execute()  # here we can get AccessTokenRefreshError while export process :(
                except AccessTokenRefreshError as e:
                    # it seems like we got token expired :(((,
                    # or mb this is bug of oauth2client
                    # http://code.google.com/p/google-api-python-client/issues/detail?id=90
                    self.log.warning('Got AccessTokenRefreshError, e: {}'.format(e))
                    return
                except (IOError, http_client.HTTPException,) as e:
                    self.log.exception(e)
                    time.sleep(self.RETRY_SLEEP_SECS * (1 + retries))
                retries += 1

            if not results:
                raise APINoData('Error while getting data. {} attempts made.'.format(retries))

            if not headers:
                headers = [hdr['name'].replace('ga:', '') for hdr in results.get('columnHeaders')]

            fetched_items = results.get('rows', [])
            if not fetched_items:
                self.log.debug(u'STRANGE: no items fetched')
                break
            items.extend(fetched_items)

            nxt = results.get('nextLink')

            if nxt:
                # we should fetch some more items
                if params.get('start_index') and len(items) == params.get('start_index'):
                    self.log.debug(u'STRANGE: seems like we are looping over again')
                    break
                params['start_index'] = len(items) + 1  # 1-based counting
            else:
                assert len(items) == results.get('totalResults')
                break
            iteration += 1

        if results:
            total_results = results.get('totalResults')
        else:
            total_results = 'NO DATA'
        self.log.info('Fetched {} from {} in {} iterations '.format(len(items), total_results, iteration))

        data = [dict(zip(headers, map(lambda x: x.strip(), row))) for row in items]
        return dict(headers=headers, items=data)

    @customer_callable
    def get_data(self, query):
        return self._query(params=query)

    @customer_callable
    def get_profiles(self):
        management = self.analytics.management()
        web_properties = []
        accounts = management.accounts().list().execute()
        for account in accounts['items']:
            web_property = management.webproperties().list(
                accountId=account['id']
            ).execute().get('items', [])
            web_properties.extend(web_property)
        all_profiles = []
        for wp in web_properties:
            profiles = management.profiles().list(
                accountId=wp['accountId'], webPropertyId=wp['id']
            ).execute()
            all_profiles.extend(list(profiles.get('items', []) or []))
        return all_profiles
