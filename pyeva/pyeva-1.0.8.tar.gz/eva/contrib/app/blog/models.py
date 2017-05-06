# coding: UTF-8

import datetime

from sqlalchemy import Column, Integer, String, \
    Sequence, DateTime, Table, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, backref

from eva.utils.translation import ugettext_lazy as _
from eva.orm import ORMBase
from eva.db.models import UIDMixin
from eva.utils.time_ import rfc3339_string


blog_article__tag = Table(
    'blog_article__tag', ORMBase.metadata,
    Column('article_id', Integer, ForeignKey('blog_article.id')),
    Column('tag_id', Integer, ForeignKey('blog_tag.id'))
)


class BlogCategory(UIDMixin, ORMBase):
    ''' Blog 全局类别
    '''

    __tablename__ = 'blog_category'

    id = Column(Integer, Sequence('blog_category_id_seq'), primary_key=True)

    # 父类别
    parent_id = Column(Integer, ForeignKey('blog_category.id'))
    parent = relationship("BlogCategory", backref="children", remote_side=[id])

    name = Column(String(64), nullable=False)  # 名称可以相同，因为有级别
    summary = Column(String(1024))
    body = Column(Text)
    body_markup = Column(Integer, default=1)

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, parent=None, summary='', body='', body_markup=1):
        self.name = name
        self.summary = summary
        self.body = body
        self.body_markup = body_markup
        if parent:
            self.parent_id = parent.id

    @property
    def isimple(self):
        return {
            "id": self.uid,
            "name": self.name,
            "summary": self.summary
        }

    @property
    def ibase(self):
        return {
            "parent": self.parent.isimple if self.parent_id else None,
            "id": self.uid,
            "name": self.name,
            "summary": self.summary,
            "body": self.body,
            "body_markup": self.body_markup,
            'created': rfc3339_string(self.created),
            'updated': rfc3339_string(self.updated),
        }

    @property
    def iuser(self):
        return self.iuser

    @property
    def iadmin(self):
        return self.ibase


class BlogCatalog(UIDMixin, ORMBase):

    ''' Blog 目录

    用户可以创建自己的目录结构
    '''

    __tablename__ = 'blog_catalog'

    id = Column(Integer, Sequence(
        'blog_catalog_id_seq'), primary_key=True)

    # 父目录
    parent_id = Column(Integer, ForeignKey('blog_catalog.id'))
    parent = relationship("BlogCatalog", backref="children", remote_side=[id])

    user_id = Column(Integer, ForeignKey('auth_user.id'))  # 创建用户 ID
    user = relationship("User", backref="blog_catalogs")

    name = Column(String(64), nullable=False)  # 不同用户可以创建相同的Tag
    summary = Column(String(1024))
    body = Column(Text)
    body_markup = Column(Integer, default=1)

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, name, parent=None, summary='',
                 body='', body_markup=1):
        self.user_id = user.id
        self.name = name
        if parent:
            self.parent_id = parent.id
        self.summary = summary
        self.body = body
        self.body_markup = body_markup

    @property
    def isimple(self):
        return {
            "id": self.uid,
            "name": self.name,
        }

    @property
    def ibase(self):
        return {
            "parent": self.parent.isimple if self.parent_id else None,
            "id": self.uid,
            "name": self.name,
            "summary": self.summary,
            "body": self.body,
            "body_markup": self.body_markup,
            'created': rfc3339_string(self.created),
            'updated': rfc3339_string(self.updated),
        }

    @property
    def iuser(self):
        d = self.ibase
        d.update({
            "user": self.user.isimple
        })
        return d

    @property
    def iowner(self):
        return self.ibase

    @property
    def iadmin(self):
        return self.iadmin


class BlogArticle(UIDMixin, ORMBase):

    ''' Blog 文章

    '''

    __tablename__ = 'blog_article'

    id = Column(Integer, Sequence('blog_article_id_seq'), primary_key=True)

    category_id = Column(Integer, ForeignKey('blog_category.id'))
    category = relationship("BlogCategory", backref="articles")

    catalog_id = Column(Integer, ForeignKey('blog_catalog.id'))
    catalog = relationship(
        "BlogCatalog", backref=backref("articles", lazy='dynamic'))

    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship("User", backref="blog_articles")

    title = Column(String(128), nullable=False)
    abstract = Column(String(1024))  # 摘要
    body = Column(Text)
    body_markup = Column(Integer, default=1)

    status = Column(Integer, default=0)

    # 是否公开
    is_public = Column(Boolean, default=False)
    # 是否锁定
    is_locked = Column(Boolean, default=False)

    vote_up = Column(Integer, default=0)
    vote_down = Column(Integer, default=0)

    view_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)

    tags = relationship(
        'BlogTag', secondary=blog_article__tag, backref='articles')

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, title, body, body_markup=1, abstract=None,
                 is_public=True, category=None, catalog=None):
        self.user_id = user.id
        self.title = title
        self.body = body
        self.body_markup = body_markup
        # TODO: gen abstract
        self.abstract = abstract
        self.is_public = is_public

        if category:
            self.category_id = category.id

        if catalog:
            self.catalog_id = catalog.id

    def increase_comment_count(self):
        if self.comment_count:
            self.comment_count += 1
        else:
            self.comment_count = 1

    def to_vote(self, vote):
        if vote > 0:
            self.vote_up += vote
        else:
            self.vote_down += vote

    @property
    def iuser(self):
        return {
            "title": self.title,
            "id": self.uid,
            "body": self.body,
            "body_markup": self.body_markup,
            "abstract": self.abstract,
            'created': rfc3339_string(self.created),
            'updated': rfc3339_string(self.updated),
            'tags': [t.iuser for t in self.tags],
            'catalog': self.catalog.isimple if self.catalog_id else None,
            'category': self.category.isimple if self.category_id else None,
            'author': self.user.isimple,
        }

    @property
    def iowner(self):
        return self.iuser  # TODO


