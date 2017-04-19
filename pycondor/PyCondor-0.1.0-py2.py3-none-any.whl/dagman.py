
import os

from . import base
from .job import Job


class Dagman(base.BaseSubmitNode):

    def __init__(self, name, submit=None, verbose=0):

        super(Dagman, self).__init__(name, submit, verbose)

        self.jobs = []
        self.logger.debug('{} initialized'.format(self.name))

    def __repr__(self):
        nondefaults = ''
        for attr in vars(self):
            if getattr(self, attr) and attr not in ['name', 'jobs', 'logger']:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'Dagman(name={}, n_jobs={}{})'.format(self.name, len(self.jobs), nondefaults)
        return output

    def __iter__(self):
        return iter(self.jobs)

    def _hasjob(self, job):
        return job in self.jobs

    def add_job(self, job):
        # Don't bother adding job if it's already in the jobs list
        if self._hasjob(job):
            return
        if isinstance(job, Job):
            self.jobs.append(job)
        else:
            raise TypeError('add_job() is expecting a Job')
        self.logger.debug(
            'Added Job {} Dagman {}'.format(job.name, self.name))

        return

    def build(self, makedirs=True, fancyname=True):
        for job in self.jobs:
            job._build_from_dag(makedirs, fancyname)

        # Create DAG submit file path
        name = self._get_fancyname() if fancyname else self.name
        submit_file = '{}/{}.submit'.format(self.submit, name)
        self.submit_file = submit_file

        # Write dag submit file
        self.logger.info(
            'Building DAG submission file {}...'.format(self.submit_file))
        with open(submit_file, 'w') as dag:
            for job_index, job in enumerate(self, start=1):
                self.logger.info('Working on Job {} [{} of {}]'.format(
                    job.name, job_index, len(self.jobs)))

                # Pass items in Job args to executable
                for i, arg in enumerate(job):
                    dag.write('JOB {}_p{} '.format(job.name, i) + job.submit_file + '\n')
                    dag.write('VARS {}_p{} '.format(job.name, i) +
                              'ARGS={}\n'.format(base.string_rep(arg, quotes=True)))

                # Add prescript if necessary
                if job._hasprescript():
                    prescript = job.prescript
                    args_str = prescript.args if prescript.args else ''
                    if prescript.apply_each:
                        for i, _ in enumerate(job):
                            dag.write('SCRIPT PRE {}_p{} '.format(job.name, i) + prescript.executable + ' {}\n'.format(args_str))
                    else:
                        dag.write('SCRIPT PRE {}_p0 '.format(job.name) + prescript.executable + ' {}\n'.format(args_str))
                # Add postscript if necessary
                if job._haspostscript():
                    postscript = job.postscript
                    args_str = postscript.args if postscript.args else ''
                    if postscript.apply_each:
                        for i, _ in enumerate(job):
                            dag.write('SCRIPT POST {}_p{} '.format(job.name, i) + postscript.executable + ' {}\n'.format(args_str))
                    else:
                        dag.write('SCRIPT POST {}_p{} '.format(job.name, len(job.args)-1) + postscript.executable + ' {}\n'.format(args_str))

                # Add parent/child information if necessary
                if job._hasparents():
                    parent_string = 'Parent'
                    for parentjob in job.parents:
                        for j, _ in enumerate(parentjob):
                            parent_string += ' {}_p{}'.format(parentjob.name, j)
                    child_string = 'Child'
                    for k, _ in enumerate(job):
                        child_string += ' {}_p{}'.format(job.name, k)
                    dag.write(parent_string + ' ' + child_string + '\n')

        self._built = True
        self.logger.info('DAGMan submission file for {} successfully built!'.format(self.name))

        return

    def submit_dag(self, maxjobs=3000, **kwargs):
        command = 'condor_submit_dag -maxjobs {} {}'.format(
            maxjobs, self.submit_file)
        for option in kwargs:
            command += ' {} {}'.format(option, kwargs[option])
        os.system(command)
        return

    def build_submit(self, makedirs=True, fancyname=True, maxjobs=3000, **kwargs):
        self.build(makedirs, fancyname)
        self.submit_dag(maxjobs, **kwargs)
        return
