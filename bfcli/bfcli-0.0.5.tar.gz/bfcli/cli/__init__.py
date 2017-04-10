import sys
import json

import bitfusion
import click

from bfcli.cli import node, workspace, volume
import bfcli.config as c
from bfcli.lib.api import API, enable_api_decorator

USER_PROMPT = click.option('-u',
                           '--username',
                           prompt='Enter your Bitfusion username',
                           default=lambda: c.conf.get('username', ''))
PASS_PROMPT = click.option('-p', '--password', prompt='Enter your password', hide_input=True)

@click.group()
def cli():
  try:
    c.validate_config()

    if sys.argv[1] != 'config' and sys.argv[1] != 'login':
      enable_api_decorator()
  except Exception as e:
    if sys.argv[1] != 'config':
      click.echo('Bitfusion CLI is not configured properly. Please run `bf config`')
      sys.exit(1)


@cli.command()
@click.option('--host',
              prompt='What is the Bitfusion host URL?',
              default=lambda: c.conf.get('host', ''))
@USER_PROMPT
@PASS_PROMPT
def config(host, username, password):
  new_config = {'host': host, 'username': username}

  # Save host URL and username so user won't have to type it again
  c.save_config(**new_config)

  # Login and get cookies
  client = bitfusion.BFApi(host=new_config['host'])
  try:
    client.login(username, password)
  except Exception as e:
    click.echo('Failed to login.')
    sys.exit(1)

  # Save the cookies
  new_config['cookies'] = client.get_cookies()
  new_config['uid'] = client.me.data['user']['id']

  # Validate it all and save
  c.validate_config(new_config)

  c.save_config(**new_config)

  click.echo('Successfully configured Bitfusion CLI\n\n' + \
             '##############################################\n' + \
             '################### CONFIG ###################\n' + \
             '##############################################\n\n' + \
             '{}'.format(json.dumps(new_config, indent=2)))


@cli.command()
@USER_PROMPT
@PASS_PROMPT
def login(username, password):
  # Save the username
  c.conf['username'] = username
  c.save_config(**c.conf)

  # Login and get cookies
  try:
    API.login(username, password)
  except Exception as e:
    click.echo('Failed to login.')
    sys.exit(1)

  c.conf['cookies'] = API.get_cookies()
  c.conf['uid'] = API.me.data['user']['id']

  c.save_config(**c.conf)


cli.add_command(workspace.workspace)
cli.add_command(node.node)
cli.add_command(volume.volume)
