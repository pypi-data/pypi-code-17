'''Parser class definition'''


class Parser:

    '''
    Serves as base class for DDSParser and DASParser classes.
    '''

    def __init__(self):

        self.dtype = 'Undefined'  # Name of parsed dataset (e.g. DDS, DAS)
        self.data = {}  # data dictionary
        self.indts = []  # Indentation list
        self.data_lines = []  # List of lines in data to be parsed
        self.lnum = 0  # Current line number
        self.finished = False  # Flag to indicate parsing complete

    def find_start(self, data_str, start_str):

        # Remove any empty lines
        temp_lines = data_str.split('\n')
        for l in temp_lines:
            if len(l) > 0:
                self.data_lines.append(l)

        # Loop to find start of dataset
        while start_str not in self.data_lines[self.lnum]:
            if self.lnum == len(self.data_lines) - 1:
                print('Parser: No datasets found, stopping.')
                break
            self.lnum += 1

        # Get root indentation level and store in list
        if self.lnum < len(self.data_lines) - 1:
            self.indts.append(self.find_indent_level
                              (self.data_lines[self.lnum]))

    @staticmethod
    def find_indent_level(line):

        i = 0
        if len(line) > 0:
            el = line.split()[0]  # First element
            while line[i:i+len(el)] != el:
                i += 1
        return i

    def check_line(self):

        do_line = True

        self.lnum += 1
        indt = self.find_indent_level(self.data_lines[self.lnum])

        if indt > self.indts[-1]:  # Increased: expecting new variable
            self.indts.append(indt)
        elif indt < self.indts[-1]:  # Decreased: end of current body
            while (len(self.indts) > 0) & (indt < self.indts[-1]):
                self.indts.pop()
            do_line = False
            if len(self.indts) == 1:  # Back to root level so must be finished
                self.finished = True

        return do_line

    @staticmethod
    def print_data(dtype, data):
        # dtype and data can be passed in externally for convenience
        print('dtype :', dtype, '\n')
        if len(data) == 0:
            print('Structure is not defined')

    @staticmethod
    def print_data_to_file(dtype, data, file):
        # dtype, data & file object can be passed in externally for convenience
        file.write('dtype :' + dtype + '\n\n')
        if len(data) == 0:
            file.write('Structure is not defined\n')
