import requests
import json
from promise import Promise
from .blitz_queue import Queue
from .blitz_socket import Socket
from .blitz_http import Http


def setup_promise(self, resolve, reject, options):
    self.options = options
    self.queue = Queue(options)

    # Get access token if credentials are provided
    if options.get('user_key') and options.get('user_secret'):
        # Set auth token for supplied user data
        (self.get_token(options.get('user_key'), options.get('user_secret'))
            .then(self.set_headers(self.access_token))
            .then(self.set_client(options.get('use_socket')))
            .then(resolve(None)))
    # Credentials are not provided
    else:
        # Set connection target and connect with client
        self.auth_options = {
            'namespace': self.options.get('namespace'),
            'api_url': self.options.get('api_url'),
            'api_port': self.options.get('api_port'),
            'auth_url': self.options.get('auth_url')
        }
    self.set_client(options.get('use_socket')).then(resolve(None))


def get_token_promise(self, resolve, reject, user_key, user_secret):
    # Set auth options
    auth_request = {
        'user_key': user_key,
        'user_secret': user_secret
    }

    # Send to /auth endpoint
    res = requests.request("POST", self.options.get('auth_url') + 'token', data=auth_request)

    if res.ok:
        # Save token in class object
        content = res.json()
        self.access_token = content.get('access_token')
        self.refresh_token = content.get('refresh_token')
        resolve(None)
    else:
        reject()


def set_client_promise(self, resolve, reject, use_socket):
    # Use appropriate client (default: socket)
    if use_socket:
        self.client = Socket()
        self.client.config(self.auth_options, resolve, reject)
    else:
        self.client = Http()
        self.client.config(self.auth_options, resolve, reject)


def refresh_token_promise(self, resolve, reject, token):
    if not token:
        token = self.refresh_token

    # Refresh state for multiple failed requests
    if not self.refreshing:
        self.refreshing = True

        # Set auth options
        auth_request = {
            'refresh_token': token
        }

        # Send to /auth endpoint
        res = requests.request("POST", self.options.get('auth_url') + 'token', data=auth_request)

        if res.ok:
            # Save token in class object
            content = res.json()
            self.access_token = content.get('access_token')
            self.set_headers()
            self.refreshing = False
            self.set_client(self.options.get('use_socket')).then(resolve(None))
        else:
            reject()
    else:
        # Already refreshing? -> Add to queue
        resolve(None)


def request_promise(self, resolve, reject, verb, query):
    # Avoid rate limit errors if not disabled
    (self.queue.throttle()
        # Let connection send request
        .then(lambda res: self.client.send(verb, query))
        # Check if response is error
        .then(lambda res: self.err_check(res, verb, query))
        # Res is potentially modified (non-err) res from err_check
        .then(lambda res: resolve(res))
        .catch(lambda err: reject(err)))


def err_check_promise(self, resolve, reject, res, verb, query):
    status_prefix = str(res.get('statusCode'))[0] if res.get('statusCode') else None

    # Response not 2xx?
    if res.get('body') and status_prefix != '2':
        # If expired: Get new token with refresh token & retry method
        if 'jwt expired' in str(res.get('body')):
            (self.refresh_token_method()
                # Retry original method
                .then(self.request(verb, query))
                # Modify response for main
                .then(lambda x: resolve(x)))
        # Rate limited
        elif 'Rate limit' in str(res.get('body')):
            # Rejection due to frequency
            if 'Request intervals too close' in str(res.get('body')):
                (self.queue.delay(self.queue.delay_diff)
                    .then(self.request(verb, query))
                    .then(lambda x: resolve(x)))
            # Rejection due to empty token bucket
            if 'Max requests per interval reached' in str(res.get('body')):
                (self.queue.delay(self.queue.delay_max)
                    .then(self.request(verb, query))
                    .then(lambda x: resolve(x)))
        # Unhandled error
        else:
            reject(res)
    # No error
    else:
        resolve(res)


class Connection:
    def __init__(self):
        self.auth_options = None
        self.options = None
        self.token = None
        self.queue = None
        self.refreshing = None
        self.client = None

    def setup(self, options):
        return Promise(lambda resolve, reject: setup_promise(self, resolve, reject, options))

    """
    Get token on initial call and expiration
    Always uses http /auth endpoint
    """
    def get_token(self, user_key, user_secret):
        return Promise(lambda resolve, reject: get_token_promise(self, resolve, reject, user_key, user_secret))

    """
    Config headers for request/socket
    Leave independent param <token>. May be useful for manual action.
    """
    def set_headers(self, token):
        if not token:
            token = self.token
        self.auth_options = {
            'token': token,
            'namespace': self.options.get('namespace'),
            'api_url': self.options.get('api_url'),
            'api_port': self.options.get('api_port'),
            'auth_url': self.options.get('auth_url')
        }

    """
    Compare connection type, then create new client with previous options
    """
    def set_client(self, use_socket):
        return Promise(lambda resolve, reject: set_client_promise(self, resolve, reject, use_socket))

    """
    Get new access token from refresh_token & save in object
    """
    def refresh_token_method(self, token):
        return Promise(lambda resolve, reject: refresh_token_promise(self, resolve, reject, token))

    """
    RESTful methods
    """
    def request(self, verb, query):
        return Promise(lambda resolve, reject: request_promise(self, resolve, reject, verb, query))

    """
    Handles Error responses
    """
    def err_check(self, res, verb, query):
        return Promise(lambda resolve, reject: err_check_promise(self, resolve, reject, res, verb, query))

    """
    Return warning if wrong connection type is set
    """
    def warn_socket(self):
        if not self.__class__.__name__ == 'Socket':
            print("nexus-stats-api cannot listen toe vents without socket.io stream. "
                  "Set options.get('connection_type'): 'socket', if you want to use this feature.")
            return False
