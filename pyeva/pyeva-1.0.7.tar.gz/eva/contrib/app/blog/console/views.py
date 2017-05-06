import datetime

from sqlalchemy import and_
from sqlalchemy.orm.exc import (
    NoResultFound,
    MultipleResultsFound,
)

from eva.web import APIRequestHandler as _APIRequestHandler, authenticated
from eva.utils.translation import ugettext_lazy as _
from eva.sqlalchemy.list import owner_list_objects, get_filters
from eva.exceptions import EvaError

from app.blog.models import (
    BlogCategory,
    BlogCatalog,
    BlogArticle,
    BlogComment,
    BlogTag
)
from .forms import (
    CatalogNewForm,
    CatalogEditForm,
    ArticleNewForm,
    ArticleEditForm,
    TagNewForm,
    TagEditForm
)


class APIRequestHandler(_APIRequestHandler):

    def get_my_obj(self, model, uid):
        try:
            return self.db.query(model).filter(
                and_(
                    model.user_id == self.current_user.id,
                    model.uid == uid
                )).one()

        except NoResultFound:
            raise EvaError(_("can not find {0} with uid {1}").format(
                model.__tablename__, uid))

        except MultipleResultsFound:
            # 不应该出现
            raise EvaError(
                _("found duplicate objects for {0}").format(model.__tablename__))

    def get_my_category(self, uid):
        return self.get_my_obj(BlogCategory, uid)

    def get_my_catalog(self, uid):
        return self.get_my_obj(BlogCatalog, uid)

    def get_my_article(self, uid):
        return self.get_my_obj(BlogArticle, uid)

    def get_my_tag(self, uid):
        return self.get_my_obj(BlogTag, uid)


class StatisticsHandler(APIRequestHandler):

    @authenticated
    def get(self):
        '''获取用户博客详情'''

        catalog = self.db.query(BlogCatalog.id).filter_by(
            user_id=self.current_user.id).count()
        article = self.db.query(BlogArticle.id).filter_by(
            user_id=self.current_user.id).count()
        tag = self.db.query(BlogTag.id).filter_by(
            user_id=self.current_user.id).count()
        comment = self.db.query(BlogComment.id).filter_by(
            user_id=self.current_user.id).count()

        self.success(**{
            "catalog": catalog,
            "article": article,
            "tag": tag,
            "comment": comment,
        })


class CatalogHandler(APIRequestHandler):

    @authenticated
    def get(self):
        '''目录列表'''

        q = self.db.query(BlogCatalog).filter_by(
            user_id=self.current_user.id)
        d = owner_list_objects(self, BlogCatalog, q)
        self.success(**d)

    @authenticated
    def post(self):
        '''新建目录'''

        form = CatalogNewForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        parent = None
        if not form.parent_id.is_missing:
            parent = self.get_my_catalog(form.parent_id.data)

        catalog = BlogCatalog(
            parent=parent,
            user=self.current_user,
            name=form.name.data,
            summary=form.summary.data,
            body=form.body.data,
            body_markup=form.body_markup.data
        )
        catalog.uid = BlogCatalog.gen_uid(self.db)
        self.db.add(catalog)
        self.db.commit()

        self.success(id=catalog.uid)


class _SingleCatalogBaseHandler(APIRequestHandler):

    @authenticated
    def prepare(self):
        self.catalog = self.get_my_catalog(self.path_args[0])


class SingleCatalogHandler(_SingleCatalogBaseHandler):

    def get(self, uid):
        '''查看目录'''

        self.success(**self.catalog.iowner)

    def put(self, uid):
        '''更新目录'''

        form = CatalogEditForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        catalog = self.catalog

        if not form.parent_id.is_missing:
            parent = self.get_my_catalog(form.parent_id.data)
            catalog.parent_id = parent.id
        if not form.name.is_missing:
            catalog.name = form.name.data
        if not form.summary.is_missing:
            catalog.summary = form.summary.data
        if not form.body.is_missing:
            catalog.body = form.body.data
        if not form.body_markup.is_missing:
            catalog.body_markup = form.body_markup.data

        catalog.updated = datetime.datetime.utcnow()
        self.db.commit()

        self.success()

    def delete(self, uid):
        '''删除目录'''

        # Can not delete non-empty catalog!
        if self.catalog.articles.count() > 0:
            return self.fail(_("there are articles in this catalog"))

        self.db.delete(self.catalog)
        self.db.commit()

        self.success()


