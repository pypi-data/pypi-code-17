from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import logging
from google.appengine.api import urlfetch
import os
import httplib2
from configfile import ConfigFile

JSON_PATH = 'mypromo/auth_json/{}_auth.json'

class ExternalAuth(object):

    environment = os.environ['ENVIRONMENT']
    logging.info('CURRENT ENVIRONMENT: ' + str(environment))
    service_pdbcontest = None

    @classmethod
    def get_pdbcontest_service(cls):
        if not cls.service_pdbcontest:
            urlfetch.set_default_fetch_deadline(60)
            appname = None
            api_root = ''
            settings = ConfigFile()

            if ExternalAuth.environment == 'DEV':
                appname = 'pdbcontest'
                api_root = settings.get_config_variable('promo', 'DEV_URL_SERVICE_PDBCONTEST', True)
            elif ExternalAuth.environment == 'PROD':
                appname = 'pdbcontesttest1'
                api_root = settings.get_config_variable('promo', 'PROD_URL_SERVICE_PDBCONTEST', True)

            logging.info('CURRENT SERVICE URL: '+str(api_root))

            api = settings.get_config_variable('promo', 'API_NAME', True)
            version = settings.get_config_variable('promo', 'API_VERSION', True)
            discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (api_root, api, version)
            logging.info('DISCOVERY: %s', discovery_url)
            scopes = ['https://www.googleapis.com/auth/userinfo.email']

            jsonpath = JSON_PATH.format(appname)
            credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonpath, scopes=scopes)

            http_req = credentials.authorize(httplib2.Http(timeout=60))
            cls.service_pdbcontest = build(api, version, discoveryServiceUrl=discovery_url, credentials=credentials, http=http_req)

            logging.info('EXTERNAL_REQUEST: ' + api_root)
        else:
            logging.info('Getting service from memory!')

        return cls.service_pdbcontest

