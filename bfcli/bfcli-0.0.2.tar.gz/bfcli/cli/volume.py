import sys

import click

from bfcli.lib.api import API

@click.group()
def volume():
  pass


@volume.command()
def list():
  """Lists all volumes available"""
  volumes = API.Volume.get_all()

  output = '' 

  for v in volume:
    output += str(v)
  
  click.echo(output)

@volume.command()
@click.argument('id')
def info(id):
  """Prints info on single volume"""
  volume = vol_lib.info(id)
  output = vol_lib.format_output(volume)
  click.echo(output)


@volume.command()
@click.option('--name', '-n', help='(Required) The name of this volume')
@click.option('--host-path', '-p', help='(Required) The path on the host')
def add(name, host_path):
  """Make a new volume available"""

  try:
    vol = vol_lib.add(name, host_path)
  except Exception as e:
    click.echo(e)
    sys.exit(1)

  click.echo(vol_lib.format_output(vol))
