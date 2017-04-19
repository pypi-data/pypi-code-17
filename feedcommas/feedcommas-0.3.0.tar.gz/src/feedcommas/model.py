# Copyright (C) 2017 Michał Góral.
#
# This file is part of Feed Commas
#
# Feed Commas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Feed Commas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Feed Commas. If not, see <http://www.gnu.org/licenses/>.

'''Schemas and manipulators for sqlite cache'''

import os
import collections
import shlex
import contextlib
from subprocess import Popen, PIPE
import datetime as dt
import urllib.parse

from sqlalchemy import (create_engine, Column, String, Integer, DateTime,
                        Text, Boolean, ForeignKey)
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql.schema import Index
from sqlalchemy.ext.declarative import declarative_base

from bs4 import BeautifulSoup
import mgcomm.env

import feedcommas.config as config
import feedcommas._version as version
from feedcommas.utils import mkdir_p

_Base = declarative_base()
Session = None


class VersionMismatch(Exception):
    '''Exception raised when Database was created for an incompatible
    version.'''
    pass


def init():
    '''Initializes and connects to database'''
    addr = config.get_value('server.address')
    user = config.get_value('server.username')
    uname = urllib.parse.quote('%s_%s' % (addr, user), safe='')

    cache_dir = os.path.join(mgcomm.env.home(), '.cache', 'feed-commas')
    mkdir_p(cache_dir)

    engine = create_engine('sqlite:///%s' % os.path.join(cache_dir, uname))

    global Session

    Session = sessionmaker(expire_on_commit=False)
    Session.configure(bind=engine)
    _Base.metadata.create_all(engine)

    with make_session() as session:
        md = session.query(MetaData).one_or_none()
        if md:
            md.version = version.version
        else:
            md = MetaData(version=version.version)
        session.add(md)


@contextlib.contextmanager
def make_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class MetaData(_Base):
    '''Feed Commas related metadata'''
    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True)
    version = Column(String)


class Feed(_Base):
    '''Feed schema'''
    __tablename__ = 'feed'

    id = Column(String, primary_key=True)
    name = Column(String)
    is_category = Column(Boolean, default=False)
    unread = Column(Integer, nullable=True)

    parent_id = Column(ForeignKey('feed.id'), nullable=True)
    children = relationship('Feed',
                            cascade='all, delete-orphan',  # cascade deletions
                            backref=backref('parent', remote_side=id))

    def __init__(self, id_, name, unread=None, is_category=False, parent=None):
        self.id = str(id_)
        self.name = name
        self.is_category = is_category
        self.parent = parent
        self.unread = unread
        self.children = []

    @property
    def depth(self):
        '''Returns a depth of this node.'''
        depth = 0
        node = self.parent
        while node:
            node = node.parent
            depth += 1
        return depth

    def bfs(self):
        '''Traverse a tree starting from this node: breadth-first search
        variant.'''
        queue = collections.deque([self])
        while len(queue) > 0:
            parent = queue.popleft()
            yield parent
            queue.extend(parent.children)

    def dfs(self):
        '''Traverse a tree starting from this node: depth-first search
        variant.'''

        stack = collections.deque([self])
        while len(stack) > 0:
            node = stack.pop()
            yield node
            stack.extend(reversed(node.children))

    def __repr__(self):
        return 'Feed(id=%s, name=%s)' % (self.id, self.name)


class Article(_Base):
    '''Article schema'''
    __tablename__ = 'article'

    id = Column(String, primary_key=True)
    feed_id = Column(String)
    feed_name = Column(String)
    publish_date = Column(DateTime)
    title = Column(String)
    orig_content = Column(Text)
    author = Column(String)
    url = Column(String)
    read = Column(Boolean)
    markable = Column(Boolean)
    starred = Column(Boolean)

    __table_args__ = (Index('article_search_index',
                            'feed_id', 'publish_date', 'read'),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_json(entry):
        '''Initializez Article from json fetched from Comma Feed'''
        art = Article()
        art.id = entry['id']
        art.feed_name = entry['feedName']
        art.feed_id = entry['feedId']
        art.title = entry['title']
        art.orig_content = entry['content']
        art.author = entry.get('author')
        art.url = entry['url']

        # epoch returned by Commafeed is in milliseconds
        timestamp = entry['date'] / 1000
        art.publish_date = dt.datetime.fromtimestamp(timestamp)

        art.read = entry['read']
        art.markable = entry['markable']
        art.starred = entry['starred']
        return art

    @property
    def date(self):
        '''Formatted publis date'''
        return self.publish_date.strftime('%c')

    @property
    def content(self):
        '''Filtered article's content'''
        return _filter_html(self.orig_content)

    def __repr__(self):
        return 'Article(id=%s, title=%s)' % (str(self.id), self.title)


def _builtin_filter(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    return soup.get_text()


def _filter_html(doc):
    method = config.get_value('settings.html-filter')
    if not method or method.lower() == 'none':
        return doc
    elif method.lower() == 'builtin':
        return _builtin_filter(doc)

    cmd = shlex.split(method)
    process = Popen(cmd, stdin=PIPE, stdout=PIPE)
    out, __ = process.communicate(input=doc.encode('utf-8'))
    return out.decode('utf-8')
