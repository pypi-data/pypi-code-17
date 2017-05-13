"""The the client with a real server over http."""
from pytest import fixture
from schul_cloud_url_crawler.cli import main

def test_all_resources_are_unique(resources):
    """Make sure all resources existonly once in the array.

    This is a requirement to split up the array.
    """
    for resource in resources:
        assert resources.count(resource) == 1


def test_resource_server_starts_without_resources(resources_server):
    """Make sure there are not resources on the server."""
    assert not resources_server.get_resources()

@fixture(params=range(4))
def update_function(request, sclient, resources_server):
    """Return an update function.

    This function uses:
    - The sclient.update method
    - The command line interface
      - no auth
      - basic auth
      - api key auth
    """
    def use_server_client(urls):
         sclient.update(urls)
    def use_api_without_authentication(urls):
         main(args=[resources_server.url] + urls, standalone_mode=False)
    def use_api_basic_authentication(urls):
         main(args=["--basic=valid1@schul-cloud.org:123abc", resources_server.url] + urls, standalone_mode=False)
    def use_api_apikey_authentication(urls):
         main(args=["--apikey=abcdefghijklmn", resources_server.url] + urls, standalone_mode=False)
    return [use_server_client, use_api_without_authentication, 
            use_api_basic_authentication, use_api_apikey_authentication][request.param]


def test_all_resources_on_the_server_are_from_the_client(
        resources_server, sclient, resources, resource_urls, update_function):
    """Crawl some resources and find them on the server."""
    update_function(resource_urls)
    server_resources = resources_server.get_resources()
    print(server_resources)
    for server_resource in server_resources:
        assert any(server_resource["X-Test-Id"] == resource["X-Test-Id"]
                   for resource in resources)


def test_all_updated_resources_are_on_the_server(
        resources_server, sclient, resources, resource_urls, update_function):
    """Crawl some resources and find them on the server."""
    update_function(resource_urls)
    server_resources = resources_server.get_resources()
    assert len(server_resources) >= len(resources)
    for resource in resources:
        assert any(server_resource["X-Test-Id"] == resource["X-Test-Id"]
                   for server_resource in server_resources)

