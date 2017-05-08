import inspect
import logging
import re
import threading
from datetime import datetime

from django.http import HttpRequest
from django.http import JsonResponse as ApiJsonResponse
from django.http.response import HttpResponseBase

from commons import *
from . import errors


def get_post_string(request, name):
    value = request.POST.get(name)
    if value:
        return value
    return ""


def get_param_string(request, name):
    """
    find in POST, if not, then find in GET
    """
    if not request:
        return None
    value = get_post_string(request, name)
    if not value:
        return get_get_string(request, name)
    return value


def get_post_date(request, name, layout):
    value = request.POST.get(name)
    if not value:
        return None
    try:
        return datetime.strptime(value, layout)
    except:
        return None


def get_param_int(request, name, default_value=0):
    try:
        return get_post_int(request, name) if request.method == "POST" else get_get_int(request, name)
    except:
        return default_value


def get_post_int(request, name):
    value = request.POST.get(name)
    if value:
        return int(value)
    return 0


def get_get_string(request, name):
    value = request.GET.get(name)
    if value:
        return value
    return ""


def get_get_int(request, name):
    value = request.GET.get(name)
    if value:
        return int(value)
    return 0


def get_cookie_string(request, name):
    if not request:
        return ""
    value = request.COOKIES.get(name)
    if value:
        return value
    return ""


def get_cookie_int(request, name):
    value = request.COOKIES.get(name)
    if value:
        return int(value)
    return 0


def get_header(request, name):
    return request.META.get('HTTP_' + name.upper())


request_context = threading.local()


