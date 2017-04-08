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
import urllib.parse
from urllib.parse import urlparse

import lxml.html

from wsgi_wovn.headers import Headers
from wsgi_wovn.lang import Lang
from wsgi_wovn.store import Store
import wsgi_wovn.version


class Middleware(object):

    def __init__(self, application, opts={}):
        self.application = application
        self.__store = Store()
        self.__store.settings(opts)

    def __call__(self, environ, start_response):
        if not self.__store.is_valid_settings():
            return self.application(environ, start_response)

        self.__environ = environ
        h = Headers(environ, self.__store.settings())
        if self.__store.settings().get('test_mode') \
                and self.__store.settings().get('test_url') != h.url:
            return self.application(environ, start_response)

        if h.path_lang() == self.__store.settings().get('default_lang'):
            redirect_headers = h.redirect(
                self.__store.settings().get('default_lang'))
            start_response('307 Temporary Redirect', redirect_headers)
            return ''

        l = h.lang_code()

        res_status_headers = []

        def local_start(stat_str, head=[]):
            res_status_headers.append({
                'status': stat_str,
                'headers': head
            })

        res = self.application(h.request_out(), local_start)

        # error?
        if len(res_status_headers) == 0:
            start_response('', [])
            return res

        res_status = res_status_headers[0]['status']
        res_headers = res_status_headers[0]['headers']

        if self.__is_html(res_headers) and not re.match(r'1|302', res_status):
            values = self.__store.get_values(h.redis_url)
            url = {
                'protocol': h.protocol,
                'host': h.host,
                'pathname': h.pathname
            }
            res = self.switch_lang(res, values, url, l, h)
            res_headers = self.__set_content_length_to_headers(
                res, res_headers)

        res_headers = h.out(res_headers)
        start_response(res_status, res_headers)
        return res

    def __is_html(self, head):
        for h in head:
            if h[0] == 'Content-Type':
                if re.search(r'html', h[1]):
                    return True
                else:
                    return False
        return False

    def __set_content_length_to_headers(self, res, head):
        new_h = []
        for h in head:
            if h[0] == 'Content-Length':
                new_h.append((h[0], self.__new_content_length(res)))
            else:
                new_h.append(h)
        return new_h

    def __new_content_length(self, res):
        content_length = 0
        for r in res:
            content_length += len(r)
        return content_length

    def add_lang_code(self, href, pattern, l, h):
        if re.match(r'(#.*)?$', href):
            return href

        new_href = href

        p = re.compile(r'(https?:)?//', re.IGNORECASE)
        if href and p.match(href):
            uri = urlparse(href)

            if uri.hostname.lower() == h['host'].lower():
                if pattern == 'subdomain':
                    matched = re.search(r'//([^\.]*)\.', href)
                    sub_d = None
                    if matched:
                        sub_d = matched.group(1)
                    sub_code = Lang.getCode(sub_d)
                    if sub_code and sub_code.lower() == l.lower():
                        p = re.compile(l, re.IGNORECASE)
                        new_href = p.sub(l.lower(), href)
                    else:
                        new_href = re.sub(
                            r'(//)([^\.]*)', r'\1%s.\2' % l.lower(), href)

                elif pattern == 'query':
                    if re.search(r'\?', href):
                        new_href = href + '&wovn=' + l
                    else:
                        new_href = href + '&wovn=' + l

                else:
                    new_href = re.sub(
                        r'([^\.]*\.[^/]*)(/|$)', r'\1/%s/' % l, href)

        elif href:
            if pattern == 'subdomain':
                lang_url = h.protocol + '://' + l.lower() + '.' + h.host
                current_dir = re.sub(r'[^/]*\.[^\.]{2,6}$', '', h.pathname)
                if re.match(r'\.\..*$', href):
                    new_href = lang_url + '/' + re.sub(r'^\.\.\/', '', href)

                elif re.match(r'\..*$', href):
                    new_href = lang_url + current_dir + \
                        '/' + re.sub(r'^\./', '', href)

                elif re.match(r'/.*$', href):
                    new_href = lang_url + href

                else:
                    new_href = lang_url + current_dir + '/' + href

            elif pattern == 'query':
                if re.search(r'\?', href):
                    new_href = href + '&wovn=' + l
                else:
                    new_href = href + '?wovn=' + l

            else:
                if re.match(r'/', href):
                    new_href = '/' + l + href
                else:
                    current_dir = re.sub(r'[^/]*\.[^\.]{2,6}$', '', h.pathname)
                    new_href = '/' + l + current_dir + href

        return new_href

    def check_wovn_ignore(self, node):
        if node is None:
            return False
        elif node.get('wovn-ignore') is not None:
            return True
        elif node.get('name') == 'html':
            return False
        return self.check_wovn_ignore(node.getparent())

    def switch_lang(self, body, values, url, l, h):
        if l is None or l == '':
            l = self.__store.settings().get('default_lang')

        l = Lang.get_code(l)
        text_index = values.get('text_vals') or {}
        src_index = values.get('img_vals') or {}
        img_src_prefix = values.get('img_src_prefix') or ''
        ignore_all = False
        # string_index = {}
        new_body = []

        for b in body:
            d = lxml.html.fromstring(b)

            if ignore_all or len(d.xpath('//html[@wovn-ignore]')) > 0:
                ignore_all = True
                html = lxml.html.tostring(d)

                def repl(matchobj):
                    return b'href="%s"' \
                        % urllib.parse.unquote(matchobj.group(1))
                html = re.sub(b'href="([^"]*)"', repl, html)
                new_body.append(html)
                continue

            if not l == self.__store.settings().get('default_lang'):
                pattern = self.__store.settings().get('url_pattern')

                for a in d.xpath('//a'):
                    if self.check_wovn_ignore(a):
                        continue
                    href = a.get('href')
                    new_href = self.add_lang_code(href, pattern, l, h)
                    a.set('href', new_href)

                for f in d.xpath('//form'):
                    if self.check_wovn_ignore(a):
                        continue
                    method = f.get('method')
                    if pattern == 'query' \
                            and (method is None or method.upper() == 'GET'):
                        tag = lxml.html.Element('input')
                        tag.set('type', 'hidden')
                        tag.set('name', 'wovn')
                        tag.set('value', l)
                        if len(list(f)) > 0:
                            f.insert(0, tag)
                        else:
                            f.append(tag)
                    else:
                        action = f.get('action')
                        new_action = self.add_lang_code(action, pattern, l, h)
                        f.set('action', new_action)

                for t in d.xpath('//text()'):
                    t = t.getparent()
                    if self.check_wovn_ignore(t):
                        continue
                    node_text = t.text.strip()
                    if node_text in text_index and l in text_index[node_text] \
                            and len(text_index[node_text][l]) > 0:
                        new_content = re.sub(
                            r'^(\s*)[\S\s]*(\s*)$',
                            '\1' +
                            text_index[node_text][l][0]['data'] + '\2'
                        )
                        t.text_content(new_content)

                for m in d.xpath('//meta'):
                    if self.check_wovn_ignore(m):
                        continue
                    meta_data = m.get('name') or m.get('property') or ''
                    meta_data_types = (
                        'description',
                        'title',
                        'og:title',
                        'og:description',
                        'twitter:title',
                        'twitter:description',
                    )
                    if meta_data not in meta_data_types:
                        continue
                    node_content = m.get('content').strip()
                    if node_content in text_index \
                            and l in text_index[node_content] \
                            and len(text_index[node_content][l]) > 0:
                        new_content = re.sub(
                            r'^(\s*)[\S\s]*(\s*)$',
                            '\1' +
                            text_index[node_content][l][0]['data'] + '\2'
                        )
                        m.set('content', new_content)

                for i in d.xpath('//img'):
                    if self.check_wovn_ignore(i):
                        continue

                    src = i.get('src')
                    if len(src) > 0:
                        if not re.search(r'://', src):
                            if re.match(r'/', src):
                                src = url['protocol'] + \
                                    '://' + url['host'] + src
                            else:
                                src = url['protocol'] + '://' + \
                                    url['host'] + url['path'] + src

                        if src in src_index and l in src_index[src] \
                                and len(src_index[src][l]) > 0:
                            new_src = img_src_prefix + \
                                src_index[src][l][0]['data']
                            i.set('src', new_src)

                    if len(i.get('alt') or '') > 0:
                        alt = i.get('alt').strip()
                        if alt in text_index and l in text_index[alt] \
                                and len(text_index[alt][l]) > 0:
                            new_alt = re.sub(
                                r'^(\s*)[\S\s]*(\s*)$',
                                '\1' + text_index[alt][l][0]['data'] + '\2'
                            )
                            i.set('alt', new_alt)

            for s in d.xpath('//script'):
                src = s.get('src')
                if len(src) > 0 and re.search(
                        r'//j.(dev-)?wovn.io(:3000)?/',
                        src
                ):
                    s.remove()

            head = d.xpath('//head')
            if head:
                parent_node = head[0]
            else:
                b = d.xpath('//body')
                if b:
                    parent_node = b[0]

            insert_node = lxml.html.Element('script')
            insert_node.set('src', '//j.wovn.io/1')
            insert_node.set('async', '')
            data = {
                'key': self.__store.settings().get('user_token'),
                'backend': 'true',
                'currentLang': l,
                'defaultLang': self.__store.settings().get('default_lang'),
                'urlPattern': self.__store.settings().get('url_pattern'),
                'version': wsgi_wovn.version.VERSION
            }
            data_array = []
            for key, value in data.items():
                data_array.append(key + '=' + value)
            insert_node.set('data-wovnio', '&'.join(data_array))
            insert_node.text = ' '

            if len(list(parent_node)) > 0:
                parent_node.insert(0, insert_node)
            else:
                parent_node.append(insert_node)

            for ll in self.get_langs(values):
                insert_node = lxml.html.Element('link')
                insert_node.set('rel', 'alternate')
                insert_node.set('hreflang', l)
                insert_node.set('href', h.redirect_location(l))
                parent_node.append(insert_node)

            def repl(matchobj):
                s = b'href="%s"' % urllib.parse.unquote(
                    matchobj.group(1).decode('utf-8')).encode('utf-8')
                return s
            output = re.sub(b'href="([^"]*)"', repl, lxml.html.tostring(d))
            new_body.append(output)

        return new_body

    def get_langs(self, values):
        langs = []
        text_vals = values.get('text_vals') or {}
        for v in text_vals.values():
            for k in v.keys():
                langs.append(k)
        img_vals = values.get('img_vals') or {}
        for v in img_vals.values():
            for k in v.keys():
                langs.append(k)
        return set(langs)
