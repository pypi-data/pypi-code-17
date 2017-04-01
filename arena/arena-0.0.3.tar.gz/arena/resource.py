import arena
import requests
from functools import wraps
from arena import BASE_URL


def paginated(fn):
    @wraps(fn)
    def decorated(*args, page=1, per_page=20, **kwargs):
        params = {
            'page': page,
            'per': per_page
        }
        params.update(kwargs.get('params', {}))
        kwargs['params'] = params
        return fn(*args, **kwargs)
    return decorated


class Resource():
    def _set_data(self, data):
        for name, val in data.items():
            setattr(self, name, val)

    def _headers(self, auth):
        if auth:
            if arena.access_token is not None:
                return {
                    'Authorization': 'Bearer {}'.format(arena.access_token)
                }
            elif arena.auth_token is not None:
                return {
                    'X-AUTH-TOKEN': arena.auth_token
                }
            raise AttributeError('No access token or auth token is set')
        return {}

    def _get(self, endpoint, params=None, auth=False):
        url = ''.join([BASE_URL, self.base_endpoint, endpoint])
        resp = requests.get(
            url,
            params=params or {},
            headers=self._headers(auth))
        if resp.status_code != 200:
            resp.raise_for_status()
        return resp.json()

    def _post(self, endpoint, data, params=None):
        resp = requests.post(
            ''.join([BASE_URL, self.base_endpoint, endpoint]),
            params=params or {},
            headers=self._headers(True),
            json=data)
        if resp.status_code != 200:
            resp.raise_for_status()
        return resp.json()

    def _put(self, endpoint, data, params=None):
        resp = requests.put(
            ''.join([BASE_URL, self.base_endpoint, endpoint]),
            params=params or {},
            headers=self._headers(True),
            json=data)
        if resp.status_code != 200:
            resp.raise_for_status()
        return resp.json()

    def _delete(self, endpoint, params=None):
        resp = requests.delete(
            ''.join([BASE_URL, self.base_endpoint, endpoint]),
            params=params or {},
            headers=self._headers(True))
        if resp.status_code != 200:
            resp.raise_for_status()
        return resp.json()


def resource_for_data(d):
    cls = d['base_class']
    if cls == 'Block':
        obj = arena.Block(**d)
    elif cls == 'Channel':
        obj = arena.Channel(**d)
    elif cls == 'User':
        obj = arena.User(**d)
    else:
        raise TypeError('Unknown base_class: "{}"'.format(cls))
    return obj
