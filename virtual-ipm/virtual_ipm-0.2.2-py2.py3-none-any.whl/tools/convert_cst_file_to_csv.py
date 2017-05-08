# -*- coding: utf-8 -*-

#    Virtual-IPM is a software for simulating IPMs and other related devices.
#    Copyright (C) 2017  The IPMSim collaboration <http://ipmsim.gitlab.io/IPMSim>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import codecs
import os
import six
import re

parser = argparse.ArgumentParser()
parser.add_argument('cst_file')
parser.add_argument('--csv-file', help='If not given the csv filename is determined from the cst '
                                       'filename.')
args = parser.parse_args()

if not args.csv_file:
    path, ext = os.path.splitext(args.cst_file)
    csv_file = '{0}.{1}'.format(path, 'csv')
else:
    csv_file = args.csv_file
print('csv_file: ', csv_file)

with codecs.open(args.cst_file, encoding='ascii') as f_in, \
        codecs.open(csv_file, 'w', encoding='ascii') as f_out:
    header = f_in.readline()
    markup_line = f_in.readline()
    header = re.sub(r'\s\s+', r',', header)
    if header.endswith(','):
        header = header[:-1]
    if header.startswith(','):
        header = header[1:]
    f_out.write(header + '\n')
    for entry in f_in:
        cols = list(filter(
            None,
            entry.split(' ')
        ))
        csv_entry = ','.join(map(
            six.text_type,
            cols
        ))
        f_out.write(csv_entry)
