import random
import requests

from helga import log

logger = log.getLogger(__name__)


class XKCDClient(object):

    BASE = 'https://xkcd.com'
    EXT = 'info.0.json'

    def __init__(self):
        self._sess = requests.Session()

    def _request(self, comic_number=None):
        url_args = [str(a) for a in (self.BASE, comic_number, self.EXT) if a is not None]
        url = '/'.join(url_args)
        logger.debug('Requesting comic at %s', url)
        try:
            resp = self._sess.get(url)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError:
            logger.exception("Got bad response from %s", url)
            return None

    def fetch_latest(self):
        return self._request()

    def fetch_number(self, number):
        # XXX: hacking around the fact that 404 comic is not real.
        if number == 404:
            return {'img': 'http://i.imgur.com/utzTCyo.png', 'safe_title': "That's the joke.", 'alt': 'Visit the page for yourself', 'num': number}
        return self._request(number)

    def fetch_random(self, latest=None):
        if latest is None:
            latest = self.fetch_latest() or {'num': 1830}
        random_selection = random.randint(1, latest.get('num') + 1)
        return self._request(random_selection)
