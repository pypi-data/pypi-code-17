import json
import os
import sys

import click

from bfcli.lib.api import API
from bfcli.lib import local_project

@click.command()
@click.argument('name')
def init(name):
  if local_project.exists():
    error = 'There is a {} file in this directory.\n' + \
            'Delete the file and rerun init if you want to make a new project'
    click.echo(error.format(local_project.PROJECT_FILE))
    sys.exit(1)

  project = None
  p_file = local_project.path()

  try:
    with open(p_file, 'w') as _f:
      project = API.Project.create(name)
      _f.write(json.dumps(project.data, indent=2))
  except Exception as e:
    os.remove(p_file)
    click.echo('Failed to create the project')
    sys.exit(1)

  click.echo(str(project))


@click.group()
def project():
  pass


@project.command()
def list():
  projects = API.Project.get_all()
  for p in projects:
    click.echo(str(p))


@project.command()
@click.option('--id', help='The project ID')
def info(id):
  if not id and not local_project.exists():
    click.echo('You need to be in a directory with a ".flex" file or ' + \
               'specify the project ID to get project info')
    sys.exit(1)

  if id:
    proj = API.Project.get(id)
  else:
    proj = local_project.get()

  click.echo(str(proj))
