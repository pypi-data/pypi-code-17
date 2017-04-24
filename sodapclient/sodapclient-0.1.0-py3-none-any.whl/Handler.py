''''Handler class definition'''

import urllib.request as ureq
from datetime import datetime

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .ProxyDict import ProxyDict
from .DDSParser import DDSParser
from .DASParser import DASParser
from .VariableLoader import VariableLoader


class Handler:

    '''
    The main sodapclient class.

    Both atomic variables and constructor variables are handled.
    Note that map vectors within constructors are treated
    as atomic variables. This means that existing variable names will be
    overwritten whenever they are repeated (whether atomic variables or
    map vectors within a constructor). E.g. if a Grid contains an atomic
    N-dimensional array it will be included in the returned dds and the
    variable will be loaded but any map vectors with the same name as an
    existing atomic variable will overwrite the existing variable.
    Therefore the implementation will work provided map vectors defined within
    a constructor are identical to any variable with the same name defined
    outside the constructor. This should not be a limitation as all OpenDAP
    datasets seem to adhere to this anyway.
    '''

    def __init__(self, url, proxy_file_name=None, log=False):

        self.log_file = None
        if log:
            log_file_name = '/var/tmp/sodapclient-log-' + \
                str(datetime.now().timestamp()) + '.txt'
            self.log_file = open(log_file_name, 'wt')
            self.log_file.write('sodapclient created at ' +
                                str(datetime.now()) + '\n\n')

        # Set up the proxy (if required)
        if proxy_file_name is not None:
            self.proxy_dict = ProxyDict(proxy_file_name)
            if self.proxy_dict.valid_proxy:
                self.set_up_proxy()
        if self.log_file:
            self.log_file.write('Using Proxy Server.\n')

        # Check the URL is valid
        urlval = URLValidator()
        try:
            urlval(url)
        except ValidationError:
            msg = 'ERROR: Invalid URL format\n'
            if self.log_file:
                self.log_file.write(msg)
            print(msg)
            raise

        self.base_url = url
        if self.base_url[-4:] == 'html':   # Remove .html extension if present
            self.base_url = self.base_url[:-5]

        if self.log_file:
            self.log_file.write('Base URL: ' + self.base_url + '\n')

        # Set up the dds
        self.get_dds()

        # Set up the das
        self.get_das()

        # Set up the (initially empty) variables dictionary
        self.variables = {}  # Dictionary to hold loaded variables

    def __del__(self):
        '''Close the log file when the handler is deleted'''
        if self.log_file:
            self.log_file.write('\nHandler destroyed at ' +
                                str(datetime.now()) + '\n\n')
            self.log_file.close()

    def set_up_proxy(self):
        '''Set up the proxy'''
        proxy_handler = ureq.ProxyHandler(self.proxy_dict.get_dict())
        opener = ureq.build_opener(proxy_handler)
        ureq.install_opener(opener)

    def get_dds(self):
        '''Get the Dataset Descriptor Structure (DDS)'''
        turl = self.base_url + '.dds'
        try:
            urlo = ureq.urlopen(turl)
        except ureq.HTTPError:
            self.dds = None
            return
        dds_str = urlo.read().decode('utf-8')
        urlo.close()
        dds_parser = DDSParser()
        dds_parser.parse(dds_str)
        self.dataset_name = dds_parser.dataset_name
        self.dds = dds_parser.data
        if self.log_file:
            self.log_file.write('\n--- dds ---\n\n')
            dds_parser.print_dds_to_file(self.log_file)

    def get_das(self):
        '''Get the Dataset Attribute Structure (DAS)'''
        turl = self.base_url + '.das'
        try:
            urlo = ureq.urlopen(turl)
        except ureq.HTTPError:
            self.das = None
            return
        das_str = urlo.read().decode('utf-8')
        urlo.close()
        das_parser = DASParser()
        das_parser.parse(das_str)
        self.das = das_parser.data
        if self.log_file:
            self.log_file.write('--- das ---\n\n')
            das_parser.print_das_to_file(self.log_file, das=None)
            self.log_file.write('-----------\n\n')

    def get_variable(self, var_name, dim_sels, byte_ord_str, check_type=True):
        '''Get a variable'''
        var_loader = VariableLoader(self.base_url, self.dataset_name, self.dds)
        requrl = var_loader.get_request_url(var_name, dim_sels)
        if requrl is not None:
            with ureq.urlopen(requrl) as urlo:
                var_data = urlo.read()
            var = var_loader.load_variable(var_name, var_data, dim_sels,
                                           byte_ord_str, check_type)
            if var is not None:
                self.variables[var_name] = var

    def print_status(self):
        '''Print the handler status to the console'''
        print('HANDLER STATUS...\n')
        print('Base URL:', self.base_url, '\n')
        print('dds:\n')
        psr = DDSParser()  # Temporary object - just need printing function
        psr.print_dds(self.dataset_name, self.dds)
        print('das:\n')
        psr = DASParser()  # Temporary object - just need printing function
        psr.print_das(self.das)  # Convenience instantiation just to print dds

    def print(self):
        '''Print the handler status and available variables'''
        self.print_status()
        print('VARIABLES...\n')
        if len(self.variables) > 0:
            print('Variables loaded:\n')
            for var in self.variables.keys():
                print('Variable name :', var)
                print('Loaded dimensions :', self.variables[var].shape)
                print('data...')
                print(self.variables[var])
        else:
            print('No variables loaded.')
