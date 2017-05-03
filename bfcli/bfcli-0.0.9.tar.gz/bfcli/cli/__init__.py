import click

from bfcli.cli import config, data, job, node, project, volume, workspace
import bfcli.config as c
from bfcli.lib.api import API

@click.group()
def cli():
  pass


cli.add_command(config.version)
cli.add_command(config.config)
cli.add_command(config.login)
cli.add_command(workspace.workspace)
cli.add_command(node.node)
cli.add_command(volume.volume)

if API.is_paas_enabled():
  cli.add_command(data.data)
  cli.add_command(job.info)
  cli.add_command(job.logs)
  cli.add_command(job.run)
  cli.add_command(job.status)
  cli.add_command(job.stop)
  cli.add_command(project.init)
  cli.add_command(project.project)
