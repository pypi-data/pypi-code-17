"""Test the communication with the api and the server.
"""
from pytest import mark
from unittest.mock import call
from collections import namedtuple

RESPONSE = namedtuple("RESPONSE", ["data"])
ID = namedtuple("ID", ["id"])


def test_delete_all_resources(client, api):
    """Test the deletion of all resources."""
    client.delete_resources()
    api.delete_resources.assert_called_once_with()


def test_update_present_resource(client, api, crawled_resource):
    """Test that the client tries to delete the resource and add it again if it is present."""
    _id = client.client_id + ":" + crawled_resource.id
    post = crawled_resource.get_api_resource_post(client.client_id + ":")
    api.get_resource_ids.return_value = RESPONSE([ID(_id)])
    client.update_resource(crawled_resource)
    assert api.mock_calls == [call.get_resource_ids(), call.delete_resource(_id), call.add_resource(post)]


def test_update_nonexistent_resource(client, api, crawled_resource):
    """Test that a delete call is not issued if the resource does not exist."""
    _id = client.client_id + ":" + crawled_resource.id
    post = crawled_resource.get_api_resource_post(client.client_id + ":")
    api.get_resource_ids.return_value = RESPONSE([])
    client.update_resource(crawled_resource)
    assert api.mock_calls == [call.get_resource_ids(), call.add_resource(post)]

