'''VariableLoader class definition'''

import numpy
from .Definitions import Definitions


class VariableLoader:
    '''
    Variable loader class. Does some checks and returns the requested variable
    as a NumPy array.
    '''

    def __init__(self, url, dataset_name, dds):

        # Get available DDS definitions
        self.url = url
        self.dataset_name = dataset_name
        self.dds = dds

    def get_request_url(self, var_name, dim_sels):

        '''
        The dimension selections (dim_sels) variable must be a numpy ndarray,
        type int, size N by 3.
        Each row corresponds to one variable dimension, with columns containing
        the min, step and max indexes
        '''
        # Check variable exists and dimensions are not exceeded

        if var_name not in self.dds:
            print('VariableLoader: Requested variable not in DDS, stopping.')
            return None

        var_dims = self.dds[var_name][1]
        num_dims = len(var_dims)
        if (num_dims > 0) and (dim_sels.shape[0] != num_dims):
            print('VariableLoader: Requested number of dimensions incorrect, \
stopping.')
            return None

        dims_ok = self.check_dim_sels(var_dims, dim_sels, num_dims)
        if not dims_ok:
            print('VariableLoader: At least one dimension selection request \
is not valid, stopping.')
            return None

        # Construct the request url

        requrl = self.url + '.dods?' + var_name
        for idim in range(num_dims):
            dimstr = '[' + str(dim_sels[idim, 0]) + ':' + \
                     str(dim_sels[idim, 1]) + ':' + \
                     str(dim_sels[idim, 2]) + ']'
            requrl += dimstr

        return requrl

    @staticmethod
    def check_dim_sels(var_dims, dim_sels, num_dims):

        '''Extract dimension selections and check they're valid.'''

        dims_ok = True
        for idim in range(num_dims):
            if (dim_sels[idim, 0] < 0) or (dim_sels[idim, 1] < 0) or \
               (dim_sels[idim, 2] < 0):
                dims_ok = False
            if (dim_sels[idim, 0] > var_dims[idim] - 1) or \
               (dim_sels[idim, 2] > var_dims[idim] - 1):
                dims_ok = False
            if dim_sels[idim, 2] < dim_sels[idim, 0]:
                dims_ok = False
            if (dim_sels[idim, 0] != dim_sels[idim, 2]) and \
               (dim_sels[idim, 1] > dim_sels[idim, 2]):
                dims_ok = False

        return dims_ok

    def load_variable(self, var_name, var_data, dim_sels, byte_ord_str,
                      check_type=True):
        '''
        Load the requested variable and return as a NumPy array.
        '''

        dims = False
        if dim_sels.shape[1] == 3:
            dims = True
        #  Otherwise size is [1,1] and contains number of elements in
        # dimensionless data

        if dims:
            boffs = 8
            #  Byte offset for the two occurrences of the number of
            #  elements (int32)
        else:
            boffs = 4
            #  Offset for dimensionless data

        #  Find the header portion of the byte stream
        # (until the 'Data' identifier)

        data_id = 'Data:\n'.encode('utf-8')
        id_len = len(data_id)
        data_len = len(var_data)

        i = 0
        while (i < data_len-id_len-1) and (var_data[i:i+id_len] != data_id):
            i += 1
        if var_data[i:i+id_len] != data_id:
            print('VariableLoader: Data start identifier not found, stopping.')
            return None

        data_start_ind = i + id_len
        data_start_ind += boffs

        # Check the var_data byte stream contains the correct variable type
        hdr_str = var_data[:data_start_ind - boffs].decode('utf-8')
        var_type = self.dds[var_name][0]
        if check_type and (var_type not in hdr_str):
            print('VariableLoader: Variable type in requested data header \
does not match DDS, stopping.')
            return None

        #  Check the var_data byte stream contains the correct
        # variable dimensions

        dim_str = var_name
        if dims:
            dim_str, num_els = self.get_dim_str(dim_sels, var_name)
        else:
            num_els = dim_sels[0, 0]  # Number of elements to retrieve

        if dim_str not in hdr_str:
            print('VariableLoader: Variable dimensions in requested data \
header do not match DDS, stopping.')
            return None

        # All OK - load the variable

        np_type = Definitions.atomics[var_type]
        data_type = np_type

        if len(byte_ord_str) > 0:
            data_type = np_type.newbyteorder(byte_ord_str)

        lvar = numpy.frombuffer(var_data, dtype=data_type,
                                count=numpy.prod(num_els),
                                offset=data_start_ind)
        if dims:
            var = lvar.reshape(tuple(num_els))
        else:
            var = lvar

        return var

    def get_dim_str(self, dim_sels, var_name):

        '''Get the dimension selection string and numbr of elements'''

        assoc_names = self.dds[var_name][2]
        dim_str = var_name
        num_els = []
        for idim in range(dim_sels.shape[0]):
            count = 1
            ind = dim_sels[idim, 0]
            while ind < dim_sels[idim, 2]:
                ind += dim_sels[idim, 1]
                count += 1
            if ind > dim_sels[idim, 2]:
                count -= 1
            num_els.append(count)
            dim_str += '[' + assoc_names[idim] + ' = ' + \
                       str(num_els[idim]) + ']'

        return dim_str, num_els
