import requests
import time
from zohoapi import config
from zohoapi.errors import (ZohoGeneralError, ZohoBadRecordError,
                            ZohoConnectionError, ZohoNoDataError)
from xml.etree import ElementTree

"""
Because of the way modules and module id's are named, all custom modules must be mapped in
in this dictionary
'Id' for 'Accounts' is 'ACCOUNTID'
'Id' for 'CustomModule3' is 'CUSTOMMODULE3_ID'
Note the difference in plurals as well as the underscore inconsistency
"""
custom_module_mapping = {
    'TradeShows': 'CustomModule3',
}


class _BaseConnection:
    """
    This is an abstract class that ensures all of our api calls are made using
    the same method: _call_zoho()
        _call_zoho() is our meat and potatoes so to speak, it is the only method
        that ever really does anything. It's setup to accept a method and parameters,
        which are generally defined in less abstract methods

    It also handles our sessions, if we have one already it passes it along
    otherwise it'll create one the first time you init a new ZohoConnection()

    We also house some helper functions here to help with formatting etc.
    """
    def __init__(self, session=None):
        self.base_url = 'https://crm.zoho.com/crm/private/'
        self.data_format = ''
        self.module = ''
        self.method = ''
        self.params = {'authtoken': config.AUTH_TOKEN,
                       'scope': 'crmapi', }
        self.headers = config.BASE_HEADERS

        if session:
            self.session = session
        else:
            self.session = requests.Session()

    @property
    def url(self):
        if not (self.base_url and self.module and self.method and self.data_format):
            raise ZohoGeneralError
        return self.base_url + self.data_format + '/' + self.module + '/' + self.method

    def _call_zoho(self, method, **parameters):
        _data = None
        for param in parameters:
            if param == 'xmlData':
                _data = parameters['xmlData']
                parameters['xmlData'] = None
            if parameters[param]:
                self.params[param] = parameters[param]
        result = self.session.request(method, self.url, params=self.params, data={'xmlData': _data})
        if result.status_code >= 300:
            raise ZohoConnectionError(result.url, result.content)

        if self.data_format == 'json':
            if 'result' not in result.json()['response']:
                if 'nodata' not in result.json()['response']:
                    # TODO: Determine why this never works, maybe we need to wait for a full minute?
                    # Limit is supposed to be '60 times per minute' with literally no other explanation
                    if result.json()['response']['error']['code'] == '4820':
                        print('You\'ve hit the searchRecords rate limit... Good luck... trying again in 30 seconds')
                        time.sleep(30)
                        self.session = requests.Session()
                        self._call_zoho(method, **parameters)
                    raise ZohoBadRecordError(result.url, result.json()['response'])
                else:
                    raise ZohoNoDataError(result.url, result.json()['response'])
            return result.json()

        if self.data_format == 'xml':
            """
            Zoho returns xml errors in the form:
            <row no="2">
                <error>
                    <code>4832</code>
                    <details>You have given a wrong value for the field : Annual Revenue</details>
                </error>
            </row>
            """
            errors = []
            if ElementTree.fromstring(result.content)[0].tag == 'error':
                _code = ElementTree.fromstring(result.content)[0].find('code').text
                _message = ElementTree.fromstring(result.content)[0].find('message').text
                return 'Error {}: {}'.format(_code, _message)
            for row in ElementTree.fromstring(result.content)[0].findall('row'):
                if row.find('error'):
                    _content = "Row: {} Code: {} Details: {}".format(row.attrib['no'],
                                                                        row.find('error')[0].text,
                                                                        row.find('error')[1].text)
                    errors.append(_content)
            return errors if errors else [i[0].text for i in
                                          ElementTree.fromstring(result.content).find('result').findall('recorddetail')]

    @staticmethod
    def _xml_format(key, content):
        if isinstance(content, int):
            return "<FL val=\"{key}\">{content}</FL>".format(key=key, content=content)
        else:
            return "<FL val=\"{key}\"><![CDATA[{content}]]></FL>".format(key=key, content=content)

    def _gen_content(self, value_content_dict):
        return ''.join([self._xml_format(k, c) for k, c in value_content_dict.items()])

    def dicts_to_xml(self, value_content_dicts):

        # If it's a single record we make it a list so our iterable below works
        if not isinstance(value_content_dicts, list):
            value_content_dicts = [value_content_dicts]

        _xml = "<{module}>" \
               "{rows_of_content}" \
               "</{module}>"

        row = "<row no=\"{row_number}\">" \
              "{content}" \
              "</row>"

        rows_of_content = ''.join([row.format(row_number=(row_number + 1), content=self._gen_content(record))
                                   for row_number, record in enumerate(value_content_dicts)])

        return _xml.format(module=self.module, rows_of_content=rows_of_content)


