import logging
import tornado.web
import tornado.httpclient
from tornado.web import asynchronous
from mako.exceptions import RichTraceback

from eva.conf import settings
from eva.api import API


class RequestHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(RequestHandler, self).__init__(
            application, request, **kwargs)
        self.template_path = None
        self.title = None
        self.data = {}
        self._api = None

    def render_string(self, template_path, **kwargs):
        namespace = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            # locale=self.locale,
            # _=self.locale.translate,
            # pgettext=self.locale.pgettext,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url,
            # custom
            s=lambda x: u"\"{0}\"".format(x),
        )

        # 如果标题未设置，设置一个默认值
        if self.title:
            namespace['title'] = self.title
        else:
            namespace['title'] = settings.DEFAULT_HTML_TITLE

        namespace.update(self.data)
        namespace.update(kwargs)

        try:
            html = self.application.template_lookup.get_template(
                template_path).render(**namespace)
        except:
            html = self.application.template_lookup.get_template(
                'mako_failed.html').render(
                    traceback=RichTraceback())

        return html

    def render(self, template_path=None, **kwargs):
        if not template_path:
            template_path = self.template_path
        html = self.render_string(template_path, **kwargs)
        self.finish(html)

    def static_url(self, path, app=None):
        '''静态文件地址

        Tornado 的 static_url 扩展。但不计算 version，可由 nginx 提供。

        支持指定 app，获取其 static 文件 url
        '''

        if app:
            url = None
            data = self.settings.get('app_static_urls')
            if data:
                url = data.get(app)

            # 默认 url
            if not url:
                url = '/{0}/static/'.format(app)

            url += path
        else:
            url = self.settings.get('static_url_prefix', '/static/') + path

        return url

    def get(self):
        '''提供默认的 HTTP GET 请求

        Python不太爱隐藏细节，但是程序员很懒。
        '''
        if self.template_path:
            self.render()
        else:
            # 可能 Handler 没有提供 get 方法
            logging.error('Can not find template_path in get method!')
            raise tornado.web.HTTPError(405)

    @property
    def api(self):
        if not self._api:
            self._api = API(url_prefix=settings.API_URL_PREFIX,
                            sid=self.get_cookie('SID'))
        return self._api

    # TODO: 默认不必放在这里
    @property
    def r(self):
        return self.application.r

    def update_errors(self, api_response):
        '''更新错误信息'''

        # TODO

        if not hasattr(api_response, 'error'):
            return

        self.data['error'] = api_response.error
        if hasattr(api_response, 'errors'):
            if 'form' in self.data:
                self.data["form"].errors = api_response.errors
            else:
                self.data["errors"] = api_response.errors

    def get_current_user(self):
        profile = self.api.get('/console/account/profile')
        if hasattr(profile, 'error'):
            return None
        return profile



class ForwardingRequestHandler(tornado.web.RequestHandler):
    '''转发处理
    '''

    def initialize(self, host, port, permanent=True, url_prefix='/'):
        self._host = host
        self._port = port
        self._permanent = permanent
        self._uri_prefix = url_prefix

    def prepare(self):
        self._uri = self._uri_prefix + self.path_args[0]
        if self.request.query:
            self._uri = self._uri + '?' + self.request.query

    @asynchronous
    def get(self, uri):
        self.forward(host=self._host, port=self._port, uri=self._uri)

    @asynchronous
    def post(self, uri):
        self.forward(host=self._host, port=self._port, uri=self._uri)

    @asynchronous
    def put(self, uri):
        self.forward(host=self._host, port=self._port, uri=self._uri)

    @asynchronous
    def delete(self, uri):
        self.forward(host=self._host, port=self._port, uri=self._uri)

    def handle_response(self, response):
        if response.error and not isinstance(response.error,
                                             tornado.httpclient.HTTPError):
            logging.error("response has error %s", response.error)
            self.set_status(500)
            self.write("Internal server error:\n" +
                       str(response.error))
            self.finish()
        else:
            self.set_status(response.code)
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            if response.body:
                self.write(response.body)
            self.finish()

    def forward(self, host=None, port=None, uri=None):
        try:
            tornado.httpclient.AsyncHTTPClient().fetch(
                tornado.httpclient.HTTPRequest(
                    url="%s://%s:%s%s" % (
                        self.request.protocol, host or "127.0.0.1",
                        port or 3000, uri or self.request.uri),
                    method=self.request.method,
                    body=self.request.body,
                    headers=self.request.headers,
                    allow_nonstandard_methods=True,
                    follow_redirects=False),
                self.handle_response)
        except tornado.httpclient.HTTPError as x:
            logging.error("tornado signalled HTTPError %s", x)
            if hasattr(x, response) and x.response:
                self.handle_response(x.response)
        except tornado.httpclient.CurlError as x:
            logging.error("tornado signalled CurlError %s", x)
            self.set_status(500)
            self.write("Internal server error:\n" +
                       ''.join(traceback.format_exception(*sys.exc_info())))
            self.finish()
        except:
            self.set_status(500)
            self.write("Internal server error:\n" +
                       ''.join(traceback.format_exception(*sys.exc_info())))
            self.finish()
