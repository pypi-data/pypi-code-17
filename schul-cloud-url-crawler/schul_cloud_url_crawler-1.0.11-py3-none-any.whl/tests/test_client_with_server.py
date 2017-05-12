"""The the client with a real server over http."""

def test_all_resources_are_unique(resources):
    """Make sure all resources existonly once in the array.

    This is a requirement to split up the array.
    """
    for resource in resources:
        assert resources.count(resource) == 1

def test_all_resources_on_the_server_are_from_the_client(
        resources_server, sclient, resources, resource_urls):
    """Crawl some resources and find them on the server."""
    assert not resources_server.get_resources()
    sclient.update(resource_urls)
    server_resources = resources_server.get_resources()
    print(server_resources)
    for server_resource in server_resources:
        assert any(server_resource["X-Test-Id"] == resource["X-Test-Id"]
                   for resource in resources)

def test_all_updated_resources_are_on_the_server(
        resources_server, sclient, resources, resource_urls):
    """Crawl some resources and find them on the server."""
    sclient.update(resource_urls)
    server_resources = resources_server.get_resources()
    for resource in resources:
        assert any(server_resource["X-Test-Id"] == resource["X-Test-Id"]
                   for server_resource in server_resources)
    

