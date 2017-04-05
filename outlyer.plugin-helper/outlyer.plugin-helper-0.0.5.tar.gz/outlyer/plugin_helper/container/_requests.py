import urlparse
import requests.api

from outlyer.plugin_helper import container


def safe_request(method, url, **kwargs):
    url = sanitize_container_endpoint(url)
    return requests.request(method, url, **kwargs)


def sanitize_container_endpoint(url):
    if not container.is_container():
        return url
    parsed = urlparse.urlparse(url)

    if parsed.hostname in ['127.0.0.1', 'localhost']:
        url = _set_to_container_ip(parsed)

    return url


def _set_to_container_ip(parse_endpoint):
    parts = list(parse_endpoint)
    hostname = container.get_container_ip()

    if not hostname:
        hostname = parse_endpoint.hostname

    if parse_endpoint.port:
        hostname = "%s:%s" % (hostname, parse_endpoint.port)

    parts[1] = hostname

    return urlparse.urlunparse(parts)


def patch():
    if not is_patched():
        requests.api._request = requests.api.request
        requests.api.request = safe_request


def unpatch():
    if is_patched():
        requests.api.request = getattr(requests.api, '_request')
        delattr(requests.api, '_request')


def is_patched():
    return hasattr(requests.api, '_request')
