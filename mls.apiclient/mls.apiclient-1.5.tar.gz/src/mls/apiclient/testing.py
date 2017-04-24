# -*- coding: utf-8 -*-
"""Test helpers for mls.apiclient."""

# python imports
import itertools
import os
import re
import responses
import urllib

# local imports
from mls.apiclient import (
    REST_API_URL,
    REST_API_VERSION,
)
from mls.apiclient import utils

HOST = 'demomls.com'
BASE_URL = 'http://{0}'.format(HOST)


def setup_fixtures():
    """Setup the test fixtures for integration tests."""

    base_params = {
        'apikey': 'YOUR_API_KEY',
        'lang': 'en',
    }

    # register the development endpoints
    _register(
        'developments',
        params=base_params,
        fixture='integration/development_list_26-1.json',
    )
    _register(
        'developments',
        params=dict(
            {
                'fields': ''.join([
                    'id,title,logo,location,lot_size,location_type,',
                    'geographic_type,number_of_listings,number_of_phases,',
                    'number_of_groups,number_of_pictures',
                ]),
                'limit': 5,
                'offset': 0,
            },
            **base_params),
        fixture='integration/development_list_26-1.json',
    )


def load_fixture(name):
    """Return a file-like fixture, just like urlopen would."""
    fixture = open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'tests',
            'fixtures',
            name,
        ), 'r'
    )
    return fixture.read()


def get_url(base_url, endpoint):
    return '/'.join([
        base_url,
        endpoint,
    ])


def API_BASE():
    return utils.join_url(BASE_URL, REST_API_URL, REST_API_VERSION)


def _register(endpoint, content=None, fixture=None, params=None):
    if fixture:
        content = load_fixture(fixture)
    base_url = get_url(API_BASE(), endpoint)
    if not params:
        responses.add(
            responses.GET,
            re.compile(base_url),
            body=content,
            match_querystring=True,
            status=200,
            content_type='application/json',
        )
    else:
        for keys in itertools.permutations(params.keys()):
            query = urllib.urlencode(
                [(key, params.get(key)) for key in keys]
            )
            responses.add(
                responses.GET,
                re.compile('\?'.join((base_url, query))),
                body=content,
                match_querystring=True,
                status=200,
                content_type='application/json',
            )