def get_client_ip(request):
    """
    从请求拿到用户的ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _parse_request(anonymous, get_response, request):
    ctx = get_request_context()
    sig = inspect.signature(get_response)
    args = []
    for p in sig.parameters:
        if "request" == p:
            args.append(request)
        elif "user_id" == p:
            user_id = ctx.user_id

            if not anonymous and not user_id:
                raise ApiException(errors.SESSION_INVALID, "请先登录")

            args.append(user_id)
        elif p.startswith("header_"):
            args.append(get_header(request, p[7:]))
        elif "request_context" == p:
            args.append(request_context.ctx)
        else:
            if p.startswith('i_'):
                args.append(get_param_int(request, p[2:]))
            else:
                args.append(get_param_string(request, p))
    return args


def get_request_context(request=None):
    if request and hasattr(request, 'context'):
        return request.context
    return request_context.ctx if hasattr(request_context, 'ctx') else _dummy


def api_func(get_response):
    def middleware(*args):
        if len(args) == 1 and isinstance(args[0], HttpRequest):
            return _process_api(get_response, *args)
        else:
            get_response(*args)

    return middleware


def api_func_anonymous(get_response):
    def middleware(*args):
        if len(args) == 1 and isinstance(args[0], HttpRequest):
            return _process_api(get_response, *args, anonymous=True)
        else:
            get_response(*args)

    return middleware


def init_request_context(request):
    if not request:
        return _dummy
    if not hasattr(request_context, 'request') or request != request_context.request:
        request_context.request = request
        ctx = RequestContext(request)
        request_context.ctx = ctx

    return request_context.ctx


def _process_api(get_response, request, anonymous=False):
    if not hasattr(request_context, 'ctx'):
        init_request_context(request)

    ctx = get_request_context()
    if not anonymous and ctx.is_anonymous():
        return JsonResponse(data={
            'return_code': errors.SESSION_INVALID,
            'return_message': '请登陆'
        })

    # if request.path_info.startswith('/api') or request.path_info.startswith('/cms/api'):
    try:
        args = _parse_request(anonymous, get_response, request)
        response = get_response(*args)
    except ApiException as e:
        response = api_response(data={}, return_code=e.code, return_msg=e.message)
    # else:
    #     return get_response(request)
    if isinstance(response, HttpResponseBase):
        return response
    if response and hasattr(response, 'dict'):
        response = response.dict()

    if not response or 'return_code' not in response:
        response = api_response(response)
    return JsonResponse(data=response)


class JsonResponse(ApiJsonResponse):
    def __init__(self, data, **kwargs):
        self.data = data
        super(JsonResponse, self).__init__(data, **kwargs)


def get_client_platform(request):
    """

    extract platform from useragent
    ios, android, web, wechat
    """

    if hasattr(request_context, 'ctx'):
        return request_context.ctx.platform

    userAgent = request.META.get('HTTP_USER_AGENT', '').upper()
    app = get_param_string(request, 'app')

    # header.put("User-Agent", "volley/1.0.0 Android HJC/" + BuildConfig.VERSION_NAME);; 这是安卓的生成方式
    # webview ua: settings.getUserAgentString() + " Android HJC/" + BuildConfig.VERSION_NAME; 安卓webview生成方式
    # and re.match('^([1-9]+)([0-9.]?)([0-9]+)$', userAgent.split('/')[-1]) is not None
    # 这里需要区分出 安卓app, 安卓app内webview, 安卓手机浏览器, pc手机浏览器

    if 'MicroMessenger'.upper() in userAgent:
        return PLATFORM_WX
    elif 'ANDROID' in userAgent:
        return PLATFORM_ANDROID
    elif ('IOS' in userAgent) or ('IPHONE' in userAgent) or ('CFNETWORK' in userAgent):
        return PLATFORM_IOS
    else:
        return PLATFORM_WEB


def get_session_id(request):
    session_id = get_param_string(request, "session_id")
    if session_id == "":
        session_id = get_cookie_string(request, "session_id")
    return session_id


def get_scheme(request):
    host = request.get_host()
    if 'com' in host and 'test' not in host:
        return 'https'
    return 'http'


class RequestContext:
    def is_anonymous(self):
        return self.user_id is None or self.user_id == 0

    def __init__(self, request=None):
        self.device_guid = ''
        self.request = request

        if not request:
            return
        self.ua = request.META.get('HTTP_USER_AGENT', '') if request else ""
        self.platform = get_client_platform(request) if request else ""
        self.app = get_param_string(request, 'app') if request else ""

        self.version = ""

        self.is_in_app = False

        if not self.app:
            self.app = 'miaojie'

        self.ip = get_client_ip(request) if request else ""
        self.device_guid = get_param_string(request, 'device_guid')
        self.client_type = 'b' if self.app.endswith('_b') else 'c'
        self.session_id = get_session_id(request)
        self.user_id = 0
        self.created_at = datetime.now()
        self.host = request.get_host() if request else ""
        self.scheme = get_scheme(request) if request else ""
        self.method = request.method if request else ""
        self.path = request.get_full_path() if request else ""
        self.version_code = get_param_int(request, 'version_code', 0)

        self.is_wx = "MicroMessenger" in self.ua

        try:
            if self.platform == PLATFORM_ANDROID:
                # volley/1.0.0 79kjA jiyongqian_c JYQDK/1.1.2
                if '79kjA' in self.ua:
                    self.is_in_app = True
                    elems = self.ua.split(' ')
                    if len(elems) > 3:
                        if not self.app:
                            self.app = elems[2]
                        elems__split = elems[3].split('/')
                        if len(elems__split) > 1:
                            self.version = elems__split[1]
                        else:
                            logger.info("ua - %s " % self.ua)

                        result = re.search('\\[(.+?)\\]', self.ua)
                        if result:
                            self.phone = result.group(1)

            elif self.platform == PLATFORM_IOS:
                if '79kjI' in self.ua:
                    self.is_in_app = True
                    elems = self.ua.split(' ')
                    if len(elems) > 2:
                        if not self.app:
                            self.app = elems[1]
                        elems__split = elems[2].split('/')
                        if len(elems__split) > 1:
                            self.version = elems__split[1]
                        else:
                            logger.info("ua - %s " % self.ua)

                        result = re.search('\\[(.+?)\\]', self.ua)
                        if result:
                            self.phone = result.group(1)

        except Exception as e:
            logger.warning("error parse {}".format(e), exc_info=True)


### response

def api_params_invalid_json_response(return_msg):
    return JsonResponse(data=api_response({}, return_code=errors.PARAM_INVALID, return_msg=return_msg))


def api_response(data, return_code=0, return_msg='ok'):
    """

    :param data:  dict or list
    :param return_code:
    :param return_msg:
    :return:
    """
    return ResultItem(return_code=return_code, return_msg=return_msg, data=data)


def api_error(return_code, return_msg='错误'):
    raise ApiException(return_code, return_msg)


def api_err_response(return_msg):
    return ResultItem(return_code=errors.PARAM_INVALID, return_msg=return_msg, data={})


def json_response(api_handle_func):
    return api_json_handler_wrapper(api_handle_func)


def api_json_handler_wrapper(api_handle_func):
    """

    返回一个将返回json的函数包装成返回json response的函数
    """

    def wrapper(*args, **kwargs):
        data = api_handle_func(*args, **kwargs)
        if isinstance(data, JsonResponse):
            return data

        if not data or 'return_code' not in data:  ## 不是api response
            data = api_response(data)

        response = JsonResponse(data=data)
        if data["return_code"] == errors.SESSION_INVALID:
            # clear_session_cookie(response)
            pass

        # if data["return_code"] != 0:
        #     logger.warn("path {0}, params {1}, return {2}".format(request.path, request.POST, data))
        return response

    return wrapper


_dummy = RequestContext()
logger = logging.getLogger(__name__)
