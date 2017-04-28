import logging
import email.utils
import requests
from .signed_request_auth import SignedRequestAuth
from . import schema, exceptions


class NiftyWalletClient(object):
    def __init__(self, config, logger=None):
        self.config = config
        if not hasattr(self.config, 'api_base'):
            self.config.api_base = 'http://api.wallet.nifty.co.ke/api/v1'
        self.logger = logger or logging.getLogger(__name__)

    @property
    def wallet_url(self):
        return '{config.api_base}/user/{config.user_id}/wallet'.format(config=self.config)

    @property
    def wallet_transactions_url(self):
        return '{wallet_url}/transactions'.format(wallet_url=self.wallet_url)

    @property
    def headers(self):
        return {
            "date": email.utils.formatdate(usegmt=True),
            "content-type": "application/json"
        }

    @property
    def auth(self):
        return SignedRequestAuth(self.config.key_id, self.config.secret)

    def log_response(self, request):
        self.logger.info("%s request to: %s " % (request.request.method, request.url))
        self.logger.debug("Headers: %s" % request.request.headers)
        self.logger.debug("Content: %s" % request.content)


    def process_response(self, response, schema_factory):
        self.log_response(response)
        try:
            return schema_factory.load(response.json()).data
        # Catches simplejson & stdlib decode errors (requests uses either)
        except ValueError as exc:
            self.logger.exception("Unable to parse response. Is it JSON?" % response.content)
            raise exceptions.ResponseFormatError(exc)
        except requests.exceptions.HTTPError as exc:
            self.logger.exception("HTTP Response failure: %s Content: %s" % (exc, response.content))
            if response.status_code == 401:
                raise exceptions.AuthenticationError(exc)
            raise exceptions.ResponseError(exc)
        except Exception as exc:
            self.logger.exception("Unhandled Exception: %s Content:%s " % (exc, response.content))
            raise exceptions.NiftyBaseError(exc)


    def get_wallet(self):
        """
        Fetch the wallet details. If there's no wallet, the response will be an empty list
        Otherwise return the existing wallet
        """
        response = requests.get(self.wallet_url, auth=self.auth, headers=self.headers, json=dict())
        return self.process_response(response, schema.WalletSchema())

    def create_wallet(self):
        """
        Create the wallet if it doesn't exist.
        Otherwise return the existing wallet
        """
        response = requests.post(self.wallet_url, auth=self.auth, headers=self.headers, json=dict())
        return self.process_response(response, schema.WalletSchema())

    def consume_token(self, **kwargs):
        """
        Consume a token and credit account with token amount
        """
        data = kwargs
        response = requests.put(self.wallet_url, auth=self.auth, headers=self.headers, json=data)
        return self.process_response(response, schema.TransactionSchema())

    def transactions(self, **kwargs):
        """
        Consume a token and credit account with token amount
        """
        data = kwargs
        response = requests.get(self.wallet_transactions_url,auth=self.auth, headers=self.headers, json=data)
        return self.process_response(response, schema.TransactionSchema())
