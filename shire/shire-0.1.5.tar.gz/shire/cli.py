# -*- coding: utf-8 -*-

import click
import os
import tabulate

from shire.config import Config
from shire.hostler import Hostler
from shire.models import JobEntry, Queue, Limit, Crontab
from shire.manager import ShireManager
from shire.pool import Pool
from shire.pool_starter import PoolStarter
from shire.scribe import Scribe
from shire.whip import Whip
from shire.utils import to_list

__all__ = ['cli']


@click.group()
@click.option('-c', '--config', type=click.Path(), default='shire.cfg')
@click.option('-v', '--verbose', is_flag=True)
@click.pass_context
def cli(ctx, config, verbose):
    config = os.path.realpath(config)
    cfg = Config()
    ctx.obj = ctx.obj or {}
    if os.path.exists(config):
        cfg.load(config)
        ctx.obj['config_path'] = config
    else:
        cfg.make_default()
        ctx.obj['config_path'] = None
    ctx.obj.update({'cfg': cfg, 'verbose': verbose})


@cli.command()
@click.pass_context
def init_db(ctx):
    with ctx.obj['cfg'].with_db():
        for model in (JobEntry, Queue, Limit, Crontab):
            model.create_table(True)


@cli.command()
@click.argument('path', type=click.Path(writable=True))
def make_config(path):
    cfg = Config()
    cfg.make_default()
    cfg.save(path)


@cli.command()
@click.option('-n', '--name', type=click.STRING)
@click.pass_context
def run_pool(ctx, name):
    pool = Pool(config=ctx.obj['cfg'], name=name, verbose=ctx.obj['verbose'])
    pool.run()


@cli.command()
@click.option('-n', '--names', type=click.STRING)
@click.pass_context
def start_pools(ctx, names):
    starter = PoolStarter(config=ctx.obj['cfg'], pools=to_list(names), config_path=ctx.obj['config_path'])
    starter.run()


@cli.command()
@click.pass_context
def run_whip(ctx):
    whip = Whip(config=ctx.obj['cfg'], verbose=ctx.obj['verbose'])
    whip.run()


@cli.command()
@click.pass_context
def run_hostler(ctx):
    hostler = Hostler(config=ctx.obj['cfg'], verbose=ctx.obj['verbose'])
    hostler.run()


@cli.command()
@click.pass_context
def run_scribe(ctx):
    scribe = Scribe(config=ctx.obj['cfg'], verbose=ctx.obj['verbose'])
    scribe.run()


@cli.command()
@click.argument('command')
@click.option('-p', '--pools', type=click.STRING, default=None)
@click.option('-s', '--statuses', type=click.STRING, default=None)
@click.pass_context
def manager(ctx, command, pools, statuses):
    shire_manager = ShireManager(ctx.obj['cfg'])
    kwargs = {}
    if pools is not None:
        kwargs['pools'] = to_list(pools)
    if statuses is not None:
        kwargs['from_statuses'] = to_list(statuses.upper())
    if command == 'get_status':
        click.echo(
            tabulate.tabulate(
                [
                    (x['name'], x['uuid'], x['status'])
                    for x in sorted(shire_manager.run_command(command, **kwargs), key=lambda x: x['name'])
                ],
                headers=['Name', 'UUID', 'Status'], tablefmt='psql'
            )
        )
        return
    shire_manager.run_command(command, **kwargs)


@cli.command()
@click.option('-d', '--days_ago', type=click.INT, default=7)
@click.pass_context
def cleanup_old_jobs(ctx, days_ago):
    with ctx.obj['cfg'].with_db():
        from shire.utils import cleanup_old_jobs
        cleanup_old_jobs(days_ago=days_ago)


@cli.command()
@click.argument('job_id', type=click.INT)
@click.pass_context
def execute_job(ctx, job_id):
    with ctx.obj['cfg'].with_db():
        from shire.utils import execute_job
        result = execute_job(job_id, ctx.obj['cfg'])
        # TODO: Убедиться, что это работает
        return 0 if result else 1


@cli.command()
@click.pass_context
@click.argument('action', type=click.STRING)
@click.option('-p', '--pool', type=click.STRING, default='default')
def crontab(ctx, action, pool):
    from shire.scheduler import CrontabJob
    config = ctx.obj['cfg']
    if action == 'start':
        print('Crontab scheduler started!')
    elif action == 'stop':
        CrontabJob.stop_crontab(config=config)
        print('Crontab scheduler stopped!')
    elif action == 'restart':
        CrontabJob.stop_crontab(config=config)
        CrontabJob.start_crontab(config=config, pool=pool)
        print('Crontab scheduler restarted!')
    elif action == 'clear_jobs':
        CrontabJob.stop_crontab(config=config)
        print('Planned crontab jobs cleared')
    elif action == 'list':
        for cron in CrontabJob.list(config=config):
            print('{}:\t"{}" (last at scheduled {})'.format(
                cron.key, cron.cron_string, cron.last_scheduled if cron.last_scheduled else '--')
            )
            if cron.description:
                print('\t{}'.format(cron.description))
    else:
        print('Wrong action! May be start/stop/restart/clear_jobs/list')


if __name__ == '__main__':
    cli(obj={})