class _RecordMethods(_BaseConnection):
    """
    Abstract Class that contains shared methods that follow the same form
    in different modules. These get called primarily on single records, but could
    be called outright if the record_id is passed as a mandatory parameter

    >>> zc = ZohoConnection()
    >>> zc.Contacts.delete_record(100201947456)
    >>> zc.Account.update_record(101020654321, {'Account Name': 'Test Account'})

    They're subclasses in the _SingleRecord class and the id is automatically
    supplied
    """
    def __init__(self, module, session):
        super().__init__(session=session)
        self.module = module

    def _return_records(self, _resp, _returned_record_type=None):
        if not _returned_record_type:
            _returned_record_type = self.module
        if isinstance(_resp['response']['result'][_returned_record_type]['row'], dict):
            return [_SingleRecord(_resp['response']['result'][_returned_record_type]['row']['FL'],
                                  _returned_record_type, session=self.session)]
        else:
            return [_SingleRecord(i['FL'], _returned_record_type, session=self.session) for i in
                    _resp['response']['result'][_returned_record_type]['row']]

    def delete(self, record_id, **params):
        self.data_format = 'json'
        self.method = 'deleteRecords'
        params['id'] = record_id
        return self._call_zoho('POST', **params)

    def update(self, record_id, content_val_dict, **params):
        self.data_format = 'xml'
        self.method = 'updateRecords'
        params['id'] = record_id
        params['xmlData'] = self.dicts_to_xml(content_val_dict)
        _resp = self._call_zoho('POST', **params)
        return _resp

    # This is a weird one. if we start with a lead and we want campaigns
    # we actually have to make the request through the campaigns module
    # this is a kind of hackey workaround. I think Zoho built it backwards
    def related_records(self, record_id, parent_module, **params):
        _resp = None
        self.data_format = 'json'
        self.method = 'getRelatedRecords'
        params['parentModule'] = self.module
        params['id'] = record_id
        _real_module = self.module
        self.module = parent_module
        try:
            _resp = self._call_zoho('GET', **params)
        except (ZohoBadRecordError, ZohoNoDataError):
            pass
        self.module = _real_module
        if _resp:
            return self._return_records(_resp, _returned_record_type=parent_module)
        else:
            raise ZohoNoDataError(self.url, 'This is ok, there were no related records')


