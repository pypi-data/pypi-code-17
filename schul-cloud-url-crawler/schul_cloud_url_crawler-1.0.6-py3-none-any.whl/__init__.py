import requests


class Fetcher:

    def __init__(self):
        """Fetch objects from urls."""
        self._ressources = []

    def fetch(self, url):
        """Fetch a url and add the ressources to this fetcher."""
        response = requests.get(url)
        ressource = response.json()
        self._ressources.append(ressource)

    def get_ressources(self):
        """Return a list of ressources as defined in the api."""
        return self._ressources


def fetch(urls):
    """Return a Fetcher that fetches the urls."""
    fetcher = Fetcher()
    for url in urls:
        fetcher.fetch(url)
    return fetcher