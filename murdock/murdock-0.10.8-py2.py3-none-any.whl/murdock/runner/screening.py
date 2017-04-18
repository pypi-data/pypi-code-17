# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Module `murdock.runner.screening`
---------------------------------

Provides the class `.Screening` used to initialize and run a screening setup.
Multiple `~.runner.docking.Docking` instances are spawned using the class
`.ParallelScreeningWorker`.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import multiprocessing
import os
import signal
import time

import murdock.config
import murdock.runner.docking
from murdock.report import ScreeningReport
from murdock.results import DockingResult, ScreeningResult
from murdock.runner.runner import MurdockInterrupt, MurdockTerminate, Runner


log = logging.getLogger(__name__)


class ScreeningError(Exception):
    pass


class Screening(Runner):
    """A screening class.

    The class is used to sequentially perform docking runs on all
    receptor-ligand sets given as input using the same setup (specified by a
    list of `.docking_steps`.

    """

    def __init__(
            self, label, title, moldata, docking_steps, resdir='.',
            restore=False, resume=False, num_runs=1, docked_suffix='',
            result_suffix='-results', num_procs=1, num_threads=None,
            preprocessing=None, dry=False, report_projects=[], reverse=False,
            notes=None, update_interval=1, debugsampling=False,
            pymolexec=None, pymolscript=None, failmode='continue',
            draw_resscore_charts=False, draw_resdist_charts=False,
            outfmts=None):
        super(Screening, self).__init__(
            moldata, resdir=resdir, restore=restore, resume=resume,
            result_suffix=result_suffix)
        #: `.ParallelScreeningWorker` instances (one per docking)
        self.workers = []
        #: number of parallel processes used
        self.num_procs = num_procs
        #: idle time before results are updated (optionally Sphinx-built)
        self.update_interval = update_interval
        #: `.runner.docking.Docking` arguments
        self.dkwargs = {
            'docking_steps': docking_steps, 'docked_suffix': docked_suffix,
            'result_suffix': result_suffix, 'restore': restore,
            'resume': self.resume, 'num_runs': num_runs,
            'preprocessing': preprocessing, 'dry': dry,
            'report_projects': report_projects, 'screening_pid': os.getpid(),
            'debugsampling': debugsampling, 'pymolexec': pymolexec,
            'pymolscript': pymolscript, 'num_threads': num_threads,
            'failmode': failmode, 'draw_resscore_charts': draw_resscore_charts,
            'draw_resdist_charts': draw_resdist_charts, 'outfmts': outfmts}
        #: screening result container
        self.result = ScreeningResult(label=label, notes=notes, title=title)
        #: formatted report
        self.report = ScreeningReport(
            backends=[_p.get_document(label) for _p in report_projects],
            resdir=self.resdir, result=self.result, pymolexec=pymolexec,
            pymolscript=pymolscript, num_threads=num_threads,
            num_runs=num_runs)
        if reverse:
            self.moldata = moldata[::-1]
        global log
        log = self._create_logger()

    def update(self):
        changed = False
        for worker in self.workers:
            if worker.update():
                log.info(
                    ' Docking `%s` changed status to `%s`.', worker.title,
                    worker.status)
                changed = True
        if len(self.result.dress) != len(self.workers) or changed:
            self.result.clear_dress()
            for worker in self.workers:
                self.result.add_dres(worker.result)
        return changed

    def _run(self):
        if self.resume:
            log.info('Resume screening `%s`.', self.title)
        else:
            log.info('Start screening `%s`.', self.title)
        if self.resume or self.restore:
            try:
                self.result.load_json(self.json_filepath)
            except ValueError as exc:
                log.warning(
                    'Can not parse screening result file `%s`: %s.',
                    self.json_filepath, str(exc))
            except IOError as exc:
                log.info(
                    'No existing screening result file `%s` found.',
                    self.json_filepath)
            else:
                log.info(
                    'Timing information from existing result file `%s` will '
                    'be used.', self.json_filepath)
        self.update()
        self._write_results()
        waiting = self.workers[:]
        while waiting or self._workers_running():
            try:
                while (
                        len(self._workers_running()) < self.num_procs and
                        len(waiting) > 0):
                    waiting.pop(0).start()
                if self.update():
                    self._write_results()
                time.sleep(self.update_interval)
            except MurdockInterrupt:
                for w in self.workers:
                    w.stop(signum=signal.SIGINT, wait=False)
                raise
            except MurdockTerminate:
                for w in self.workers:
                    w.stop(signum=signal.SIGTERM, wait=False)
                raise
        return True

    def _setup(self):
        """Set up screening, fill `.workers`.
        """
        for dockdat in self.moldata:
            dkwargs = self.dkwargs.copy()
            dkwargs['label'] = dockdat['label']
            dkwargs['title'] = dockdat['title']
            dkwargs['moldata'] = {
                'receptor': dockdat['receptor'], 'ligands': dockdat['ligands']}
            dkwargs['notes'] = dockdat['notes'] if 'notes' in dockdat else None
            dkwargs['resdir'] = os.path.join(
                self.resdir, 'dockings', dockdat['label'])
            w = ParallelScreeningWorker(sres=self.result, dkwargs=dkwargs)
            self.workers.append(w)
        return True

    def _shutdown(self, quick=False):
        """Do final chores before the sun goes down.
        """
        try:
            self.result.timing.end.set_current()
            if quick:
                log.info('Shut down (quick).')
                for worker in self.workers:
                    worker.stop(
                        signum=signal.SIGTERM, timeout=1, kill=True)
                    if worker.result.running:
                        worker.result.set_status('aborted')
                self.update_full = False
            else:
                log.info('Shut down.')
                for worker in self.workers:
                    worker.stop()
                self.update()
                self.update_full = True
            self._write_results()
        except (MurdockInterrupt, MurdockTerminate):
            return self._shutdown(quick=True)
        for worker in self.workers:
            worker.stop()
        log.info('%s done.', self.__class__.__name__)
        return True

    def _workers_running(self):
        return [_w for _w in self.workers if _w.alive]


