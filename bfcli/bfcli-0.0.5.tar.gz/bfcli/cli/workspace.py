import sys

import click

from bfcli import config
from bfcli.lib.api import API

@click.group()
def workspace():
  pass

@workspace.command()
@click.argument('id')
def delete(id):
  """Deletes the workspace with the given ID."""
  ws = API.Workspace.get(id)
  ws.delete()
  click.echo('Deleted workspace:' + str(ws))


@workspace.command()
@click.argument('id')
def info(id):
  """Prints the workspace with the given ID"""
  ws = API.Workspace.get(id)
  click.echo(str(ws))


@workspace.command()
def list():
  """List all of the currently running workspaces"""
  spaces = API.Workspace.get_all()

  output = '' 

  for ws in spaces:
    output += str(ws)
  
  click.echo(output)


@workspace.command()
@click.argument('platform_type', type=click.Choice(['tensorflow']))
@click.option('--node', '-n', 'node_id', type=int, help='(Required) The ID of the Node to run this workspace on')
@click.option('--name', '-N', help='The name for your workspace. If not given, it will be auto generated')
@click.option('--gpu-ids', '-g', default='', help='A comma-separated list of GPU IDs to attach to the workspace')
def create(platform_type, node_id, name, gpu_ids):
  """Runs a workspace on a node"""

  if not node_id:
    click.echo('You must supply a node ID')
    sys.exit(1)

  if gpu_ids:
    gpus = gpu_ids.split(',')
    ws = API.Workspace.create(platform_type,
                              node_id,
                              config.user.data['user']['defaultGroup'],
                              name,
                              gpus)
  else:
    ws = API.Workspace.create(platform_type,
                              node_id,
                              config.user.data['user']['defaultGroup'],
                              name)

  click.echo(str(ws))

