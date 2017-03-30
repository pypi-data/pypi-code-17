# -*- coding: utf-8 -*-
import glob
from contextlib import contextmanager
from tempfile import NamedTemporaryFile

import click


click.disable_unicode_literals_warning = True


JOBS_DIRECTORY = 'jenkins-jobs'
JOBS_MASK = '*.yml'


@click.group('jenkins-jobs')
def main():
    pass


@main.command()
@click.argument('filenames', nargs=-1)
@click.option('--branch', default='master', help='The job branch.')
def create(filenames, branch):
    """
    Create jobs.
    """
    import os

    click.echo('jenkins-jobs create')

    if not filenames:
        if not os.path.isdir(JOBS_DIRECTORY):
            click.echo('ERROR: {}: Jobs directory not found.'.format(JOBS_DIRECTORY))
            return
        filenames = glob.glob(JOBS_DIRECTORY + '/' + JOBS_MASK)

    for i_filename in filenames:
        click.echo('INFO: {}: Generating job.'.format(i_filename))
        with _temp_file(_template(i_filename, branch=branch)) as oss:
            _jenkins_jobs('update', oss.name)


def _jenkins_jobs(*args):
    from jenkins_jobs.cli.entry import JenkinsJobs

    click.echo('$ jenkins-jobs {}'.format(' '.join(args)))
    jjb = JenkinsJobs(args)
    jjb.execute()


def _template(filename, **kwargs):
    template = open(filename, 'r').read()
    return template.format(**kwargs)


@contextmanager
def _temp_file(content):
    import os
    with NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as oss:
        oss.write(content)
        oss.close()
    yield oss
    os.unlink(oss.name)