class ArticleHandler(APIRequestHandler):

    @authenticated
    def get(self):
        '''文章列表'''

        q = self.db.query(BlogArticle).filter_by(
            user_id=self.current_user.id)
        d = owner_list_objects(self, BlogArticle, q)
        self.success(**d)

    @authenticated
    def post(self):
        '''新建文章'''

        form = ArticleNewForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        article = BlogArticle(
            user=self.current_user,
            title=form.title.data,
            abstract=form.abstract.data,
            body=form.body.data,
            body_markup=form.body_markup.data,
            is_public=form.is_public.data
        )
        article.uid = BlogArticle.gen_uid(self.db)

        # 类别
        if not form.category_id.is_missing:
            category = self.get_my_category(form.category_id.data)
            article.category_id = category.id

        # 目录
        if not form.catalog_id.is_missing:
            catalog = self.get_my_catalog(form.catalog_id.data)
            article.catalog_id = catalog.id

        # 标签
        if not form.tags.is_missing:
            article.tags = [self.get_my_tag(ID) for ID in form.tags.data]

        self.db.add(article)
        self.db.commit()

        self.success(id=article.uid)


class _SingleArticleBaseHandler(APIRequestHandler):

    @authenticated
    def prepare(self):
        self.article = self.get_my_article(self.path_args[0])


class SingleArticleHandler(_SingleArticleBaseHandler):

    def get(self, uid):
        '''查看文章'''

        self.success(**self.article.iowner)

    @authenticated
    def put(self, uid):
        '''更新文章'''

        form = ArticleEditForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        article = self.article

        if not form.category_id.is_missing:
            category = self.get_my_category(form.category_id.data)
            article.category_id = category.id
        if ((not form.catalog_id.is_missing) and
                # pass same catalog
                (not (article.catalog and
                              article.catalog.uid == form.catalog_id.data))
                ):
            catalog = self.get_my_catalog(form.catalog_id.data)
            article.catalog_id = catalog.id
        if not form.title.is_missing:
            article.title = form.title.data
        if not form.abstract.is_missing:
            article.abstract = form.abstract.data
        if not form.body.is_missing:
            article.body = form.body.data
        if not form.body_markup.is_missing:
            article.body_markup = form.body_markup.data
        if not form.is_public.is_missing:
            article.is_public = form.is_public.data

        # FIXME! if tags is [], form.tags.is_missing is True also!
        if not form.tags.is_missing:

            add_tags = set(form.tags.data) - \
                set([tag.uid for tag in article.tags])
            for t in [self.get_my_tag(ID) for ID in add_tags]:
                article.tags.append(t)

            del_tags = set([tag.uid for tag in article.tags]) - \
                set(form.tags.data)
            for t in [self.get_my_tag(ID) for ID in del_tags]:
                article.tags.remove(t)

        self.db.commit()
        self.success()

    @authenticated
    def delete(self, uid):
        '''删除文章'''

        self.db.delete(self.article)
        self.db.commit()
        self.success()


class TagHandler(APIRequestHandler):

    @authenticated
    def get(self):
        '''标签列表'''

        q = self.db.query(BlogTag).filter_by(
            user_id=self.current_user.id)
        d = owner_list_objects(self, BlogTag, q)
        self.success(**d)

    @authenticated
    def post(self):
        '''新建标签'''

        form = TagNewForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        tag = self.db.query(BlogTag).filter(
            and_(
                BlogTag.user_id == self.current_user.id,
                BlogTag.name == form.name.data
            )).first()
        if tag:
            return self.fail(_("tag exist"))

        tag = BlogTag(
            user=self.current_user,
            name=form.name.data,
            summary=form.summary.data,
            body=form.body.data,
            body_markup=form.body_markup.data
        )
        tag.uid = BlogTag.gen_uid(self.db)

        self.db.add(tag)
        self.db.commit()

        self.success(id=tag.uid)


class _SingleTagBaseHandler(APIRequestHandler):

    @authenticated
    def prepare(self):
        self.tag = self.get_my_tag(self.path_args[0])


class SingleTagHandler(_SingleTagBaseHandler):

    def get(self, uid):
        '''查看标签(统计信息)'''

        # TODO: 统计信息
        d = self.tag.iowner
        d.update({
            "articles": self.tag.articles.count("id")
        })
        self.success(**d)

    def put(self, uid):
        '''更新标签'''

        form = TagEditForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        tag = self.tag

        if not form.name.is_missing:
            old_tag = self.db.query(BlogTag).filter(
                and_(
                    BlogTag.user_id == self.current_user.id,
                    BlogTag.name == form.name.data,
                    BlogTag.uid != tag.uid # 不是本标签
                )).first()
            if old_tag:
                return self.fail(_("tag exist"))
            tag.name = form.name.data
        if not form.body.is_missing:
            tag.body = form.body.data
        if not form.body_markup.is_missing:
            tag.body_markup = form.body_markup.data
        if not form.summary.is_missing:
            tag.summary = form.summary.data

        self.db.commit()
        self.success()

    def delete(self, uid):
        '''删除标签'''

        # Can not delete non-empty tag!
        if self.tag.articles.count("id") > 0:
            return self.fail(_("there are articles in this tag"))

        self.db.delete(self.tag)
        self.db.commit()

        self.success()
