import sys

import click

from bfcli.lib.api import API, me

@click.group()
def data():
  pass


@data.command()
@click.argument('path')
def upload(path):
  user = me()
  click.echo('Uploading data...')

  API.data.upload(path,
                  '/',
                  group_id=user.data['user']['defaultGroup'],
                  account_id=user.data['account']['id'])
  click.echo('Upload complete!')
