import datetime
import logging

import requests
import requests.packages


logger = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()


class Config(object):
    API_URL = 'https://api.intercom.io/'

    def __getitem__(self, key):
        url = self.API_URL[0:]
        headers = {
            'Content-type': 'application/json',
            'User-agent': 'intercomio',
            'Accept': 'application/json',
        }
        url = url + key.split('_')[0].lower()
        return url, headers


class Endpoint(object):
    def __init__(self, url, headers, auth, action=None):
        self._url, self.headers, self._auth, self.action = url, headers, auth, action

    def _get(self, filters=None, action_id=None, id=None, **kwargs):
        return api_call(self._auth, 'get', self._url, headers=self.headers, action=self.action, action_id=action_id,
                        filters=filters, resource_id=id, **kwargs)

    def list(self, filters=None, action_id=None, **kwargs):
        return self._get(filters=filters, **kwargs)

    def get(self, id=None, filters=None, action_id=None, **kwargs):
        return self._get(id=id, filters=filters, **kwargs)

    def create(self, data=None, filters=None, id=None, action_id=None, **kwargs):
        return api_call(self._auth, 'post', self._url, headers=self.headers, resource_id=id, data=data,
                        action=self.action, action_id=action_id, filters=filters, **kwargs)

    def update(self, id, data, filters=None, action_id=None, **kwargs):
        return api_call(self._auth, 'put', self._url, resource_id=id, headers=self.headers, data=data,
                        action=self.action, action_id=action_id, filters=filters, **kwargs)

    def delete(self, id=None, filters=None, **kwargs):
        return api_call(self._auth, 'delete', self._url, action=self.action, headers=self.headers, resource_id=id,
                        filters=filters, **kwargs)


class Client(object):
    def __init__(self, auth=None, config=Config()):
        self.auth, self.config = auth, config

    def __getattr__(self, name) -> Endpoint:
        split = name.split('_')
        fname = split[0]
        action = None
        if len(split) > 1:
            action = split[1]
        url, headers = self.config[name]
        endpoint = type(fname, (Endpoint,), {})(url=url, headers=headers, action=action, auth=self.auth)
        setattr(self, name, endpoint)
        return endpoint


def api_call(auth, method, url, headers, data=None, filters=None, resource_id=None,
             timeout=60, action=None, action_id=None, **kwargs):
    url = build_url(url, method=method, action=action, resource_id=resource_id, action_id=action_id)
    req_method = getattr(requests, method)

    try:
        response = req_method(url, data=data, params=filters, headers=headers, auth=auth,
                              timeout=timeout, verify=False, stream=False)

        logger.debug('REQUEST: %s' % response.request.url)
        logger.debug('REQUEST_HEADERS: %s' % response.request.headers)
        logger.debug('REQUEST_CONTENT: %s' % response.request.body)

        logger.debug('RESPONSE: %s' % response.content)
        logger.debug('RESP_HEADERS: %s' % response.headers)
        logger.debug('RESP_CODE: %s' % response.status_code)

        response.raise_for_status()
        return response

    except requests.exceptions.Timeout as err:
        raise TimeoutError(err)
    except requests.RequestException as err:
        if err.response is not None \
                and err.response.status_code == 429 \
                and 'x-ratelimit-reset' in err.response.headers:
            raise RateLimitError(err)
        raise ApiError(err)


def build_url(url, method, action=None, resource_id=None, action_id=None):
    if resource_id:
        url += '/%s' % str(resource_id)
    if action:
        url += '/%s' % action
    return url


class ApiError(requests.RequestException):
    def __init__(self, err: requests.RequestException):
        super(ApiError, self).__init__(request=err.request, response=err.response)


class RateLimitError(ApiError):
    def __init__(self, err: requests.RequestException):
        super(RateLimitError, self).__init__(err)
        reset = datetime.datetime.fromtimestamp(int(self.response.headers['x-ratelimit-reset']))
        self.eta = reset + datetime.timedelta(minutes=1)


class TimeoutError(ApiError):
    pass
