''' DDSParser class definition '''

from .Parser import Parser
from .Definitions import Definitions


class DDSParser(Parser):
    '''
    Dataset Descriptor Response (dds) parser class.

    Given a dds string read from a URL, it parses the string to set up
    a dds dictionary. The dictionary is of form:
    {name : [type, [dims], [assoc_names]]}
    where name is the variable name,
    dims is a list of dimensions,
    assoc_names is a list of associated names.

    See Handler class for comments on constructor handling.

    A single data set is included, i.e. if the URL describes more than one,
    only the first will be included.
    '''

    def __init__(self):

        super().__init__()
        self.dtype = 'Dataset Descriptor Structure (dds)'

        self.atomic_defs = list(Definitions.atomics.keys())
        self.constructor_defs = Definitions.constructors

        self.dataset_name = 'Undefined'

    def parse(self, dds_str):
        '''Parse the DDS'''

        self.find_start(dds_str, Definitions.dataset)

        # Main loop
        while (not self.finished) and \
              (self.lnum < len(self.data_lines) - 1) and (len(self.indts) > 0):
            do_line = self.check_line()
            if do_line:
                self.process_line()

        if self.finished:
            # Exclude trailing semicolon...
            self.dataset_name = self.data_lines[self.lnum].split()[-1][:-1]

    def process_line(self):
        ''' Process a line'''

        var_type = None
        next_line = self.data_lines[self.lnum]
        segs = next_line.split()
        for adef in self.atomic_defs:
            if segs[0] == adef:
                var_type = adef
                self.read_atomic(next_line, var_type)
                break
        if var_type is None:  # Not an atomic type
            for adef in self.constructor_defs:
                if segs[0] == adef:
                    var_type = adef
                    self.read_constructor(next_line, var_type)
                    break

    def read_atomic(self, line, var_type):
        ''' Read an atomic variable'''
        # Will still work even if dimensionless...
        var_name = line.split()[1].split('[')[0]
        segs = line.split('=')
        num_dims = len(segs) - 1
        # Remove trailing semicolon...
        if num_dims == 0:
            var_name = var_name[:-1]
        dims = [None]*num_dims
        assoc_names = [None]*num_dims
        for idim in range(num_dims):
            # Remove trailing space...
            assoc_names[idim] = segs[idim].split('[')[-1][:-1]
            dims[idim] = int(segs[idim+1].split(']')[0])
        self.data[var_name] = [var_type, dims, assoc_names]

    def read_constructor(self, line, var_type):
        ''' Reading constructor variables not implemented
        (all variables handled as atomics)'''
        pass

    def print_dds(self, dataset_name=None, dds=None):
        ''' Print the dds to the console. Dataset name and dds
        can be passed in externally for convenience'''
        if dataset_name is None:
            dataset_name = self.dataset_name
        if dds is None:
            dds = self.data
        self.print_data(self.dtype, dds)
        print('Dataset name :', dataset_name, '\n')
        for var in dds.keys():
            print('Variable name :', var)
            print('dtype :', dds[var][0])
            print('Dimensions :', dds[var][1])
            print('Associated names :', dds[var][2], '\n')

    def print_dds_to_file(self, file_name, dataset_name=None, dds=None):
        ''' Print the dds to a file. Dataset name and dds
        can be passed in externally for convenience'''
        if dataset_name is None:
            dataset_name = self.dataset_name
        if dds is None:
            dds = self.data
        self.print_data_to_file(self.dtype, dds, file_name)
        file_name.write('Dataset name : ' + dataset_name + '\n\n')
        for var in dds.keys():
            file_name.write('Variable name : ' + var + '\n')
            file_name.write('dtype : ' + dds[var][0] + '\n')
            file_name.write('Dimensions : ' + str(dds[var][1]) + '\n')
            file_name.write('Associated names : ' + str(dds[var][2]) + '\n\n')
