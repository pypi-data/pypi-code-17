#!/usr/bin/env python
"""Convert structured text data into table format.

Available functions:
- parse_file: 
"""

__author__ = 'pbilling@stanford.edu (Paul Billing-Ross)'

import re
import pdb
import sys
import json 

from itertools import ifilter

class FlexTableParser:

    def __init__(self, config_file, out_file, static_values={}):
        
        self.static_values = static_values
        self.out_fh = open(out_file, 'w')

        with open(config_file, 'r') as config_fh:
            self.config = json.load(config_fh)
        self.schema = self.config['schema']
        self.dimensions = self.config['dimensions']
        self.overlap = bool(self.config['overlap'])

        #pdb.set_trace()
        self.match_patterns = []
        for dimension_name in self.dimensions:
            dimension = self.dimensions[dimension_name]
            regex_pattern = dimension['regex_pattern']
            self.match_patterns.append(regex_pattern)


    def _write_single_row(self, dimension_name, value):
        """Write single row to table.

        Args:
            dimension (str):
            value (int/float): 

        """

        print('Writing single row for dimension: {}'.format(dimension_name))
        # Fixed at 1 when writing single row
        index = ''
        
        # Combine line-entry values with static values
        table_values = {
                        'dimension': dimension_name,
                        'index': index,
                        'value': value
                       }
        static_values = self.static_values.copy()
        table_values.update(static_values)

        # Populate out string ordered by schema
        strings = [str(table_values[column]) for column in self.schema]
        out_str = ','.join(strings) + '\n'
        self.out_fh.write(out_str)

    def _write_series_rows(self, dimension, in_fh):
        """Write series of rows.
        """

        dimension_name = dimension['name']
        print('Writing series of rows for dimension: {}'.format(dimension_name))
        # Indexes of the delimiter separated line.
        # (I know, I know... need better terminology.)
        index_element = dimension['index']  # type: int
        value_element = dimension['value']  # type: int

        delimiter = dimension['delimiter'] # type: str
        if not delimiter:
            delimiter = None
        stop_pattern = dimension['stop_pattern'] # type: str

        stop = False

        while stop == False:
            table_values = self.static_values.copy()
            line = in_fh.next()
            #pdb.set_trace()
            stop_match = re.match(stop_pattern, line)
            if stop_match:
                stop = True
            else:
                elements = line.split(delimiter)
                print(elements)
                table_values['dimension'] = dimension['name']
                table_values['index'] = elements[index_element]
                table_values['value'] = elements[value_element]

                # Convert all values to schema ordered strings
                strings = [str(table_values[column]) for column in self.schema]
                out_str = ','.join(strings) + '\n'
                self.out_fh.write(out_str)

    def _parse_match(self, match, in_fh):
        """Parse single line pattern match.
        """
        dimension_name = match.groupdict().keys()[0]
        print(dimension_name)
        row_type = self.dimensions[dimension_name]['row_type']
        if row_type == 'single':
            value = match.groupdict().values()[0]
            self._write_single_row(dimension_name, value)
        elif row_type == 'series':
            dimension = self.dimensions[dimension_name]
            self._write_series_rows(dimension, in_fh)
        else:
            print('Error: Invalid dimension type: {}'.format(dimension_type))
            pdb.set_trace()

    def parse_file(self, in_file):
        """Parse file.
        """
        with open(in_file, 'r') as in_fh:
            for line in in_fh:
                matches = [re.match(regex, line) for regex in self.match_patterns]
                true_matches = list(ifilter(lambda x: x > 0, matches))
                if len(true_matches) == 0:
                    continue
                elif len(true_matches) > 1:
                    print('\nWarning: Multiple regex patterns matched this line.')
                    print(line.strip())
                    #pdb.set_trace()
                    if self.overlap:
                        # Potential for error if you have overlapping matches 
                        # & and is a series
                        for match in true_matches:
                            self._parse_match(match, in_fh)
                    else:
                        print('Error: Configuration file does not allow for overlapping patterns')
                        sys.exit()

                elif len(true_matches) == 1:
                    print('\nInfo: Found single match for line.')
                    print(line.strip())
                    self._parse_match(true_matches[0], in_fh)
                        