class ParallelScreeningWorker(object):

    def __init__(self, sres, dkwargs):
        self.dkwargs = dkwargs
        self.process = None
        self.pid = None
        self.result = DockingResult(sres=sres)
        self.result.from_json(dkwargs)
        self.resdir = self.dkwargs['resdir']

    @property
    def alive(self):
        return self.pid is not None and self.process.is_alive()

    @property
    def label(self):
        return self.result.label

    @property
    def log_filename(self):
        return '%s.log' % self.label

    @property
    def log_filepath(self):
        return os.path.join(self.resdir, self.log_filename)

    @property
    def json_filepath(self):
        return os.path.join(self.resdir, '%s%s.json' % (
            self.label, self.dkwargs['result_suffix']))

    @property
    def status(self):
        return self.result.status

    @property
    def title(self):
        return self.result.title

    def start(self):
        self.process = multiprocessing.Process(
            target=_mp_run_docking, args=(self.dkwargs, ))
        log.setLevel(logging.WARNING)
        self.process.start()
        log.setLevel(logging.INFO)
        self.pid = self.process.pid
        log.info('Start docking `%s` [%d].', self.title, self.pid)
        return True

    def stop(self, signum=None, wait=True, timeout=None, kill=False):
        if not self.alive:
            return True
        if signum is not None:
            os.kill(self.pid, signum)
        if wait:
            self.process.join(timeout=timeout)
            if self.process.is_alive() and kill:
                log.debug(
                    'Docking process %d (`%s`) still alive after `%d` second '
                    'timeout. Send kill signal.', self.pid, self.title,
                    timeout)
                os.kill(self.pid, signal.SIGKILL)
                self.result.set_status('KILLED')
        return True

    def update(self):
        if self.status == 'KILLED':
            return False
        old_status = self.status
        alive = self.alive
        try:
            self.result.load_json(self.json_filepath, done=False)
        except (IOError, ValueError):
            return False
        if self.pid is None:
            self.result.set_status('not started')
        elif alive and not self.result.running:
            self.result.set_status(old_status)
        elif not alive and self.result.running:
            log.fatal(
                'Docking process %d (`%s`) has been found dead with status '
                '`%s`. The process was probably killed from the outside.',
                self.pid, self.title, self.status)
            self.result.set_status('KILLED')
            return True
        if self.status == old_status:
            return False
        if self.status == 'CRASHED':
            log.fatal(
                'Docking `%s` crashed. Check docking log file `%s`.',
                self.title, self.log_filepath)
        return True


