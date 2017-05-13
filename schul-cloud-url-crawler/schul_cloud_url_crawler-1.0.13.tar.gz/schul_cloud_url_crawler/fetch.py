import requests


class Fetcher:
    """This holds the state of a fetch operation."""

    from .crawled_resource import CrawledResource

    def __init__(self, on_added_resource=None):
        """Fetch objects from urls."""
        self._resources = []
        self._on_added_resource = on_added_resource

    def fetch(self, url, origin=[], relative_id=""):
        """Fetch a url and add the resources to this fetcher.

        - url: the url to fetch
        - origin: where you got the url from
        - relative_id: if you got the url from somewhere, how you would identify it there
        """
        response = requests.get(url)
        print("origin", origin)
        try:
            resource = response.json()
        except ValueError:
            links = response.text.split()
            for i, link in enumerate(links):
                self.fetch(link, origin + [url + "#" + str(i)], relative_id + "." + str(i))
        else:
            crawled_resource = self.CrawledResource(
                resource, origin + [url], relative_id)
            self._resources.append(crawled_resource)
            if self._on_added_resource is not None:
                self._on_added_resource(crawled_resource)

    def get_resources(self):
        """Return a list of resources as defined in the api.

        These are collected from the crawled_resources.
        """
        return [ resource.crawled_resource for resource in self._resources]

    @property
    def crawled_resources(self):
        """The crawled resources."""
        return self._resources


def fetch(url_or_list_of_urls, on_added_resource=None):
    """Return a Fetcher that fetches the urls.

    - on_added_resource: a callback to call when a resource is added.
    """
    fetcher = Fetcher(on_added_resource)
    if not isinstance(url_or_list_of_urls, list):
        url_or_list_of_urls = [url_or_list_of_urls]
    for url in url_or_list_of_urls:
        fetcher.fetch(url)
    return fetcher

