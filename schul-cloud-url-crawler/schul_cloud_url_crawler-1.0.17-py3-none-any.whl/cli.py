"""
The command line interface for the crawler.

TODO:
- delete all
- delete not updated
- delete from urls
- delete not from urls

"""
import click
import schul_cloud_url_crawler.resource_client as resource_client
from schul_cloud_resources_api_v1 import ApiClient, ResourceApi
from schul_cloud_resources_api_v1.rest import ApiException
import schul_cloud_resources_api_v1.auth as auth
from urllib3.exceptions import MaxRetryError
import traceback
import sys

UnReachable = (MaxRetryError,)

error_messages = {
    3: "The resources server could be reached but basic authentication failed.",
    4: "The resources server could be reached but API-key authentication failed.",
    5: "The resources server could be reached but it requires authentication with --basic or --apikey.",
    6: "The resource server could not be reached.",
    7: "You can only provide one authentication mechanism with --basic and --apikey.",
    8: "Basic authentication requires a username and a password divided by \":\". Example: --basic=user:password",
}

def error(return_code):
    """Raise an error and explain it."""
    ty, err, tb = sys.exc_info()
    if err:
        traceback.print_exception(ty, err, tb)
    click.echo("Error {}: {}".format(return_code, error_messages[return_code]))
    exit(return_code)


def authenticate(basic, apikey):
    """Authenticate with the parameters.

    Return the return code in case auf authentication failure.
    """
    if basic is not None and apikey is not None:
        error(7)
    if basic is not None:
        username_and_password = basic.split(":", 1)
        if len(username_and_password) == 1:
            error(8)
        username, password = username_and_password
        auth.basic(username, password)
        return 3
    elif apikey is not None:
        auth.api_key(apikey)
        return 4
    auth.none()
    return 5


@click.command()
@click.argument("api", type=str, required=True)
@click.argument("urls", type=str, nargs=-1, required=False)
@click.option("--basic", nargs=1, type=str, metavar="username:password", 
              help="Username an password for authentication at the API.")
@click.option("--apikey", nargs=1, type=str, metavar="api-key",
              help="The api-key for authentication at the API.")
@click.option("--delete-all", is_flag=True, default=False,
              help="Delete all resources stored on the server. "
                   "This only affects resources you are authenticated for.")
@click.option("--delete-not-mentioned", is_flag=True, default=False,
              help="Delete all resources from urls which are not mentioned in the "
                   "arguments. Enable this if this is your only crawler.")
@click.option("--id", default="url-crawler", nargs=1,
              type=str, metavar="crawler-id", 
              help="The crawler-id is the id of the crawler. "
                   "By changing the id, you can connect multiple crawlers which do not"
                   " interact. "
                   "The crawler only adds and deletes resources with the crawler-id. "
                   "--delete-all is the only option that affects crawlers with other ids.")
def main(api, urls=[], basic=None, apikey=None, delete_not_mentioned=False,
         delete_all=False, id="url-crawler"):
    """Fetch ressources from URLS and post them to the API."""
    urls = list(urls)
    print(api, urls, basic, apikey, delete_not_mentioned, delete_all, id)
    api_client = ApiClient(api)
    resource_api = ResourceApi(api_client)
    client = resource_client.ResourceClient(resource_api, id)
    auth_error = authenticate(basic, apikey)
    try:
        if delete_all:
            client.delete_resources()
        if delete_not_mentioned:
            client.delete_resources_not_from(urls)
        client.update(urls)
    except ApiException as err:
        if err.status == 401:
            click.echo(err.body)
            error(auth_error)
        raise
    except UnReachable:
        error(6)
