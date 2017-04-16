from six.moves.urllib.parse import urlparse


def parse_url(url):
    parsed = urlparse(url)
    return parsed.hostname, parsed.port
