# MIT License
#
# Copyright (c) 2016 Minimal Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

from wsgi_wovn.lang import Lang


class Headers(object):

    def __init__(self, environ, settings):
        self.__environ = environ
        self.__settings = settings
        self.protocol = environ.get('wsgi.url_scheme') or 'http'
        self.unmasked_host = environ.get('HTTP_HOST')

        if 'REQUEST_URI' not in self.__environ:
            if re.match(r'[^/]', self.__environ.get('PATH_INFO') or ''):
                self.__environ['REQUEST_URI'] = '/'
            else:
                self.__environ['REQUEST_URI'] = ''
            self.__environ[
                'REQUEST_URI'] += self.__environ.get('PATH_INFO') or ''
            if len(self.__environ.get('QUERY_STRING') or '') > 0:
                self.__environ['REQUEST_URI'] += '?' + \
                    self.__environ['QUERY_STRING']

        if re.search(r'://', self.__environ['REQUEST_URI']):
            self.__environ['REQUEST_URI'] \
                = re.sub('^.*://[^/]+', '', self.__environ['REQUEST_URI'])
        self.unmasked_pathname = self.__environ['REQUEST_URI'].split('?')[0]
        if not (re.search(r'/$', self.unmasked_pathname) or
                re.search(r'/[^/.]+\.[^/.]+$', self.unmasked_pathname)):
            self.unmasked_pathname += '/'
        self.unmasked_url = '%s://%s%s' \
            % (self.protocol, self.unmasked_host, self.unmasked_pathname)
        if settings['url_pattern'] == 'subdomain':
            self.host = self.remove_lang(
                self.__environ['HTTP_HOST'], self.lang_code())
        else:
            self.host = self.__environ.get('HTTP_HOST')
        request_uri = self.__environ['REQUEST_URI'].split('?')
        self.pathname = request_uri[0]
        if len(request_uri) >= 2:
            self.__query = request_uri[1]
        else:
            self.__query = ''
        if settings['url_pattern'] == 'path':
            self.pathname = self.remove_lang(self.pathname, self.lang_code())
        self.url = (self.host or '') + (self.pathname or '')
        if len(self.__query) > 0:
            self.url += '?'
        self.url += self.remove_lang(self.__query, self.lang_code())
        if len(settings['query']) > 0:
            query_vals = []
            for qv in settings['query']:
                pattern = r'(^|&)(?P<query_val>%s[^&]+)(&|$)' % qv
                m = re.search(pattern, self.__query)
                if m and m.group('name'):
                    query_vals.append(m.group('name'))
            if len(query_vals) > 0:
                self.__query += '?' + query_vals.sort().join('&')
        else:
            self.__query = ''
        self.__query = self.remove_lang(self.__query, self.lang_code())
        self.pathname = re.sub(r'/+$', '', self.pathname)
        self.redis_url = (self.host or '') + \
            (self.pathname or '') + (self.__query or '')

    def lang_code(self):
        if self.path_lang() and len(self.path_lang()) > 0:
            return self.path_lang()
        else:
            return self.__settings['default_lang']

    def path_lang(self):
        if not hasattr(self, '__path_lang'):
            pattern = re.compile(self.__settings.get('url_pattern_reg'))
            url = (self.__environ.get('SERVER_NAME') or '') \
                + (self.__environ.get('REQUEST_URI') or '')
            match = pattern.search(url)
            if match \
                    and match.group('lang') \
                    and Lang.get_lang(match.group('lang')):
                self.__path_lang = Lang.get_code(match.group('lang'))
            else:
                self.__path_lang = ''
        return self.__path_lang

    def browser_lang(self):
        if not self.__browser_lang:
            cookie = self.__environ['HTTP_COOKIE'] or ''
            match = re.search(
                'wovn_selected_lang\s*=\s*(?P<lang>[^;\s]+)', cookie)
            if match \
                    and match.group('lang') \
                    and Lang.get_lang(match.group('lang')):
                self.__browser_lang = match.group('lang')
            else:
                self.__brwoser_lang = ''
                accept_lang = self.__environ['HTTP_ACCEPT_LANGUAGE'] or ''
                accept_langs = re.split(r'[,;]', accept_lang)
                for l in accept_langs:
                    if Lang.get_lang(l):
                        self.__browser_lang = l
                        break
        return self.__browser_lang

    def redirect(self, lang=None):
        if not lang:
            lang = self.browser_lang()
        redirect_headers = []
        redirect_headers.append(('Location', self.redirect_location(lang)))
        redirect_headers.append(('Content-Length', 0))
        return redirect_headers

    def redirect_location(self, lang):
        if lang == self.__settings['default_lang']:
            return '%s://%s' % (self.protocol, self.url)
        else:
            location = self.url
            if self.__settings['url_pattern'] == 'query':
                if not re.search('\?', location):
                    location = '%s?wovn=%s' % (location, lang)
                elif not re.search(
                        '(\?|&)wovn=', self.__envirion['REQUEST_URI']):
                    location = '%s&wovn=%s' % (location, lang)
            elif self._settings['url_pattern'] == 'subdomain':
                location = '%s.%s' % (lang.lower(), location)
            else:
                location = re.sub('(\/|$)', '/%s/' % lang, location)
            return '%s://%s' % (self.protocol, location)

    def request_out(self, def_lang=None):
        if not def_lang:
            def_lang = self.__settings['default_lang']

        if self.__settings['url_pattern'] == 'query':
            if 'REQUEST_URI' in self.__environ:
                self.__environ['REQUEST_URI'] \
                    = self.remove_lang(self.__environ['REQUEST_URI'])
            if 'QUERY_STRING' in self.__environ:
                self.__environ['QUERY_STRING'] \
                    = self.remove_lang(self.__environ['QUERY_STRING'])
            if 'ORIGINAL_FULLPATH' in self.__environ:
                self.__environ['ORIGINAL_FULLPATH'] \
                    = self.remove_lang(self.__environ['ORIGINAL_FULLPATH'])

        elif self.__settings['url_pattern'] == 'subdomain':
            self.__environ['HTTP_HOST'] = self.remove_lang(
                self.__environ['HTTP_HOST'])
            self.__environ['SERVER_NAME'] = self.removelang(
                self.__environ['SERVER_NAME'])
            if 'HTTP_REFERER' in self.__environ:
                self.__environ['HTTP_REFERER'] \
                    = self.remove_lang(self.__environ['HTTP_REFERER'])

        else:
            self.__environ['REQUEST_URI'] = self.remove_lang(
                self.__environ['REQUEST_URI'])
            if 'REQUEST_PATH' in self.__environ:
                self.__environ['REQUEST_PATH'] \
                    = self.remove_lang(self.__environ['REQUEST_PATH'])
            self.__environ['PATH_INFO'] = self.remove_lang(
                self.__environ['PATH_INFO'])
            if 'ORIGINAL_FULLPATH' in self.__environ:
                self.__environ['ORIGINAL_FULLPATH'] \
                    = self.remove_lang(self.__environ['ORIGINAL_FULLPATH'])

        return self.__environ

    def remove_lang(self, uri, lang=None):
        if not lang:
            lang = self.path_lang()

        if self.__settings['url_pattern'] == 'query':
            uri = re.sub(r'(^|\?|&)wovn=%s(&|$)' % lang, r'\1', uri)
            return re.sub(r'(\?|&)+$', '', uri)

        elif self.__settings['url_pattern'] == 'subdomain':
            pattern = re.compile(r'(^|(//))%s\.' % lang, re.IGNORECASE)
            return pattern.sub(r'\1', uri)

        else:
            return re.sub(r'/%s(/|$)' % lang, '/', uri)

    def out(self, headers):
        new_headers = []
        for h in headers:
            if not h[0] == 'Location':
                new_headers.append(h)
                continue

            if not re.search(r'//' + self.host, h[1]):
                new_headers.append(h)
                continue

            if self.__settings['url_pattern'] == 'query':
                if re.search(r'\?', h[1]):
                    new_location = h[1] + '&'
                else:
                    new_location = h[1] + '?'

                new_location += 'wovn=' + self.lang_code()

            elif self.__settings['url_pattern'] == 'subdomain':
                new_location = re.sub(
                    r'//([^.]+)', r'//%s.\1' % self.lang_code(), h[1]
                )

            else:
                new_location = re.sub(
                    r'(//[^/]+)', r'\1/' + self.lang_code(), h[1]
                )

            new_headers.append((h[0], new_location))

        return new_headers