class _ModuleMethods(_RecordMethods):
    """
    This abstract class contains methods that can only be called on plain
    old modules, never on records

    _return_records() is an ugly, ugly function that fixes the really stupid
    way zoho returns data if there is only one record. All records are returned
    as part of a list
    """

    def _extend_record(self, params):
        print('Gathering {} from {} to {}'.format(self.module, params['fromIndex'], params['toIndex']))
        return self._return_records(self._call_zoho('GET', **params))

    def _loop_records(self, params):
        params['fromIndex'] = 1
        params['toIndex'] = 200
        _records = []
        while True:
            time.sleep(.7)
            _resp = self._extend_record(params)
            _records.extend(_resp)
            # This makes sure we stop looping if we're not getting responses
            if len(_resp) < 200:
                return _records

            params['fromIndex'] += 200
            if params['toIndex'] + 200 == params['recordCount']:
                params['toIndex'] += 200
                _records.extend(self._extend_record(params))
                return _records
            elif params['toIndex'] + 200 > params['recordCount']:
                params['toIndex'] += (params['recordCount'] - int(params['toIndex']))
                _records.extend(self._extend_record(params))
                return _records
            else:
                params['toIndex'] += 200

    def get_records(self, **params):
        self.data_format = 'json'
        self.method = 'getRecords'

        """
        Since Zoho is nice enough not to supply us with a 'next' or 'link' in
        their response header we get to hand roll a pagination system that only
        asks for 200 records at a time
        """
        if 'recordCount' in params:
            return self._loop_records(params)

        else:
            return self._return_records(self._call_zoho('GET', **params))

    # Somebody really cool would build a method to make this
    # more intuitive
    # >>> zc.Accounts.search_records('((Account Name:Crawford)OR(Phone:111))')
    def search_records(self, criteria, select_columns='All', **params):
        self.data_format = 'json'
        self.method = 'searchRecords'
        params['criteria'] = criteria
        params['selectColumns'] = select_columns
        params['fromIndex'] = 1
        params['toIndex'] = 200

        if 'recordCount' in params:
            return self._loop_records(params)
        else:
            return self._return_records(self._call_zoho('GET', **params))

    def get_by_pdc(self, search_column, search_value, select_columns='All', **params):
        self.data_format = 'json'
        self.method = 'getSearchRecordsByPDC'
        self.params['searchColumn'] = search_column
        self.params['selectColumns'] = select_columns
        self.params['searchValue'] = search_value

        return self._return_records(self._call_zoho('GET', **params))

    def update(self, content_val_dict_list, **params):
        # All of these k,v dicts must contain the key 'id'
        self.data_format = 'xml'
        self.method = 'updateRecords'
        params['version'] = 4

        # Fuck you, you can only do 100 records at a time
        if len(content_val_dict_list) > 100:
            list_of_lists = [content_val_dict_list[x:x + 100] for x in range(0, len(content_val_dict_list), 100)]
            _resp = ''
            for mini_list in list_of_lists:
                _resp += str(self.update(mini_list, **params))
            return _resp

        else:
            params['xmlData'] = self.dicts_to_xml(content_val_dict_list)
            # print(params['xmlData'])
            _resp = self._call_zoho('POST', **params)
            return _resp

    def insert(self, content_val_dict_list, **params):
        self.method = 'insertRecords'
        self.data_format = 'xml'

        if len(content_val_dict_list) > 100:
            params['version'] = 4
            list_of_lists = [content_val_dict_list[x:x+100] for x in range(0, len(content_val_dict_list), 100)]
            _resp = ''
            for mini_list in list_of_lists:
                _resp += str(self.insert(mini_list, **params))
            return _resp

        else:
            params['xmlData'] = self.dicts_to_xml(content_val_dict_list)
            # print(params['xmlData'])
            _resp = self._call_zoho('POST', **params)
            return _resp


class _SingleRecord(_RecordMethods):
    def __init__(self, content_val_dict, module, session):
        super().__init__(module, session=session)
        self._content_dict = content_val_dict

    def __str__(self):
        return 'Zoho: {} {}'.format(self.module.rstrip('s'), self.id)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.value(item)

    @property
    def all_values(self):
        return {i.get('val', None): i.get('content', None) for i in self._content_dict}

    @property
    def id(self):
        if self.module in [v for k, v in custom_module_mapping.items()]:
            return self.value(self.module.upper() + '_ID')
        return self.value(self.module.upper()[:-1] + 'ID')

    def value(self, _value):
        return self.all_values.get(_value, None)

    def update(self, content_val_dict, **params):
        return super().update(self.id, content_val_dict, **params)

    def delete(self, **params):
        return super().delete(self.id, **params)

    def related_records(self, parent_module, **params):
        return super().related_records(self.id, parent_module, **params)


class ZohoConnection(_BaseConnection):
    """
    This is a fun little thing we do, below we redefine __getattr__
    so that something like ZohoConnection().Contacts will create a
    connection to the 'Contacts' Module

    The alternative is either writing dummy classes for everything - e.g.
    Contacts(), Accounts() etc

    Or having to call something like ZohoConnection().ZohoModule('Contacts')

    I'm pretty pleased with the current implementation

    ***

    In almost all use cases your code will assign an instance of ZohoConnection
    to a variable, then use that to interact with Zoho:

    >>> zc = ZohoConnection()
    >>> first_two_hundred_contacts = zc.Contacts.get_records()
    >>> zc.Accounts.insert_record({'First Name': 'Ben',
    ...                            'Last Name': 'Jarrett'})

    """
    def __getattr__(self, module):
        if module in custom_module_mapping:
            return _ModuleMethods(module=custom_module_mapping[module], session=self.session)
        return _ModuleMethods(module=module, session=self.session)
