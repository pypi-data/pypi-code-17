

class ResourceClient:
    """The client to communicate with the ressource server."""

    def __init__(self, api, client_id="url-crawler"):
        """Communicate with the server behind the api.

        - api: a schul_cloud_resources_api_v1.ResourceApi object.
        - client_id: the id of the client. Only resources with this id are touched.
        """
        self._api = api
        self._client_id = client_id

    @property
    def client_id(self):
        """Return the id of the client. Only resources with this id are touched."""
        return self._client_id

    def delete_resources(self):
        """Delete all resources."""
        self._api.delete_resources()

    def delete_resources_from(self, urls):
        """Delete all resources which were crawled from these urls."""


    def delete_resources_not_from(self, urls):
        """Delete all resources which do not originate from the urls."""


    def update(self, urls):
        """Synchronize the content on the server from the given urls.

        The urls are fetched from the source and added to the api.
        - Nonexisting resources are created.
        - Existing resources are replaced.
        - Deleted resources are deleted.
        """

    def delete_resource(self, resource_id):
        """Delete the identified resource.

        The client id is prefixed.
        """
        self._api.delete_resource(self._client_id + ":" + resource_id)

    def update_resource(self, crawled_resource):
        """Update the crawled resource on the server.

        This deleted the resource on the server and posts it again.
        """
        ids = self._api.get_resource_ids()
        post = crawled_resource.get_api_resource_post(self._client_id + ":")
        resource_id = post["data"]["id"]
        print(ids, resource_id)
        if any(_id.id == resource_id for _id in ids.data):
             self._api.delete_resource(resource_id)
             print("delete", resource_id)
        self._api.add_resource(post)


