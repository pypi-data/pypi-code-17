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

  for v in volumes:
    output += str(v)
  
  click.echo(output)

@volume.command()
@click.argument('id')
def info(id):
  """Prints info on single volume"""
  volume = API.volume.get(id)
  click.echo(str(volume))


@volume.command()
@click.option('--name', '-n', help='(Required) The name of this volume')
@click.option('--host-path', '-p', help='(Required) The path on the host')
def add(name, host_path):
  """Make a new volume available"""
  vol = API.Volume.create(name=name, host_path=host_path)
  click.echo(str(vol))
