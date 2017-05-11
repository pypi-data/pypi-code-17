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


import datetime
import io
from pathlib import Path
import tempfile

import pytest

from headercop import headercop


@pytest.fixture
def base_file():
    with tempfile.TemporaryDirectory() as f_out:
        tester_path = Path(f_out, 'tester.sh')
        with tester_path.open('w') as f_out:
            f_out.write('#/bin/sh\n')
        yield tester_path


@pytest.fixture
def shell_file():
    with tempfile.TemporaryDirectory() as f_out:
        tester_path = Path(f_out, 'tester.sh')
        with tester_path.open('w') as f_out:
            f_out.write('#/bin/sh\nsome text\n')
        yield tester_path


def test_checkfile_emptyfile():
    txt = io.StringIO('')
    assert headercop.check_file(txt, 'no license', 1) is False


def test_checkfile_nolicense():
    txt = io.StringIO('meh')
    with pytest.raises(ValueError):
        headercop.check_file(txt, '', 1) is False


def test_checkfile_nomatch():
    txt = io.StringIO('no ticket')
    assert headercop.check_file(txt, 'tickets please', 1) is False


def test_checkfile_partialmatch():
    txt = io.StringIO('no ticket')
    assert headercop.check_file(txt, 'no ticket\nno seriously no ticket', 1) is False


def test_checkfile_licensechanged_partialmatch():
    txt = io.StringIO('no ticket\nSome year')
    assert headercop.check_file(txt, 'no ticket\nDifferent year', 1) is False


def test_checkfile_goodmatch_wholefile():
    license = 'no ticket\nno seriously no ticket'
    txt = io.StringIO(license)
    assert headercop.check_file(txt, license, 1) is True


def test_checkfile_goodmatch():
    license = 'no ticket\nno seriously no ticket'
    txt = io.StringIO('{}\nwith a bit more text on the end'.format(license))
    assert headercop.check_file(txt, license, 1) is True


def test_checkfile_goodmatch_trailingreturns():
    license = 'no ticket\nno seriously no ticket\n\n'
    txt = io.StringIO('with a bit more text on the end\n{}\n\n'.format(license))
    assert headercop.check_file(txt, license, 1) is True


def test_inject_header_previousfailed():
    with pytest.raises(ValueError), tempfile.NamedTemporaryFile() as f_in:
        swap_file = Path(f_in.name)
        swap_file = Path(swap_file.parent, '.{}.headercop.swp'.format(swap_file.name))
        with swap_file.open('w'):
            headercop.inject_header(Path(f_in.name), 'no license', 0, '.*')


def test_inject_header_simple():
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir, 'meh.txt')
        with test_file.open('w') as f_out:
            f_out.write('original text\n')
        headercop.inject_header(test_file, 'test\n', 0, '.*')
        with test_file.open() as f_in:
            assert f_in.read() == 'test\noriginal text\n'


def test_inject_header_skipwholefile():
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir, 'meh.txt')
        with test_file.open('w') as f_out:
            f_out.write('original text\n')
        headercop.inject_header(test_file, 'test\n', 1, '.*')
        with test_file.open() as f_in:
            assert f_in.read() == 'original text\ntest\n'


def test_inject_header_skip():
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir, 'meh.txt')
        with test_file.open('w') as f_out:
            f_out.write('original text\nextra text\n')
        headercop.inject_header(test_file, 'test\n', 1, '.*')
        with test_file.open() as f_in:
            assert f_in.read() == 'original text\ntest\nextra text\n'


def test_format_license_noprefix():
    with pytest.raises(ValueError):
        headercop.format_license('meh')


def test_format_license_mixed():
    result = headercop.format_license('meh', prefix='/*', perline_prefix='# ', postfix='*/')
    assert result == '/*\n# meh\n*/\n'


def test_format_license_prefix():
    result = headercop.format_license('meh', prefix='/*', postfix='*/')
    assert result == '/*\nmeh\n*/\n'


def test_format_license_preline():
    result = headercop.format_license('meh', perline_prefix='# ')
    assert result == '# meh\n'


def test_format_license_perline_postfix():
    result = headercop.format_license('meh', perline_prefix='# ', postfix='\n\n')
    assert result == '# meh\n\n\n'


def test_format_license_perline_postfix_license_has_trailing_return():
    result = headercop.format_license('meh\n', perline_prefix='# ', postfix='\n\n')
    assert result == '# meh\n\n\n'


