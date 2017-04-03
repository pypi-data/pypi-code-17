"""doxycore.py contains the core functionality for doxybuild."""

from collections import namedtuple
import logging
import os
import shutil
import subprocess

"""Create a directory if it does not already exist."""
def create_dir(path):
    # TODO should really check if `path` is an ordinary file and raise an Exception
    if not os.path.isdir(path):
        logging.info('Creating directory {}'.format(path))
        os.makedirs(path)

"""Return texmf dir. (*nix specific for now)."""
def texmf_dir():
    return os.path.join(
        os.path.expanduser('~'),
        'texmf',
    )

"""Copy necessary style files into the texmf directory."""
def setup_texmf(sty_files):
    logging.info('texmf dir is {}'.format(texmf_dir()))
    logging.info('Copying style files:')
    for sty_file in sty_files:
        logging.info('*  {}'.format(sty_file))
        sty_name = os.path.splitext(os.path.basename(sty_file))[0]
        target_dir = os.path.join(texmf_dir(), sty_name)
        create_dir(target_dir)
        shutil.copy2(sty_file, target_dir)

"""Return unique job name for file from directory structure."""
def job_name(source_file, source_dir):
    relative_path = os.path.relpath(source_file, source_dir)
    relative_path = os.path.splitext(relative_path)[0]
    return '_'.join(relative_path.split(os.path.sep))

"""Encapsulates a source file and its unique job name."""
Job = namedtuple('Job', 'source_file name')

"""Get list of files to compile.

Arguments:
    source_dir      The root directory in which to search (recursively) for TeX
                    files to compile
    tex_dir         The subdirectory name for tex files belonging to multi file
                    projects (such subdirectories are ignored when searching)
    extensions      The extensions of files to compile

Returns:
    A list of TeX files to be compiled, paired with unique job names generated
    from the directory structure. Filenames returned are absolute.
"""
def get_jobs(source_dir, exclude_dirs, extensions):
    logging.info(' * Search for source files ({exts}) in {source}.'.format(
        source=os.path.abspath(source_dir),
        exts=','.join(extensions),
    ))
    logging.info('   Ignoring subdirectories: {}'.format(','.join(exclude_dirs)))

    jobs = []
    for dirname, subdirs, filenames in os.walk(source_dir):
        for exclude_dir in exclude_dirs:
            if exclude_dir in subdirs: subdirs.remove(exclude_dir)
        for filename in filenames:
            # [1:] removes the preceding '.' on the extension
            if os.path.splitext(filename)[1][1:] in extensions:
                source_file = os.path.join(dirname, filename)
                jobs.append(Job(source_file, job_name(source_file, source_dir)))
                logging.info('    * File: {}'.format(source_file))
                logging.info('      Job name: {}'.format(job_name(source_file, source_dir)))
    return jobs

"""Encapsulates a program such as latexmk along with necessary configuration."""
class Builder:
    def __init__(
        self,
        build_dir,
        command='latexmk',
        default_options=['-pdf', '-cd', '-interaction=nonstopmode'],
        build_dir_opt='-output-directory=',
        job_name_opt='-jobname=',
        log_file=None,
        ):
        self.command = command
        self.options = default_options
        self.build_dir = build_dir
        self.build_dir_opt = build_dir_opt
        self.job_name_opt = job_name_opt

        create_dir(self.build_dir)
        logging.info('Build dir: {}'.format(self.build_dir))

        if log_file:
            create_dir(os.path.dirname(log_file))
            logging.info('Latexmk log file: {}'.format(log_file))
            self.log_file = open(log_file, mode='w')
        else:
            self.log_file=os.devnull

    """Construct the shell command to use to build a file."""
    def build_command(self, job, extra_options=[], disable_default_options=False):
        command = [
            self.command,
            '{build_dir_opt}{build_dir}'.format(
                build_dir_opt=self.build_dir_opt,
                build_dir=self.build_dir),
            '{job_name_opt}{job_name}'.format(
                job_name_opt=self.job_name_opt,
                job_name=job.name)
            ]
        command += extra_options
        if not disable_default_options:
            command += self.options
        command += [job.source_file, ]

        return command

    """Build a job by executing the builder (e.g. latexmk)."""
    def build_job(self, job, extra_options=[], disable_default_options=False):
        logging.info(' * Building job: {}'.format(job.name))
        logging.info('   Source file: {}'.format(job.source_file))

        command = self.build_command(
            job=job,
            extra_options=extra_options,
            disable_default_options=disable_default_options
            )
        logging.info(' '.join(command))
        subprocess.call(command, stdout=self.log_file, stderr=self.log_file)

    """Copy compiled file to final destination."""
    def install_job(self, job, dest_dir):
        create_dir(dest_dir)

        source = os.path.join(self.build_dir, job.name+'.pdf')
        dest = os.path.join(dest_dir, job.name+'.pdf')

        logging.info(' * Copying job: {}'.format(job.name))
        logging.info('   Destination: {}'.format(source, dest))
        shutil.copy2(source, dest)
