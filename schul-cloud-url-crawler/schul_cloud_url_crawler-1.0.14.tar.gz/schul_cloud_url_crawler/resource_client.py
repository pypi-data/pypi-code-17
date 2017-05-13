import hashlib
import schul_cloud_url_crawler
from pprint import pprint


def hash_url(url):
    """Return the hashed url."""
    return hashlib.sha256(url.encode()).hexdigest()

class ResourceClient:
    """The client to communicate with the ressource server."""

    CLIENT_RESOURCE_ID_DIVISION_STRING = "+"

    def __init__(self, api, client_id="url-crawler"):
        """Communicate with the server behind the api.

        - api: a schul_cloud_resources_api_v1.ResourceApi object.
        - client_id: the id of the client. Only resources with this id are touched.
        """
        self._api = api
        self._client_id = client_id
        self.__ids = None

    @property
    def _ids(self):
        """Return a list of ids on the server."""
        if self.__ids is None:
            _cid = self._client_id + "+"
            self.__ids = set(_id.id for _id in self._api.get_resource_ids().data
                             if _id.id.startswith(_cid))
        return self.__ids

    fetch = staticmethod(schul_cloud_url_crawler.fetch)

    @property
    def client_id(self):
        """Return the id of the client. Only resources with this id are touched."""
        return self._client_id

    def delete_resources(self):
        """Delete all resources."""
        self._api.delete_resources()

    def delete_resources_from(self, urls):
        """Delete all resources which were crawled from these urls."""
        url_hashes = list(map(hash_url, urls))
        for _id in self._ids:
            if any(h in _id for h in url_hashes):
                self._api.delete_resource(_id)


    def delete_resources_not_from(self, urls):
        """Delete all resources which do not originate from the urls."""
        url_hashes = list(map(hash_url, urls))
        for _id in self._ids:
            if all(h not in _id for h in url_hashes):
                self._api.delete_resource(_id)

    def update(self, urls):
        """Synchronize the content on the server with the given urls.

        The urls are fetched from the source and added to the api.
        - Nonexisting resources are created.
        - Existing resources are replaced.
        - Deleted resources are deleted.
        - Only resources with this client's id are touched.
        """
        updated_ids = set()
        def sync_resource(crawled_resource):
            """Syncronize a crawled resource."""
            _id = self.update_resource(crawled_resource)
            updated_ids.add(_id)
        self.fetch(urls, sync_resource)
        url_hashes = set(map(hash_url, urls))
        for untouched_id in self._ids - updated_ids:
            for url_hash in url_hashes:
                if url_hash in untouched_id:
                    self._api.delete_resource(untouched_id)
                    self._ids.remove(untouched_id)
                    print("delete and untouched", untouched_id)

    def delete_resource(self, resource_id):
        """Delete the identified resource.

        The client id is prefixed.
        """
        resource_id = self._client_id + self.CLIENT_RESOURCE_ID_DIVISION_STRING + resource_id
        if resource_id in self._ids:
            self._api.delete_resource(resource_id)
            self._ids.remove(resource_id)
#        print("delete", self._ids, resource_id)
        print("delete()", resource_id)

    def update_resource(self, crawled_resource):
        """Update the crawled resource on the server.

        This deleted the resource on the server and posts it again.
        Return the id of the resource.
        """
        post = crawled_resource.get_api_resource_post(self._client_id + self.CLIENT_RESOURCE_ID_DIVISION_STRING)
        resource_id = post["data"]["id"]
        if resource_id in self._ids:
             self._api.delete_resource(resource_id)
        self._api.add_resource(post)
        self._ids.add(resource_id)
#        print("update", self._ids)
        print("update()", resource_id)
        return resource_id


