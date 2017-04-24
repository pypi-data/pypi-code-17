''' DASParser class definition '''

from .Parser import Parser
from .Definitions import Definitions


class DASParser(Parser):

    '''
    DASParser class. Extracts and stores the attributes within a das string.
    '''

    def __init__(self):

        super().__init__()
        self.dtype = 'Dataset Attribute Structure (das)'

    def parse(self, das_str):
        ''' Parse the DAS'''

        self.find_start(das_str, Definitions.attributes)

        attr_ind = -1  # Attribute index counter

        # Main loop
        while (not self.finished) & (self.lnum < len(self.data_lines) - 1) & \
              (len(self.indts) > 0):
            do_line = self.check_line()
            if do_line:  # New Attribute
                attr_ind += 1
                attr_name = self.data_lines[self.lnum].split()[0]
                attr_data = []
                while self.check_line():
                    # Remove trailing semicolon
                    attr_data.append(self.data_lines[self.lnum].lstrip()[:-1])
                self.data[attr_name] = attr_data

    def print_das(self, das=None):
        '''Print the DAS to the console'''
        if das is None:
            das = self.data
        self.print_data(self.dtype, das)
        for var in das.keys():
            print('Variable :', var)
            print('Attributes...')
            for l in das[var]:
                print(l)
            print()

    def print_das_to_file(self, file_name, das=None):
        '''Print the DAS to a file'''
        if das is None:
            das = self.data
        self.print_data_to_file(self.dtype, das, file_name)
        for var in das.keys():
            file_name.write('Variable : ' + var + '\n')
            file_name.write('Attributes...\n')
            for l in das[var]:
                file_name.write(l + '\n')
            file_name.write('\n')
