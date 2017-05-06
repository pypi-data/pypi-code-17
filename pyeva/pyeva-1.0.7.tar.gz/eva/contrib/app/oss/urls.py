# coding: utf-8

from tornado.web import url, StaticFileHandler

from eva.conf import settings

from . import views

handlers = [

    # 静态文件，生产环境使用 nginx 部署！
    (settings.OSS_STATIC_URL_PREFIX + '(.*)', StaticFileHandler, {'path': settings.OSS_PATH}),

    # imditor 上传图片的定制 API
    url(r'/oss/simditor_image_upload',
        views.SimditorImageUpload),

]
