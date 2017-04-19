
import os

from . import base


class Job(base.BaseSubmitNode):

    def __init__(self, name, executable, error=None, log=None, output=None, submit=os.getcwd(), request_memory=None, request_disk=None, request_cpus=None, getenv=True, universe='vanilla', initialdir=None, notification='never', requirements=None, queue=None, extra_lines=None, verbose=0):

        super(Job, self).__init__(name, submit, verbose)

        self.executable = base.string_rep(executable)
        self.error = error
        self.log = log
        self.output = output
        self.request_memory = request_memory
        self.request_disk = request_disk
        self.request_cpus = request_cpus
        self.getenv = getenv
        self.universe = universe
        self.initialdir = initialdir
        self.notification = notification
        self.requirements = requirements
        self.queue = queue
        self.extra_lines = extra_lines
        self.args = []
        self.parents = []
        self.children = []

        self.logger.debug('{} initialized'.format(self.name))

    def __repr__(self):
        nondefaults = ''
        for attr in vars(self):
            if getattr(self, attr) and attr not in ['name', 'executable', 'logger']:
                nondefaults += ', {}={}'.format(attr, getattr(self, attr))
        output = 'Job(name={}, executable={}{})'.format(self.name, os.path.basename(self.executable), nondefaults)
        return output

    def __iter__(self):
        return iter(self.args)

    def add_arg(self, arg):
        arg_str = base.string_rep(arg)
        self.args.append(arg_str)
        self.logger.debug(
            'Added argument \'{}\' to Job {}'.format(arg_str, self.name))
        return

    def add_args(self, args):
        try:
            for arg in args:
                self.add_arg(arg)
        except:
            raise TypeError(
                'add_args() is expecting an iterable of argument strings')

        return

    def _hasparent(self, job):
        return job in self.parents

    def add_parent(self, job):

        # Ensure that job is a Job
        assert isinstance(job, Job), 'job must be of type Job'

        # Don't bother continuing if job is already in the parents list
        if self._hasparent(job):
            return

        # Add job to existing parents
        self.parents.append(job)
        self.logger.debug(
            'Added Job {} as a parent for Job {}'.format(job.name, self.name))

        # Add self Job instance as a child to the new parent job
        job.add_child(self)

        return

    def add_parents(self, job_list):

        # Ensure that job_list is an iterable of type Job
        try:
            for job in job_list:
                self.add_parent(job)
        except:
            raise TypeError('add_parents() is expecting an iterable of Jobs')

        return

    def _haschild(self, job):
        return job in self.children

    def add_child(self, job):
        # Ensure that job is a Job
        assert isinstance(job, Job), 'job must be of type Job'

        # Don't bother continuing if job is already in the children list
        if self._haschild(job):
            return

        # Add job to existing children
        self.children.append(job)
        self.logger.debug(
            'Added Job {} as a child for Job {}'.format(job.name, self.name))
        # Add this Job instance as a parent to the new child job
        job.add_parent(self)

        return

    def add_children(self, jobs):
        # Ensure that jobs is an iterable of type Job
        try:
            for job in jobs:
                self.add_child(job)
        except:
            raise TypeError('add_children() is expecting a list of Jobs')

        return

    def _haschildren(self):
        return bool(self.children)

    def _hasparents(self):
        return bool(self.parents)

    def add_prescript(self, executable, args=None, apply_each=False):
        # Check to see if a prescript for this Job already exists
        if hasattr(self, 'prescript'):
            self.logger.warning('A pre-script for this Job already exists. Replacing it with this one...')
        self.prescript = base.Script(executable=executable, type_='pre',
            args=args, apply_each=apply_each)
        return

    def add_postscript(self, executable, args=None, apply_each=False):
        # Check to see if a postscript for this Job already exists
        if hasattr(self, 'postscript'):
            self.logger.warning('A post-script for this Job already exists. Replacing it with this one...')
        self.postscript = base.Script(executable=executable, type_='post',
            args=args, apply_each=apply_each)
        return

    def _hasprescript(self):
        return hasattr(self, 'prescript')

    def _haspostscript(self):
        return hasattr(self, 'postscript')

    def _has_no_dag_features(self):

        if self._hasparents():
            message = 'Job has parents and must be submitted via Dagman'
            self.logger.error(message)
            raise ValueError(message)
        elif self._haschildren():
            message = 'Job has children and must be submitted via Dagman'
            self.logger.error(message)
            raise ValueError(message)
        elif self._hasprescript() or self._haspostscript():
            message = 'Job has pre/post script and must be submitted via Dagman'
            self.logger.error(message)
            raise ValueError(message)
        else:
            return True

    def _make_submit_script(self, makedirs=True, fancyname=True, indag=False):

        # If not in a Dagman, check that Job does not have features associated
        # with it that are only supported via Dagman
        if not indag:
            assert self._has_no_dag_features()

        # Check that paths/files exist
        if not os.path.exists(self.executable):
            raise IOError(
                'The path {} does not exist...'.format(self.executable))
        for directory in [self.submit, self.log, self.output, self.error]:
            if directory is not None:
                base.checkdir(directory + '/', makedirs)

        name = self._get_fancyname() if fancyname else self.name
        submit_file= '{}/{}.submit'.format(self.submit, name)

        # Start constructing lines to go into job submit file
        lines = []
        submit_attrs = ['universe', 'executable', 'request_memory', 'request_disk', 'request_cpus', 'getenv', 'initialdir', 'notification', 'requirements']
        for attr in submit_attrs:
            if getattr(self, attr) is not None:
                attr_str = base.string_rep(getattr(self, attr))
                lines.append('{} = {}'.format(attr, attr_str))

        # Set up files paths
        for attr in ['log', 'output', 'error']:
            if getattr(self, attr) is not None:
                path = getattr(self, attr)
                # If path has trailing '/', then it it removed. Else, path is unmodified
                path = path.rstrip('/')
                lines.append('{} = {}/{}.{}'.format(attr, path, name, attr))

        # Add any extra lines to submit file, if specified
        if self.extra_lines:
            extra_lines = self.extra_lines
            assert isinstance(extra_lines, (str, list, tuple)), 'extra_lines must be of type str, list, or tuple'
            if isinstance(extra_lines, str):
                lines.append(extra_lines)
            else:
                lines.extend(extra_lines)

        # Add arguments and queue line
        if self.queue:
            assert isinstance(self.queue, int), 'queue must be of type int'
        # If building this submit file for a job that's being managed by DAGMan, just add simple arguments and queue lines
        if indag:
            lines.append('arguments = $(ARGS)')
            lines.append('queue')
        else:
            if self.args and self.queue:
                if len(self.args) > 1:
                    message = 'At this time multiple arguments and queue values are only supported through Dagman'
                    self.logger.error(message)
                    raise NotImplementedError(message)
                else:
                    lines.append('arguments = {}'.format(base.string_rep(self.args, quotes=True)))
                    lines.append('queue {}'.format(self.queue))
            # Any arguments supplied will be taken care of via the queue line
            elif self.args:
                for arg in self.args:
                    lines.append('arguments = {}'.format(base.string_rep(arg)))
                    lines.append('queue')
            elif self.queue:
                lines.append('queue {}'.format(self.queue))
            else:
                lines.append('queue')

        with open(submit_file, 'w') as f:
            f.writelines('\n'.join(lines))

        # Add submit_file data member to job for later use
        self.submit_file = submit_file

        return

    def build(self, makedirs=True, fancyname=True):
        self.logger.info(
            'Building submission file for Job {}...'.format(self.name))
        self._make_submit_script(makedirs, fancyname, indag=False)
        self._built = True
        self.logger.info('Condor submission file for {} successfully built!'.format(self.name))
        return

    def _build_from_dag(self, makedirs=True, fancyname=True):
        self.logger.debug(
            'Building submission file for Job {}...'.format(self.name))
        self._make_submit_script(makedirs, fancyname, indag=True)
        self._built = True
        self.logger.debug('Condor submission file for {} successfully built!'.format(self.name))
        return

    def submit_job(self, **kwargs):
        # Ensure that submit file has been written
        assert self._built, 'build() must be called before submit()'
        # Ensure that there are no parent relationships
        assert len(self.parents) == 0, 'Attempting to submit a Job with the following parents:\n\t{}\nInterjob relationships requires Dagman.'.format(self.parents)
        command = 'condor_submit {}'.format(self.submit_file)
        # Ensure that there are no child relationships
        assert len(self.children) == 0, 'Attempting to submit a Job with the following children:\n\t{}\nInterjob relationships requires Dagman.'.format(self.children)

        if len(self.args) > 20:
            message = 'You are submitting a Job with {} arguments. Consider using a Dagman in the future to help monitor jobs.'.format(len(self.args))
            self.logger.warning(message)

        command = 'condor_submit {}'.format(self.submit_file)
        for option in kwargs:
            command += ' {} {}'.format(option, kwargs[option])
        os.system(command)
        return

    def build_submit(self, makedirs=True, fancyname=True, **kwargs):
        self.build(makedirs, fancyname)
        self.submit_job(**kwargs)
        return