class BlogComment(UIDMixin, ORMBase):

    ''' Blog 注释, 对 BlogPost 的回复

    1. 某回复的注释
    2. 适当降低 comment 的“价值鼓励”，引导用户少做 comment

    '''

    __tablename__ = 'blog_comment'

    id = Column(Integer, Sequence('blog_comment_id_seq'), primary_key=True)

    article_id = Column(Integer, ForeignKey('blog_article.id'))
    article = relationship("BlogArticle", backref="comments")

    parent_id = Column(Integer, ForeignKey('blog_comment.id'))
    parent = relationship("BlogComment", backref="children", remote_side=[id])

    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship("User", backref="blog_comments")

    body = Column(Text)
    body_markup = Column(Integer, default=1)

    vote_up = Column(Integer, default=0)
    vote_down = Column(Integer, default=0)

    status = Column(Integer, default=0)

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, article, user, body, body_markup=1, parent=None):

        self.article_id = article.id
        article.increase_comment_count()

        self.user_id = user.id
        self.body = body
        self.body_markup = body_markup

        if parent:
            self.parent_id = parent.id

    def to_vote(self, vote):
        if vote > 0:
            self.vote_up += vote
        else:
            self.vote_down += vote


class BlogVote(UIDMixin, ORMBase):

    '''Blog 投票系统

    1. 针对文章、评论的投票
    2. 每个用户只能投票一次
    3. 自己不能投自己

    '''

    TARGETS = (
        (1, 'article', _('Article')),
        (2, 'comment', _('Comment')),
    )

    __tablename__ = 'blog_vote'

    id = Column(Integer, Sequence(
        'blog_vote_id_seq'), primary_key=True)

    target_id = Column(Integer, nullable=False)
    target_type = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship("User", backref="blog_article_votes")

    # 投票值 [-1, 1]
    vote = Column(Integer, nullable=False)

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, vote, target):

        self.user_id = user.id
        self.vote = vote

        self.target_id = target.id
        if isinstance(target, BlogArticle):
            self.target_type = 1
        elif isinstance(target, BlogComment):
            self.target_type = 2

        target.to_vote(vote)


class BlogTag(UIDMixin, ORMBase):

    ''' Blog 标签

    不同用户可以使用自己的 Tag
    '''

    __tablename__ = 'blog_tag'

    id = Column(Integer, Sequence(
        'blog_tag_id_seq'), primary_key=True)

    user_id = Column(Integer, ForeignKey('auth_user.id'))  # 创建用户 ID
    user = relationship("User", backref="blog_tags")

    name = Column(String(64), nullable=False)  # 不同用户可以创建相同的Tag
    summary = Column(String(1024))
    body = Column(Text)
    body_markup = Column(Integer, default=1)

    # 索引值
    count = Column(Integer, default=0)

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, name, summary='', body='', body_markup=1):
        self.user_id = user.id
        self.name = name
        self.summary = summary
        self.body = body
        self.body_markup = body_markup

    @property
    def iuser(self):
        return {
            "name": self.name,
            "id": self.uid,
            "body": self.body,
            "body_markup": self.body_markup,
            "summary": self.summary,
            "count": self.count,
            "created": rfc3339_string(self.created),
            "updated": rfc3339_string(self.updated),
        }

    @property
    def iowner(self):
        return self.iuser  # TODO


class BlogGlobalTag(UIDMixin, ORMBase):

    ''' Blog 全局Tag

    根据用户BlogTag创建情况，保存唯一值

    TODO:

    1. 本表可以从BlogTag中查出
    '''

    __tablename__ = 'blog_global_tag'

    id = Column(Integer, Sequence(
        'blog_global_tag_id_seq'), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    count = Column(Integer, default=0)

    def __init__(self, name):
        self.name = name