class ConfigDeclaration(murdock.runner.docking.ConfigDeclaration):

    def screening(self):
        """Configuration options for a screening setup:

            - "title":
                project title used in formatted results `(dtype=str,
                required=False)`

            - "label":
                project label used in result filenames (no special characters)
                `(dtype=str, required=False)`

            - "user":
                program user / scientist responsible for the experiment
                `(dtype=str, required=False)`

            - "number_of_runs":
                number of independent docking runs performed for each docking
                `(dtype=int, default=1)`

            - "fail-mode":
                what to do if a single docking run fails
                    * `abort` -> abort the docking (skip remaining runs)
                    * `continue` -> continue with the next run (default)
                    * `repeat` -> repeat the failed run

            - "preprocessing":
                options for the
                `~.runner.docking.ConfigDeclaration.preprocessing` of molecular
                structures before a docking run `(dtype=dict, required=False)`

            - "steps":
                list of docking `~.runner.docking.ConfigDeclaration.steps` to
                be performed consecutively within a docking run
                `(dtype=list, required=True)`

            - "description":
                a short description of the screening setup `(dtype=str,
                required=False)`

            - "input_data":
                list of (molecular)
                `~.runner.docking.ConfigDeclaration.input_data` for each
                docking `(dtype=list, required=True)`

        """
        Option = murdock.config.ConfigOption
        opt = self.get_default_options()
        opt.append(Option(
            name='title', dtype=Option.string, description='project title '
            'used in formatted results', required=False))
        opt.append(Option(
            name='label', dtype=Option.string, description='project label '
            'used in result filenames', required=False))
        opt.append(Option(
            name='user', dtype=Option.string, description='program user / '
            'scientist responsible for the experiment', required=False))
        opt.append(Option(
            name='input_data', dtype=list, description='list of (molecular) '
            'input data to be included in the screening'))
        opt.append(Option(
            name='number_of_runs', dtype=Option.int_gt_zero, default=1,
            description='number of independent docking runs per input '
            'complex'))
        opt.append(Option(
            name='fail-mode', dtype=Option.string, description='what to do if '
            'a single docking run fails', default='continue',
            choices=('abort', 'continue', 'repeat')))
        opt.append(Option(
            name='preprocessing', dtype=dict, required=False,
            description='information on python function used to prepare or '
            'correct input structures'))
        opt.append(Option(
            name='steps', dtype=list, description='main parameter section '
            'defining docking workflow'))
        opt.append(Option(
            name='description', dtype=Option.string, description='short '
            'description of the screening setup', required=False))
        return opt

    def input_data(self):
        """Configuration options for external input data:

            - "title":
                title used in formatted results `(dtype=str, required=True)`

            - "label":
                label used in result filenames (no special characters)
                `(dtype=str, required=False)`

            - "receptor":
                options for the input
                `~.runner.docking.ConfigDeclaration.receptor`, i.e. the docking
                target `(dtype=dict, required=True)`

            - "ligands":
                list of input `~.runner.docking.ConfigDeclaration.ligands`,
                which are docked onto the receptor simultaneously
                `(dtype=list, required=True)`

            - "tags":
                a list of tag strings for classification, sorting, etc. of
                input and output data `(dtype=str, required=False)`

        """
        Option = murdock.config.ConfigOption
        opt = self.get_default_options()
        opt.append(Option(
            name='receptor', dtype=dict, description='dictionary containing '
            'receptor information'))
        opt.append(Option(
            name='ligands', dtype=list, description='list containing ligand '
            'information'))
        opt.append(Option(
            name='label', dtype=Option.string, description='label used in '
            'result filenames', required=False))
        opt.append(Option(
            name='title', dtype=Option.string, description='title used in '
            'formatted results'))
        opt.append(Option(
            name='tags', dtype=list, description='list of tag strings',
            required=False, validate=False))
        return opt


def _mp_run_docking(dkwargs):
    for p in dkwargs['report_projects']:
        p.build_exec = None
    docking = murdock.runner.docking.Docking(**dkwargs)
    try:
        docking.run()
    finally:
        logging.shutdown()
