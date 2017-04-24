# POTENTIALLY SUPPORT MULTIPLE ENVIRONMENTS
from __future__ import absolute_import, division, print_function, unicode_literals
LOCAL = False

envs = {'dev', 'staging'}

env = 'dev'

if LOCAL:
    ENDPOINTS = {
        'asset_managers': 'http://localhost:8000',
        'assets': 'http://localhost:8000',
        'books': 'http://localhost:8000',
        'corporate_actions': 'http://localhost:8000',
        'market_data': 'http://localhost:8000',
        'monitor': 'http://localhost:8000',
        'parties': 'http://localhost:8000',
        'transactions': 'http://localhost:8000'
    }
else:
    ENDPOINTS = {
        'asset_managers': 'https://mg739bdgdf.execute-api.ap-southeast-1.amazonaws.com/',
        'assets': 'https://12jlsrn8i2.execute-api.ap-southeast-1.amazonaws.com/',
        'books': 'https://jcbhgd69ie.execute-api.ap-southeast-1.amazonaws.com/',
        'corporate_actions': 'https://w5f5d9hphj.execute-api.ap-southeast-1.amazonaws.com/',
        'market_data': 'https://y7rh2tl8sj.execute-api.ap-southeast-1.amazonaws.com/',
        'monitor': 'https://6cf4vv0973.execute-api.ap-southeast-1.amazonaws.com/',
        'parties': 'https://ugkl20kxi4.execute-api.ap-southeast-1.amazonaws.com/',
        'transactions': 'https://1w0gb581sl.execute-api.ap-southeast-1.amazonaws.com/'
    }

COGNITO_CLIENT_ID = '55n70ns9u5stie272e1tl7v32v'  # This is not secret - it is just an identifier

# Do not change this
COGNITO_REGION = 'us-west-2'
COGNITO_POOL = 'us-west-2_wKa82vECF'
