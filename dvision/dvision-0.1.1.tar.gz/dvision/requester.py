from __future__ import print_function

import logging
from socket import error as SocketError

import requests
from requests.adapters import HTTPAdapter
from retrying import retry

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()  # writes to stderr
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def is_network_error(exception):
    """
    Retry if a network-related exception occurs. Fail otherwise.
    """
    return any([isinstance(exception, SocketError), isinstance(exception, requests.RequestException)])


class DVIDRequester(object):
    def __init__(self, hostname_whitelist):
        self.whitelist = hostname_whitelist
        self.session = requests.Session()

    @retry(wait_exponential_multiplier=100, wait_exponential_max=60000,
           retry_on_exception=is_network_error)
    def get(self, *args, **kwargs):
        logger.debug("Getting url " + repr(args))
        with requests.Session() as session:
            adapter = HTTPAdapter(pool_connections=1, pool_maxsize=1)
            session.mount('http://', adapter)
            response = session.get(*args, **kwargs)
            if response.ok:
                return response
            else:
                msg = "DVID response not ok from {}\n{}".format(response.url, response.text)
                logger.error(msg)
                raise Exception(msg)

    @retry(wait_exponential_multiplier=100, wait_exponential_max=10000,
           retry_on_exception=is_network_error)
    def post(self, *args, **kwargs):
        url_args = list(args) + [kwargs.get('url', '')]
        hostname_is_ok = any([
                any([hostname in url_arg for hostname in self.whitelist])
                for url_arg in url_args])
        if hostname_is_ok:
            response = self.session.post(*args, **kwargs)
            if response.ok:
                return response
            else:
                raise Exception("Bad response: {}".format(response.text))
        else:
            raise ValueError("posting to servers other than {wl} not allowed" \
                             "you requested {url_args}" \
                             .format(wl=self.whitelist, url_args=url_args))
