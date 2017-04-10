import sys

import click

import bitfusion

from bfcli import config

API = bitfusion.BFApi(host=config.conf.get('host'), cookies=config.conf.get('cookies'))

# Try to set the user in config
try:
  config.user = API.User.get(config.conf['uid'])
except:
  pass


def api_error_decorator(handler):
  def api_error_wrapper(*args, **kwargs):
    try:
      return handler(*args, **kwargs)
    except bitfusion.errors.BitfusionError as e:
      click.echo(e)
      sys.exit(1)

  return api_error_wrapper


def enable_api_decorator():
  API._session._handle_response = api_error_decorator(
    API._session._handle_response
  )
