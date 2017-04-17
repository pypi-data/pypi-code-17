# -*- coding: utf-8 -*-

"""Serve a takumi thrift service.

Usage:
    takumi serve [<gunicorn_args>...]
"""

import sys


def run(args):
    from ..runner import AppRunner
    from takumi_ext import ext
    sys.argv = ['takumi serve'] + args
    # Delegate to gunicorn
    runner = AppRunner()
    app_runner_ext = ext['app-runner']

    if app_runner_ext:
        runner_ext = app_runner_ext(runner)
        runner.cfg.set('when_ready', lambda x: runner_ext.on_start())
        runner.cfg.set('on_exit', lambda x: runner_ext.on_exit())
    runner.run()
