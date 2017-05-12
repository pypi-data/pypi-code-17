import click

@click.command()
@click.argument("api", type=str, required=True)
@click.argument("urls", type=str, nargs=-1, required=False)
@click.option("--basic", default=None, type=str, metavar="username:password", 
              help="Username an password for authentication at the API.")
@click.option("--apikey", default=None, type=str, metavar="api-key",
              help="The api key for authentication at the API.")
def main(api, urls=[], basic=None, apikey=None):
    """Fetch ressources from URLS and post them to the API."""
    pass

