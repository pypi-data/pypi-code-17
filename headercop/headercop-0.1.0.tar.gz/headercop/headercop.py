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
import re
import typing

from pathlib import Path


def check_file(file_in: typing.TextIO, formatted_license: str, tolerance: int):
    '''Check a file to see if it has the license header or not

    :param file_in: File like object to check
    :param formatted_license: The license text to check for
    :param tolerance: How many lines in the from the top of the file before the
        license text MUST start to appear
    :returns: Boolean for if the license was found in the file
    '''

    if not formatted_license.strip():
        raise ValueError('License text cannot be empty when checking for license headers')
    license_text = list(l.strip() for l in formatted_license.strip().split('\n'))
    license_found = False
    for line_no, line in enumerate(file_in):
        if not license_found and line_no > tolerance:
            return False
        if len(license_text) == 0:  # Full license text has been found
            return True
        if line.strip() == license_text[0].strip():
            license_found = True
            license_text.pop(0)
        elif license_found and line.strip() != license_text[0].strip():
            return False  # License text has some difference in it
    # Handle empty file OR license is the WHOLE file
    return license_found and len(license_text) == 0


def inject_header(target: Path,
        formatted_license: str,
        skip_lines: int,
        may_skip_regex: str):
    '''Inject the license header into a file

    :param target: File to add the license to
    :param formatted_license: The license text to check for
    :param skip_lines: How many lines from the top of the file to skip before
        inserting license text
    :param may_skip_regex: regex to use to check if a line may be skipped
    '''

    swap_file = Path(target.parent, '.{}.headercop.swp'.format(target.name))
    if swap_file.exists():
        raise ValueError('Previous run crashed? (remove {} after checking {})'
            .format(swap_file, target))

    header_only = False
    with target.open() as f_in, swap_file.open('w') as f_out:
        reader = iter(enumerate(f_in))
        # First find where we're going to inject the header
        for line_no, line in reader:
            if line_no < skip_lines and re.search(may_skip_regex, line) is not None:
                f_out.write(line)
                continue
            break
        else:  # aka we read the entire file... thus just need to write the header
            header_only = True
        # We're at the point where we know we have to write the header
        f_out.write(formatted_license)
        if not header_only:
            f_out.write(line)  # Catch the line from above that we skipped
            for line_no, line in reader:  # write out the rest of the file
                f_out.write(line)
    swap_file.rename(target)


def remove_header(target: Path,
        formatted_license: str,
        tolerance: int):
    '''Remove the license header from a file

    Generally this should be used if the license needs to be re-rendered (e.g.
    updating the copyright year)

    :param target: File to remove the license from
    :param formatted_license: The license text to check for
    :param tolerance: How many lines in the from the top of the file before the
        license text MUST start to appear
    '''

    swap_file = Path(target.parent, '.{}.headercop.swp'.format(target.name))
    if swap_file.exists():
        raise ValueError('Previous run crashed? (remove {} after checking {})'
            .format(swap_file, target))

    if not formatted_license.strip():
        raise ValueError('License text cannot be empty when checking for license headers')
    license_text = list(l.strip() for l in formatted_license.strip().split('\n'))
    license_found = False
    with target.open() as f_in, swap_file.open('w') as f_out:
        for line_no, line in enumerate(f_in):
            if not license_found and line_no > tolerance:
                break  # No license, we can skip this file
            if line.strip() == license_text[0].strip():
                license_found = True
                license_text.pop(0)
                continue
            elif license_found and line.strip() != license_text[0].strip():
                break  # Found part of the license...
            f_out.write(line)
    if license_found and len(license_text) == 0:
        swap_file.rename(target)
    else:
        swap_file.unlink()


def format_license(orignal_text: str, prefix: str=None, postfix: str=None, perline_prefix: str=None):
    rendered_text = orignal_text
    if perline_prefix is None and prefix is None:
        raise ValueError("At least one of prefix or perline_prefix is required")
    if perline_prefix is not None:
        rendered_text = '\n'.join('{perline_prefix}{line}'.format(perline_prefix=perline_prefix, line=line).strip()
            for line in rendered_text.strip().split('\n'))
    if prefix:
        rendered_text = '{prefix}\n{rendered_text}'.format(
            prefix=prefix.strip(), rendered_text=rendered_text)
    if postfix:
        rendered_text = '{rendered_text}\n{postfix}'.format(
            postfix=postfix, rendered_text=rendered_text.strip())
    # Enforce trailing return
    if rendered_text == rendered_text.strip():
        rendered_text = '{}\n'.format(rendered_text)
    return rendered_text


def render_license(template: str, author: str, program: str, year: str=None):
    if year is None:
        year = datetime.date.today().year
    return template.format(author=author, program=program, year=year)
