import json
import os
import sys

import click
import terminaltables

from bfcli.lib.api import API
from bfcli.lib import local_project

def single_project_print(project):
  table_data = [
    table_headers(),
    [project.data.get('id'), project.data.get('name'), project.data.get('createdAt')],
  ]

  table = terminaltables.SingleTable(table_data, title='Project')
  click.echo(table.table)

def table_headers():
  return ['ID', 'Name', 'Created']


def many_projects_print(projects):
  table_data = [table_headers()]

  for _p in projects:
    table_data.append([_p.data.get('id'), _p.data.get('name'), _p.data.get('createdAt')])

  table = terminaltables.SingleTable(table_data, title='Projects')
  click.echo(table.table)


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

  click.echo('Project {} initialized in the current directory'.format(name))


@click.group()
def project():
  pass


@project.command()
def list():
  projects = API.Project.get_all()
  many_projects_print(projects)


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

  single_project_print(proj)
