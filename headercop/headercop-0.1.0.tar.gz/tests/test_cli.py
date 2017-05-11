#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BSD License
#
# Copyright (c) 2017, Kaffi LLC.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.


from pathlib import Path
import re
import tempfile

from click.testing import CliRunner
import pytest

from headercop import cli


CONFIG_YAML = '''headercop:
  author: meh
  program: meh
  enforced_extensions:
    - py
'''


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.cmd)
    assert result.exit_code == 0
    assert 'Usage: cmd' in result.output
    help_result = runner.invoke(cli.cmd, ['--help'])
    assert help_result.exit_code == 0
    assert re.search('--help\s*Show this message and exit.', help_result.output) is not None


def test_basic_supported():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('headercop.yaml', 'w'):
            pass
        result = runner.invoke(cli.cmd, ['supported'])
        assert result.exit_code == 0
        assert re.search('Supported filetypes', result.output) is not None


def test_basic_inject():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('tester.py', 'w') as f_out, open('headercop.yaml', 'w') as cfg_out:
            f_out.write('pass')
            cfg_out.write(CONFIG_YAML)
        result = runner.invoke(cli.cmd, ['-vv', 'inject', 'tester.py'])
        print(result.output)
        assert result.exit_code == 0
        with open('tester.py') as f_in:
            assert f_in.read() != 'pass'


def test_basic_check_pass():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('tester.py', 'w') as f_out, open('headercop.yaml', 'w') as cfg_out:
            f_out.write('pass')
            cfg_out.write(CONFIG_YAML)
        runner.invoke(cli.cmd, ['-vv', 'inject', 'tester.py'])
        result = runner.invoke(cli.cmd, ['-vv', 'check', 'tester.py'])
        print(result.output)
        assert result.exit_code == 0


def test_basic_check_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('tester.py', 'w') as f_out, open('headercop.yaml', 'w') as cfg_out:
            f_out.write('pass')
            cfg_out.write(CONFIG_YAML)
        result = runner.invoke(cli.cmd, ['-vv', 'check', 'tester.py'])
        assert result.exit_code == 1
        assert re.search('Missing license header', result.output) is not None


def test_noconfig_die():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.cmd, ['-vvc', 'meh.yaml', 'check', 'tester.py'])
        assert result.exit_code == 1


def test_basic_check_diff_config_pass():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('tester.py', 'w') as f_out, open('oddball_config.yaml', 'w') as cfg_out:
            f_out.write('pass')
            cfg_out.write(CONFIG_YAML)
        runner.invoke(cli.cmd, ['-vvc', 'oddball_config.yaml', 'inject', 'tester.py'])
        result = runner.invoke(cli.cmd, ['-vvc', 'oddball_config.yaml', 'check', 'tester.py'])
        print(result.output)
        assert result.exit_code == 0


def test_checker_gitignored():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('.gitignore', 'w') as gitignore, open('test.py', 'w'), open('headercop.yaml', 'w') as cfg_out:
            cfg_out.write(CONFIG_YAML)
            gitignore.write('test.py\n')
        result = runner.invoke(cli.cmd, ['-vv', 'check', '.'])
        assert result.exit_code == 0


def test_config_scanning():
    with tempfile.TemporaryDirectory() as tempdir:
        config = Path(tempdir, 'headercop.yaml')
        with config.open('w') as cfg_out:
            cfg_out.write(CONFIG_YAML)
        deep_path = Path(tempdir, 'd1', 'd2', 'd3')
        deep_path.mkdir(parents=True)
        cli.scan_for_config(Path(deep_path, 'headercop.yaml'))
        assert cli.CONFIG['headercop']['author'] == 'meh'


def test_config_scanning_fails():
    with tempfile.TemporaryDirectory() as tempdir, pytest.raises(SystemExit):
        cli.scan_for_config(Path(tempdir, 'headercop_doesntexist.yaml'))
