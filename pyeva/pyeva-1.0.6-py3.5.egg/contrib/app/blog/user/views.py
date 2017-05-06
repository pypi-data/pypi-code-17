from sqlalchemy import and_

from eva.web import APIRequestHandler, authenticated
from eva.utils.translation import ugettext_lazy as _
from eva.sqlalchemy.list import simple_list_objects, get_filters

from app.blog.models import (
    BlogArticle
)


class ArticleHandler(APIRequestHandler):

    def get(self):
        '''文章列表'''

        q = self.db.query(BlogArticle).filter_by(
            is_public=True)
        d = simple_list_objects(self, BlogArticle, q)
        self.success(**d)


class SingleArticleHandler(APIRequestHandler):

    def get(self, uid):
        '''查看文章'''

        article = self.db.query(BlogArticle).filter(
            and_(BlogArticle.uid == uid,
                 BlogArticle.is_public == True)).first()
        if not article:
            return self.fail_404(_("No such article"))

        self.success(**article.iuser)
