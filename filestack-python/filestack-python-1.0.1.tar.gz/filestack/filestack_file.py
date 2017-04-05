import mimetypes
import json
import re
import os

try:
    import urllib.parse as parser
except ImportError:
    import urllib as parser

import requests

from .filestack_policy import FilestackPolicy
from .version import __version__


class FilestackFile(object):

    FILE_API_URL = 'https://cdn.filestackcontent.com/'
    METADATA_ATTRS = ['size', 'mimetype', 'filename', 'width',
                      'height', 'uploaded', 'writeable', 'md5',
                      'location', 'path', 'container', 'key']

    HEADERS = {'User-Agent': 'filestack-python {}'.format(__version__)}

    def __init__(self, handle=None, url=None, api_key=None, response_dict=None,
                  app_secret=None, policies={}, **kwargs):

        self.metadata = None

        if handle:
            self.__init_with_handle(handle=handle)
        elif url:
            self.url = url
            try:
                self.__get_handle()
            except:
                raise Exception('To init with url, please provide either a '
                                'https://cdn.filestackcontent/file_handle or '
                                'https://www.filestackapi.com/api/'
                                'file/file_handle')
        elif response_dict:
            self.__init_with_dict(response_dict)
        else:
            raise Exception('Please provide either a file handle, '
                            'a Python dictionary, or a Filestack url')

        self.policies = policies
        self.handle = handle or self.__get_handle()
        self.set_api_key(api_key)
        self.set_app_secret(app_secret)

    def __init_with_dict(self, d):
        if 'url' in d:
            self.url = d['url']
        elif 'handle' in d:
            self.url = self.FILE_API_URL + d['handle']
        else:
            raise Exception('Please define either a file handle or a url')
        if d.get('type'):
            d['mimetype'] = d.pop('type')
            self.metadata = d

    def __init_with_handle(self, handle):
        self.handle = handle
        self.url = self.FILE_API_URL + handle
        self.metadata = {}

    def __get_handle(self):
        self.url = parser.unquote(self.url)
        try:
            return re.match(r'(?:https:\/\/)'
                            r'(?:www\.|cdn\.)'
                            r'(?:file\w+\.\w+)'
                            r'(?:\/api\/file\/|\w+\/)'
                            r'(\w+)',self.url).group(1)

        except:
            raise Exception("Invalid file url")

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_app_secret(self, secret):
        self.app_secret = secret

    def update_metadata(self, policy_name=None):
        params = dict((x, 'true') for x in self.METADATA_ATTRS)
        if policy_name:
            params.update(self.policies[policy_name].signature_params())
        response = requests.get(self.url + '/metadata', params=params,
                                headers=self.HEADERS)
        try:
            self.metadata = json.loads(response.text)
        except ValueError:
            self.metadata = {}
            raise Exception("Failed to retrieve metadata")

    def delete(self, policy_name=None, api_key=None):
        if api_key:
            self.set_api_key(api_key)
        elif self.api_key is None:
            raise Exception("An API key is required, set it with set_api_key "
                            "method or pass it as a parameter in delete method")

        if policy_name is None:
            raise Exception("A policy_name is required when "
                            "using the delete method")
        else:
            try:
                policy = self.policies[policy_name].signature_params()['policy']
                signature = self.policies[policy_name].signature_params()['signature']
                url = ('https://www.filestackapi.com/api/file/{}?key={}&policy='
                      '{}&signature={}').format(self.handle,self.api_key,
                       policy, signature)
                return requests.delete(url)
            except:
                raise Exception(("Failed to find a policy with the name: "
                                "{}").format(policy_name))


    def download(self, destination_path=None, policy_name=None):
        if destination_path is None:
            raise Exception("Please Provide a destination_path")
        url = self.get_signed_url(policy_name) if policy_name else self.url
        with open(destination_path, 'wb') as f:
            response = requests.get(url, stream=True, headers=self.HEADERS)
            if response.ok:
                for chunk in response.iter_content(1024):
                    if not chunk:
                        break # pragma: no cover
                    f.write(chunk)
            return response

    def overwrite(self, url=None, filepath=None,
                  policy_name=None, data=None, files=None):
        if policy_name is None:
            raise Exception("A policy_name is required when "
                            "using the overwrite method")
        else:
            if url:
                data = {'url': url}
            elif filepath:
                filename = os.path.basename(filepath)
                mimetype = mimetypes.guess_type(filepath)[0]
                files = {'fileUpload': (filename,open(filepath,'rb'),mimetype)}
            else:
                raise Exception("A url or filepath is required when "
                                "using the overwrite method")
            self.url = self.get_signed_url(policy_name)
            return self.__post(self.url, data=data, files=files,
                               policy_name=policy_name)

    def convert(self, conversion=None, api_key=None, handle=None,
                no_api_key=False, policy_name=None, storage_task=None):
        if not conversion:
            raise Exception("Please provide conversion task(s)")

        if not api_key:
            if self.api_key is None:
                raise Exception("An API key is required, set it with "
                                "set_api_key method or pass it as a"
                                "parameter in convert method")
        else:
            self.api_key = api_key

        if not handle:
            if self.handle is None:
                raise Exception("A file handle is required, "
                                "try passing it as a parameter")
        else:
            self.handle = handle

        if no_api_key:
            if policy_name:
                if storage_task:
                    return self.__post(('https://process.filestackapi.com/'
                                        'security=policy:{},signature:'
                                        '{}/{}/store={}/{}').format(self.policies[policy_name].signature_params()['policy'],
                                                                    self.policies[policy_name].signature_params()['signature'],
                                                                    conversion,storage_task,self.handle))
                else:
                    return ('https://process.filestackapi.com/security=policy:'
                    '{},signature:{}/{}/{}').format(self.policies[policy_name].signature_params()['policy'],
                                                  self.policies[policy_name].signature_params()['signature'],
                                                  conversion,self.handle)
            else:
                if storage_task:
                    return self.__post(('https://process.filestackapi.com/'
                                        '{}/store={}/{}').format(conversion,
                                                                  storage_task,
                                                                  self.handle))
                else:
                    return ('https://process.filestackapi.com/{}/{}').format(conversion,
                                                                             self.handle)
        else:
            if policy_name:
                if storage_task:
                    return self.__post(('https://process.filestackapi.com/{}/'
                                        'security=policy:{},signature:'
                                        '{}/{}/store={}/{}').format(self.api_key,
                                                                    self.policies[policy_name].signature_params()['policy'],
                                                                    self.policies[policy_name].signature_params()['signature'],
                                                                    conversion,storage_task,self.handle))
                else:
                    return self.__post(('https://process.filestackapi.com/{}/'
                                        'security=policy:{},signature:'
                                        '{}/{}/{}').format(self.api_key,
                                                           self.policies[policy_name].signature_params()['policy'],
                                                           self.policies[policy_name].signature_params()['signature'],
                                                           conversion,self.handle))
            else:
                if storage_task:
                    return self.__post(('https://process.filestackapi.com/{}/'
                                        '{}/store={}/{}').format(self.api_key,
                                                                 conversion,
                                                                 storage_task,
                                                                 self.handle))
                else:
                    return ('https://process.filestackapi.com/{}/{}/{}').format(self.api_key,
                                                                                conversion,
                                                                                self.handle)

    def add_policy(self, name, policy):
        if self.app_secret is None:
            raise Exception("Please set app secret first")
        self.policies[name] = FilestackPolicy(policy, self.app_secret)

    def get_signed_url(self, policy_name):
        params = self.policies[policy_name].signature_params()
        return self.url + '?' + parser.urlencode(params)

    def __post(self, url, data=None, files=None, policy_name=None, **kwargs):
        headers = {'User-Agent': 'filestack-python {}'.format(__version__)}
        try:
            r = requests.post(url, data=data, files=files,
                              params=kwargs.get('params'),
                              headers=headers)
            rd = json.loads(r.text)

            if policy_name is not None:
                rd['url'] = self.get_signed_url(policy_name)

            return FilestackFile(
                    response_dict=rd, api_key=self.api_key,
                    app_secret=self.app_secret,
                    policies=self.policies)
        except requests.exceptions.ConnectionError as e: # pragma: no cover
            raise e # pragma: no cover

    def __getattribute__(self, name):
        attrs = super(FilestackFile, self).__getattribute__('METADATA_ATTRS')
        if name in attrs:
            return super(FilestackFile, self) \
                      .__getattribute__('metadata').get(name)
        else:
            return super(FilestackFile, self).__getattribute__(name)
