import json
import logging

import click

from .. import __version__ as VERSION
from .. import set_logging
from ..api import build as incubator_build
from ..core.config import ImageConfig
from ..core.constants import APP_NAME, CONFIG_NAME
from ..core.output import TITLE
from ..core.utils import get_list_from_tuple_or_string
from .types import KEY_VALUE


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("{}-{}".format(APP_NAME, VERSION))
    ctx.exit()


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-V', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli():
    """
    Incubator is an alternative image builder for docker containers.
    """
    pass


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('path', type=click.Path(exists=True,
                                        file_okay=False,
                                        dir_okay=True,
                                        readable=True))
@click.option('--build-arg', multiple=True, type=KEY_VALUE, help="Set build-time variables (default [])")
@click.option('--cpu-shares', '-c', type=click.INT, help="CPU shares (relative weight).")
@click.option('--config', '-g', type=click.File(), multiple=True, help="File with config.")
@click.option('--context-file-limit', type=click.INT, help="Limit for in-memory context. Default is 0=unlimited.")
@click.option('--cpuset-cpus', type=click.STRING, help="CPUs in which to allow execution (0-3, 0,1)")
@click.option('--file', '-f', type=click.Path(exists=False), help="Name of the Dockerfile.")
@click.option('--force-rm', is_flag=True, help="Always remove intermediate containers")
@click.option('--label', '-l', multiple=True, type=click.STRING, help="Set metadata for an image (default [])")
@click.option('--memory', '-m', type=click.STRING, help="Memory limit.")
@click.option('--memory-swap', type=click.STRING,
              help="Swap limit equal to memory plus swap: '-1' to enable unlimited swap.")
@click.option('--no-cache', is_flag=True, help=" Do not use cache when building the image.")
@click.option('--pull', is_flag=True, help="Always attempt to pull a newer version of the image")
@click.option('--quiet', '-q', is_flag=True, help="Only display ID.")
@click.option('--rm', type=click.BOOL, help="Remove intermediate containers after a successful build (default true)")
@click.option('--tag', '-t', multiple=True, type=click.STRING, help="Tag for final image.")
@click.option('--test-config', is_flag=True, help="Print only given configuration and exit.")
@click.option('--verbose', is_flag=True, help="Be verbose.")
@click.option('--volume', '-v', type=click.STRING, help="Set build-time bind mounts (default [])")
def build(path, build_arg, cpu_shares, config,
          context_file_limit,
          cpuset_cpus, file, force_rm,
          label, memory, memory_swap,
          no_cache, pull, quiet, rm,
          tag, test_config, verbose, volume):
    """
    Alternative to docker build command.

    Build process can be controlled  with config file.
    """
    if verbose:
        set_logging(level=logging.DEBUG, add_handler=(not quiet))
    else:
        set_logging(level=logging.INFO, add_handler=(not quiet))

    loaded_configs = ImageConfig.load_config_from_default_files()

    if config:
        for c in config:
            try:
                new_config = json.loads(c.read())
                new_config.setdefault(CONFIG_NAME, c.name)
                loaded_configs.append(new_config)
            except Exception as ex:
                msg = "Failed to load config from file '{}'\n{}".format(c.name, ex)
                raise click.ClickException(message=msg)

    volume = get_list_from_tuple_or_string(value=volume)
    tag = get_list_from_tuple_or_string(value=tag)
    label = get_list_from_tuple_or_string(value=label)
    buildargs = dict(build_arg)

    limits = {
        'memory': memory,
        'memswap': memory_swap,
        'cpushares': cpu_shares,
        'cpusetcpus': cpuset_cpus
    }

    if test_config:
        click.echo("path: {}\n"
                   "buildargs: {}\n"
                   "cpu_shares: {}\n"
                   "config: {}\n"
                   "context_file_limit: {}\n"
                   "cpuset_cpus: {}\n"
                   "file: {}\n"
                   "force_rm: {}\n"
                   "labels: {}\n"
                   "memory: {}\n"
                   "memory_swap: {}\n"
                   "no_cache: {}\n"
                   "pull: {}\n"
                   "quiet: {}\n"
                   "rm: {}\n"
                   "tags: {}\n"
                   "test_config: {}\n"
                   "verbose: {}\n"
                   "volumes: {}\n"
                   .format(path, buildargs, cpu_shares,
                           config, context_file_limit, cpuset_cpus, file,
                           force_rm, label, memory, memory_swap,
                           no_cache, pull, quiet, rm,
                           tag, test_config, verbose,
                           volume))

        click.echo("loaded configs:\n{}".format(str(loaded_configs)))
        click.echo("merged configs:\n{}".format(ImageConfig.merge_configs(loaded_configs).config))
        return

    try:
        image = incubator_build(buildargs=buildargs,
                                path=path,
                                config=loaded_configs,
                                pull=pull,
                                dockerfile=file,
                                container_limits=limits,
                                rm=rm,
                                forcerm=force_rm,
                                volumes=volume,
                                tag=tag,
                                labels=label)
    except Exception as ex:
        msg = "There occurred an error during building an image:\n{}".format(ex)
        raise click.ClickException(message=msg)

    output = str(image.id)
    if not quiet:
        output = TITLE.format("") + "ID:{}\n".format(output) + TITLE.format("")

    click.echo(output)


cli.add_command(build)

if __name__ == '__main__':
    cli()
