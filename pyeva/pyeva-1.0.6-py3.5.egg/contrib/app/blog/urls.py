from tornado.web import url

from .user import views as user_views
from .console import views as console_views
from .admin import views as admin_views


handlers = [

    # user
    url(r'/blog/article', user_views.ArticleHandler),
    url(r'/blog/article/([\-0-9a-zA-Z]+)', user_views.SingleArticleHandler),

    # console
    url(r'/console/blog/statistics', console_views.StatisticsHandler),
    url(r'/console/blog/catalog', console_views.CatalogHandler),
    url(r'/console/blog/catalog/([\-0-9a-zA-Z]+)', console_views.SingleCatalogHandler),
    url(r'/console/blog/article', console_views.ArticleHandler),
    url(r'/console/blog/article/([\-0-9a-zA-Z]+)', console_views.SingleArticleHandler),
    url(r'/console/blog/tag', console_views.TagHandler),
    url(r'/console/blog/tag/([\-0-9a-zA-Z]+)', console_views.SingleTagHandler),

    # admin
    url(r'/admin/blog/category', admin_views.CategoryHandler),

]
