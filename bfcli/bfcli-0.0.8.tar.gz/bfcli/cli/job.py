import os
import sys

import click

from bfcli.lib.api import API, me
from bfcli.lib import local_project

@click.command()
@click.argument('command')
@click.option('--project', '-p', help='The ID of the project to run under')
@click.option('--env', help='(Required) The container for running this command')
@click.option('--gpu', is_flag=True, help='Run this job with a GPU')
@click.option('--cpu', is_flag=True, help='Run this job CPU only')
def run(command, project, env, gpu, cpu):
  def upload_progress(monitor):
    percent = monitor.bytes_read*100/monitor.len
    sys.stdout.write('\rUploading code... {}% complete'.format(percent))

  if not project and not local_project.exists():
    click.echo('You need to be in a directory with a ".flex" file or ' + \
               'specify the project ID to run a job')
    sys.exit(1)

  if gpu and cpu:
    click.echo('You cannot use the flags --cpu and --gpu together')
    sys.exit(1)

  if project:
    proj = API.Project.get(project)
    raise Exception('Cant do this yet')
  else:
    proj = local_project.get()
    code_id = proj.upload_code(os.getcwd(), callback=upload_progress)
    print()

  user = me()
  job = API.Job.create(proj.id, code_id, user.data['user']['defaultGroup'], env, command.split(' '))

  click.echo(str(job))


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
  click.echo(str(job))


@click.command()
@click.argument('id')
def info(id):
  job = API.Job.get(id)
  click.echo(str(job))


@click.command()
def status():
  jobs = API.Job.get_all()
  for j in jobs:
    click.echo(str(j))
