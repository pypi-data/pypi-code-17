#!/usr/bin/env python3

""" CherryPy dispatcher that looks for page handlers in database """

import importlib

import cherrypy
from cherrypy.lib.static import serve_file

from ..core import cfg, resolvePath
from ..db import db
from ..gettext import setLocale
from ..models import PageNode, SiteNode
from .URLHandler import URLHandler


class NodesDispatcher(cherrypy.dispatch.Dispatcher):

    """ CherryPy dispatcher that looks for page handlers in database """

    def __call__(self, path_info=None):
        """Set handler and config for the current request."""

        def _serve_static(path):
            """ serve static """
            def _serve(*args, **kwargs):  # pylint: disable=unused-argument
                """ serve static """
                return serve_file(str(path))
            return _serve

        def _partial_paths(parts):
            """ iterate over list of parent paths """
            result = ''
            parts = ['']+parts
            for part in parts:
                result += part+'/'
                yield result

        cherrypy.response.headers['X-Clacks-Overhead'] = 'GNU Terry Pratchett'

        path_info = path_info.strip('/')
        request = cherrypy.serving.request
        request.config = cherrypy.config.copy()

        urls = list(_partial_paths(path_info.split('/')))

        q = db.query(PageNode).filter(PageNode.url.in_(urls))
        q = q.order_by(PageNode.url.desc())
        pagenode = q.first()

        if pagenode:
            vpath = path_info.split('/')[len(pagenode.url.strip('/').split('/')):]
            if pagenode.lang:
                cherrypy.response.i18n = setLocale(pagenode.lang)

            cname = pagenode.type.capitalize()+'Handler'
            mod = importlib.import_module('.'+cname, 'clacks.handlers')
            hclass = getattr(mod, cname)(pagenode)

            func = getattr(hclass, 'default', None)
            if hasattr(hclass, "_cp_config"):
                request.config.update(hclass._cp_config)
            if hasattr(func, "_cp_config"):
                request.config.update(func._cp_config)

            vpath = [x.replace("%2F", "/") for x in vpath]
            request.node = pagenode
            request.handler = cherrypy.dispatch.LateParamPageHandler(func, *vpath)
        elif path_info == '':
            func = SiteNodeHandler().default
            if hasattr(func, "_cp_config"):
                request.config.update(func._cp_config)  # pylint: disable=no-member
            request.handler = cherrypy.dispatch.LateParamPageHandler(func, [])
        else:
            filepath = resolvePath('http', path_info)
            request.user = None
            if filepath.is_file():
                request.handler = _serve_static(filepath)  # pylint: disable=redefined-variable-type
            else:
                request.handler = cherrypy.NotFound()


cherrypy.dispatch.NodesDispatcher = NodesDispatcher


class SiteNodeHandler(URLHandler):

    """Node fetching and HeadNode fallback handler.

    This handler currently serves two purposes:
     * mounts NodesDispatcher as the main dispatcher.
     * redirects content to lang page if no handler is found for '/' in the database
    """

    mount_url = ''
    dispatcher = 'NodesDispatcher'

    @cherrypy.expose
    @cherrypy.tools.require()
    def default(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ redirect to language page for if HeadNode is not of PageNode type (not implemented yet)"""
        user_langs = [str(x)[:2] for x in cherrypy.request.headers.elements('Accept-Language')]
        user_langs.append(cfg.get('locale', 'default-language'))  # fallback
        lang_pages = db.query(SiteNode).filter_by(placement='lang', visible=True).all()
        site_langs = [p.lang for p in lang_pages]
        best_lang = next(l for l in user_langs if l in site_langs)
        best_page = next(p for p in lang_pages if p.lang == best_lang)
        raise cherrypy.HTTPRedirect(best_page.url)
