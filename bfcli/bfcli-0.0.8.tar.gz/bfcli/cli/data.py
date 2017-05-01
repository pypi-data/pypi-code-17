import sys

import click

from bfcli.lib.api import API, me

@click.group()
def data():
  pass


@data.command()
@click.argument('path')
def upload(path):
  def upload_progress(monitor):
    percent = monitor.bytes_read*100/monitor.len
    sys.stdout.write('\rUpload {}% complete'.format(percent))

  user = me()
  API.data.upload(path,
                  '/',
                  group_id=user.data['user']['defaultGroup'],
                  account_id=user.data['account']['id'],
                  callback=upload_progress)
  print()
