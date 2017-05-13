"""The adapter from crawler to resource api.

"""
import hashlib


class CrawledResource:
    """A resource crawled by the crawler.


    This is an adapter bewteen crawler and API.
    The id is computed by the originating url and the id it has in the url.
    """

    def __init__(self, resource, origin_urls:list, id_in_origin=""):
        """Create a new crawled resource with the source urls."""
        if not origin_urls:
            raise ValueError("Expected the resource to have an origin.")
        self._resource = resource
        self._origin_urls = origin_urls
        self._id_in_origin = id_in_origin

    @property
    def crawled_resource(self):
        """The unchanged crawled resource."""
        return self._resource

    @property
    def origin_urls(self):
        """The urls where this resource is from."""
        return self._origin_urls

    @property
    def provider(self):
        """The provider which identifies this client."""
        return {"description": "This crawler crawls urls and adds them to the database.",
                "name": __name__.split(".", 1)[0],
                "url": "https://github.com/schul-cloud/schul_cloud_url_crawler",
                "url_trace": self.origin_urls}

    @property
    def resource(self):
        """The resource as seen by the crawler."""
        resource = self._resource.copy()
        resource.setdefault("providers", [])
        resource["providers"] = resource["providers"] + [self.provider]
        return resource

    def get_api_resource_post(self, id_prefix=""):
        """The jsonapi format for the resource."""
        return {"data":{"attributes":self.resource, "id": id_prefix+self.id, "type":"resource"}}

    @property
    def id(self):
        """Return the id of this resource."""
        return self.origin_id + self._id_in_origin

    @property
    def origin_id(self):
        """The id of the origin of this resource."""
        return hashlib.sha256(self.origin_url.encode()).hexdigest()

    @property
    def origin_url(self):
        """Return the url this resource is from."""
        return self._origin_urls[0]

    @property
    def id_in_origin(self):
        """The id the resource has in its originating url."""
        return self._id_in_origin

    def __repr__(self):
        """A string representation of this resource."""
        return "<{} {}>".format(self.__class__.__name__, self.id)