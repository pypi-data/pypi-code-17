import os
import sys

import click
import terminaltables

from bfcli.lib.api import API, me
from bfcli.lib import local_project


def get_duration_string(duration):
  m, s = divmod(duration, 60)
  h, m = divmod(m, 60)
  d, h = divmod(h, 24)

  duration_str = '{} seconds'.format(s)
  if m:
    duration_str = '{} minutes '.format(m) + duration_str
  if h:
    duration_str = '{} hours '.format(h) + duration_str
  if d:
    duration_str = '{} days '.format(d) + duration_str

  return duration_str


def get_resource_string(resources):
  if not resources:
    return ''

  tran_r_array = [_r.get('type', '') + '=' + str(_r.get('value')) for _r in resources]
  return ','.join(tran_r_array)


def print_single_job(job):
  table_data = [
    ['ID', job.data.get('id')],
    ['Project', job.data.get('project', {}).get('name')],
    ['Created', job.data.get('createdAt')],
    ['Duration', get_duration_string(job.data.get('duration', 0))],
    ['Resources', get_resource_string(job.data.get('resources'))],
  ]

  table = terminaltables.SingleTable(table_data, title='Run')
  table.inner_row_border = True

  click.echo(table.table)



def print_job_list(jobs):
  headings = ['ID', 'Project', 'Created', 'Duration', 'Resources']
  table_data = [headings]

  for _j in jobs:

    resource_str = get_resource_string(_j.data.get('resources'))
    durstr = get_duration_string(_j.data.get('duration', 0))

    table_data.append([
      _j.data.get('id'),
      _j.data.get('project', {}).get('name'),
      _j.data.get('createdAt'),
      durstr,
      resource_str
    ])

  table = terminaltables.SingleTable(table_data, title='Runs')
  click.echo(table.table)


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--project', '-p', help='The ID of the project to run under')
@click.option('--env', help='(Required) The container for running this command')
@click.option('--gpu', is_flag=True, help='Run this job with a GPU')
@click.option('--cpu', is_flag=True, help='Run this job CPU only')
@click.option('--data', '-d', help='CSV string of data IDs')
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def run(command, project, env, gpu, cpu, data):
  if gpu and cpu:
    click.echo('You cannot use the flags --cpu and --gpu together')
    sys.exit(1)
  elif gpu:
    resources = [{'type': 'gpu', 'value': 1}]
  else:
    resources = []


  if not project and not local_project.exists():
    click.echo('You need to be in a directory with a ".flex" file or ' + \
               'specify the project ID to run a job')
    sys.exit(1)

  if project:
    proj = API.Project.get(project)
    raise Exception('Cant do this yet')
  else:
    proj = local_project.get()
    click.echo('Uploading local project...')
    code_id = proj.upload_code(os.getcwd())
    click.echo('Uploading complete! Starting job...')

  user = me()
  data = ','.split(data) if data else []

  job = API.Job.create(
    proj.id,
    code_id,
    user.data['user']['defaultGroup'],
    env,
    data,
    resources,
    list(command),
  )

  print_single_job(job)


@click.command()
@click.argument('id')
@click.option('--tail', '-t', is_flag=True, help='Tail the job output')
def logs(id, tail):
  job = API.Job.get(id)
  click.echo(job.logs())


@click.command()
@click.argument('id')
def stop(id):
  job = API.Job.get(id)
  job.delete()
  job.reload()
  print_single_job(job)


@click.command()
@click.argument('id')
def info(id):
  job = API.Job.get(id)
  print_single_job(job)


@click.command()
def status():
  jobs = API.Job.get_all()
  print_job_list(jobs)
