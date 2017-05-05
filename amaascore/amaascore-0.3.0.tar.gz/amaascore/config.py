# POTENTIALLY SUPPORT MULTIPLE ENVIRONMENTS
from __future__ import absolute_import, division, print_function, unicode_literals
LOCAL = False

envs = {'dev', 'staging'}

ENVIRONMENT = 'staging'

if LOCAL:
    ENDPOINTS = {
        'asset_managers': 'http://localhost:8000',
        'assets': 'http://localhost:8000',
        'books': 'http://localhost:8000',
        'corporate_actions': 'http://localhost:8000',
        'fundamentals': 'http://localhost:8000',
        'market_data': 'http://localhost:8000',
        'monitor': 'http://localhost:8000',
        'parties': 'http://localhost:8000',
        'transactions': 'http://localhost:8000'
    }
else:
    ENDPOINTS = {
        'asset_managers': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/assetmanager',
        'assets': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/asset',
        'books': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/book',
        'corporate_actions': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/corporateaction',
        'fundamentals': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/fundamental',
        'market_data': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/marketdata',
        'monitor': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/monitor',
        'parties': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/party',
        'transactions': 'https://iwe48ph25i.execute-api.ap-southeast-1.amazonaws.com/%s/transaction'
    }

COGNITO_CLIENT_ID = '55n70ns9u5stie272e1tl7v32v'  # This is not secret - it is just an identifier

# Do not change this
COGNITO_REGION = 'us-west-2'
COGNITO_POOL = 'us-west-2_wKa82vECF'
