import sys

import click

from bfcli import config
from bfcli.lib.api import API, me

WS_TYPES = ['tensorflow']

if API:
  try:
    _images = API.Workspace.images()
    WS_TYPES = [_i['type'] for _i in _images]
  except:
    pass

@click.group()
def workspace():
  config.ensure_config_is_valid()


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
@click.argument('platform_type', type=click.Choice(WS_TYPES))
@click.option('--node', '-n', 'node_id', type=int, help='(Required) The ID of the Node to run this workspace on')
@click.option('--name', '-N', help='The name for your workspace. If not given, it will be auto generated')
@click.option('--gpu-ids', '-g', default='', help='A comma-separated list of GPU IDs to attach to the workspace')
def create(platform_type, node_id, name, gpu_ids):
  """Runs a workspace on a node"""

  if not node_id:
    click.echo('You must supply a node ID')
    sys.exit(1)

  meta = API.Workspace.image_metadata(platform_type)
  options = {}
  for param in meta.get('parameters', []):
    if 'user_input' in param:
      field_prompt = param.get('display', param['key'])
      val = click.prompt('Enter {}'.format(field_prompt))
      options[param['key']] = val


  if gpu_ids:
    gpus = gpu_ids.split(',')
    ws = API.Workspace.create(platform_type,
                              node_id,
                              me().data['user']['defaultGroup'],
                              name,
                              gpus,
                              options)
  else:
    ws = API.Workspace.create(platform_type,
                              node_id,
                              me().data['user']['defaultGroup'],
                              name,
                              options=options)

  click.echo(str(ws))

