from imgurpython import ImgurClient

import click
import os
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


def get_config():
    client_id = os.environ.get('IMGUR_API_ID')
    client_secret = os.environ.get('IMGUR_API_SECRET')

    config = ConfigParser.SafeConfigParser()
    config.read([os.path.expanduser('~/.config/imgur_uploader/uploader.cfg')])

    try:
        imgur = dict(config.items("imgur"))
    except:
        imgur = {}

    client_id = client_id or imgur.get("id")
    client_secret = client_secret or imgur.get("secret")

    if not (client_id and client_secret):
        return {}

    return {"id": client_id, "secret": client_secret}


@click.command()
@click.argument('image', type=click.Path(exists=True))
def upload_image(image):
    """Uploads an image file to Imgur"""

    config = get_config()

    if not config:
        click.echo("Cannot upload - could not find IMGUR_API_ID or "
                   "IMGUR_API_SECRET environment variables or config file")
        return

    client = ImgurClient(config["id"], config["secret"])

    click.echo('Uploading file {}'.format(click.format_filename(image)))

    response = client.upload_from_path(image)

    click.echo('File uploaded - see your image at {}'.format(response['link']))

    try:
        import pyperclip
        pyperclip.copy(response['link'])
    except ImportError:
        print("pyperclip not found. To enable clipboard functionality,"
              " please install it.")

if __name__ == '__main__':
    upload_image()
