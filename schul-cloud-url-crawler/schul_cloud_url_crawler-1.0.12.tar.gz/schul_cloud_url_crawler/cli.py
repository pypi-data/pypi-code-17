"""
The command line interface for the crawler.

TODO:
- delete all
- delete not updated
- delete from urls
- delete not from urls

"""
import click
from schul_cloud_url_crawler.resource_client import ResourceClient
from schul_cloud_resources_api_v1 import ApiClient, ResourceApi
import schul_cloud_resources_api_v1.auth as auth



@click.command()
@click.argument("api", type=str, required=True)
@click.argument("urls", type=str, nargs=-1, required=False)
@click.option("--basic", default=None, type=str, metavar="username:password", 
              help="Username an password for authentication at the API.")
@click.option("--apikey", default=None, type=str, metavar="api-key",
              help="The api key for authentication at the API.")
def main(api, urls=[], basic=None, apikey=None):
    """Fetch ressources from URLS and post them to the API."""
    urls = list(urls)
    api_client = ApiClient(api)
    resource_api = ResourceApi(api_client)
    resource_client = ResourceClient(resource_api)
    print("updating", api, urls)
    if basic:
        username, password = basic.split(":", 1)
        auth.basic(username, password)
    elif apikey:
        auth.api_key(apikey)
    else:
        auth.none()
    resource_client.update(urls)

