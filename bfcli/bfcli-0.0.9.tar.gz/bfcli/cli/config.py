import os
import json
import sys

import bitfusion
import click

import bfcli.config as c
from bfcli.lib.api import API, me, enable_api_decorator

USER_PROMPT = click.option('-u',
                           '--username',
                           prompt='Enter your Bitfusion username',
                           default=lambda: c.conf.get('username', ''))
PASS_PROMPT = click.option('-p', '--password', prompt='Enter your password', hide_input=True)

def _do_login(client, username, password):
  try:
    return client.login(username, password)
  except bitfusion.errors.AuthError as e:
    click.echo(e)
    sys.exit(1)


@click.command()
def version():
  click.echo(c.VERSION)


@click.command()
@click.option('--host',
              prompt='What is the Bitfusion host URL?',
              default=lambda: c.conf.get('host', ''))
@USER_PROMPT
@PASS_PROMPT
def config(host, username, password):
  new_config = {'host': host, 'username': username}

  # Save host URL and username so user won't have to type it again
  c.save_config(**new_config)

  VERIFY_SSL = False if os.environ.get('VERIFY_SSL', '').lower() == 'false' else True

  # Login and get cookies
  client = bitfusion.BFApi(host=new_config['host'], verify=VERIFY_SSL)
  new_config['uid'] = _do_login(client, username, password)

  # Save the cookies

  new_config['cookies'] = client.get_cookies()

  # Validate it all and save
  c.validate_config(new_config)

  c.save_config(**new_config)

  click.echo('Successfully configured Bitfusion CLI\n\n' + \
             '##############################################\n' + \
             '################### CONFIG ###################\n' + \
             '##############################################\n\n' + \
             '{}'.format(json.dumps(new_config, indent=2)))


@click.command()
@USER_PROMPT
@PASS_PROMPT
def login(username, password):
  # Save the username
  c.conf['username'] = username
  c.save_config(**c.conf)

  c.conf['uid'] = _do_login(API, username, password)
  c.conf['cookies'] = API.get_cookies()

  c.save_config(**c.conf)
  click.echo('Successfully logged in!')
