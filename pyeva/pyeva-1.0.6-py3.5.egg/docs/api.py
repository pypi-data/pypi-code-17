import sys
import logging
import pprint

import yaml
import tornado.web

from eva.docs.template import find_template


# https://www.python.org/dev/peps/pep-0257/
def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize  # python3
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


class TornadoHandlerApi(object):
    '''
    Tornado Handler API接口文档
    '''

    def __init__(self, handler, url_regex=None):
        self.handler = handler
        self.url_regex = url_regex

    def get_docs(self):
        '''生成html文档'''

        if not issubclass(self.handler, tornado.web.RequestHandler):
            raise Exception('not tornado handler!')

        docs = []

        handler_methods = vars(self.handler)
        for m in ['get', 'post', 'put', 'delete']:

            # 检查 method 是否定义于该 Handler (不检查父类定义)
            if m not in handler_methods:
                continue

            apidata = ApiData(self.url_regex, self.handler, m)
            docs.append(apidata)

        return docs


class ApiData(object):
    '''描述单个 API 的接口文档'''

    def __init__(self, url, handler, method):
        self.url = url
        self.handler = handler
        self.method = method
        self.html_template = find_template('api.html')

    @property
    def fullname(self):
        return '{module}.{name}.{method}'.format(**{
            'module': self.handler.__module__,
            'name': self.handler.__name__,
            'method': self.method
        })

    def get_url(self):
        return self.data["request"]["url"]

    def get_yaml_data(self):

        docstring = getattr(self.handler, self.method).__doc__
        if not docstring:
            logging.warn('%s: no docstring, PASS',
                         self.fullname)
            return

        try:
            docstring = trim(docstring)
            # print(docstring)
            Y = yaml.load(docstring)
        except Exception as e:
            logging.warn(
                'load YAML data from %s.__doc__ failed: %s',
                self.fullname, e, exc_info=True)

        if not isinstance(Y, dict):
            logging.warn('%s: can not find yaml data in docstring, PASS',
                         self.fullname)
            return

        if 'request' not in Y:
            Y['request'] = {}

        # 检查并自动完成常用值
        if isinstance(Y['request'], dict):
            if 'url' not in Y['request']:
                Y['request']['url'] = self.url
            if 'method' not in Y['request']:
                Y['request']['method'] = self.method

        return Y

    def get_html(self):
        return self.html_template.render(**self.get_yaml_data())


if __name__ == '__main__':
    from apps.auth.user.views import SignIn
    api = TornadoHandlerApi(handler=SignIn)
    for doc in api.get_docs():
        pprint.pprint(doc.get_yaml_data())
        print(doc.get_html())