def test_notrailing_whitespace():
    result = headercop.format_license('\n\n', perline_prefix='# ')
    assert result == '#\n'


def test_render_current():
    year = datetime.date.today().year
    assert str(year) == headercop.render_license('{year}', author=None, program=None, year=None)


def test_render_lastyear():
    year = datetime.date.today().year - 1
    assert str(year) == headercop.render_license('{year}', author=None, program=None, year=year)


def test_inject_header():
    with tempfile.TemporaryDirectory() as f_out:
        tester_path = Path(f_out, 'tester.sh')
        with tester_path.open('w') as f_out:
            f_out.write('#/bin/sh\n')
        headercop.inject_header(tester_path, '# test license', 1, '.*')
        with tester_path.open('r') as f_out:
            assert f_out.read() == '#/bin/sh\n# test license'


def test_inject_headeronly():
    with tempfile.TemporaryDirectory() as f_out:
        tester_path = Path(f_out, 'tester.sh')
        with tester_path.open('w') as f_out:
            f_out.write('#/bin/sh\n')
        headercop.inject_header(tester_path, '# test license', 2, '.*')
        with tester_path.open('r') as f_out:
            assert f_out.read() == '#/bin/sh\n# test license'


def test_inject_interwoven(shell_file):
    headercop.inject_header(shell_file, '# test license\n', 1, '.*')
    with shell_file.open('r') as f_out:
        assert f_out.read() == '#/bin/sh\n# test license\nsome text\n'


def test_check_interwoven(shell_file):
    headercop.inject_header(shell_file, '# test license\n', 1, '.*')
    with shell_file.open() as sf:
        assert headercop.check_file(sf, '# test license\n', 1)


def test_check_interwoven_wellwithintolerance(shell_file):
    headercop.inject_header(shell_file, '# test license\n', 1, '.*')
    with shell_file.open() as sf:
        assert headercop.check_file(sf, '# test license\n', 5)


def test_check_interwoven_shorttolerance(shell_file):
    headercop.inject_header(shell_file, '# test license\n', 2, '.*')
    with shell_file.open() as sf:
        assert not headercop.check_file(sf, '# test license\n', 1)


def test_check_mayskip_instant(shell_file):
    headercop.inject_header(shell_file, '# test license\n', 2, '$^')
    with shell_file.open('r') as f_out:
        assert f_out.read() == '# test license\n#/bin/sh\nsome text\n'


def test_check_mayskip_shebang(shell_file):
    headercop.inject_header(shell_file, '# test license\n', 2, '^#')
    with shell_file.open('r') as f_out:
        assert f_out.read() == '#/bin/sh\n# test license\nsome text\n'


def test_check_mayskip_everything(shell_file):
    headercop.inject_header(shell_file, '# test license\n', 2, '.*')
    with shell_file.open('r') as f_out:
        assert f_out.read() == '#/bin/sh\nsome text\n# test license\n'


def test_remove_header_identity(shell_file):
    with shell_file.open() as sf:
        shell_file_text = sf.read()
    headercop.inject_header(shell_file, '# test license\n', 2, '.*')
    headercop.remove_header(shell_file, '# test license\n', 4)
    with shell_file.open() as sf:
        assert shell_file_text == sf.read()


def test_remove_header_fail(shell_file):
    with shell_file.open() as sf:
        shell_file_text = sf.read()
    headercop.inject_header(shell_file, '# test license\n', 4, '.*')
    headercop.remove_header(shell_file, '# test license\n', 1)
    with shell_file.open() as sf:
        assert shell_file_text != sf.read()


def test_remove_header_fail_partialmatch(shell_file):
    headercop.inject_header(shell_file, '# test license\n', 0, '.*')
    with shell_file.open() as sf:
        shell_file_text = sf.read()
    headercop.remove_header(shell_file, '# test license\n# Some more of the license', 1)
    with shell_file.open() as sf:
        assert shell_file_text == sf.read()


def test_remove_header_previousfailed():
    with pytest.raises(ValueError), tempfile.NamedTemporaryFile() as f_in:
        swap_file = Path(f_in.name)
        swap_file = Path(swap_file.parent, '.{}.headercop.swp'.format(swap_file.name))
        with swap_file.open('w'):
            headercop.remove_header(Path(f_in.name), 'no license', 0)


def test_remove_header_bad_license(shell_file):
    with pytest.raises(ValueError):
        headercop.remove_header(shell_file, '\n', 1)
