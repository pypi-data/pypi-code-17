# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone.app.caching.utils import getObjectDefaultView
from plone.app.caching.utils import isPurged
from plone.cachepurging.interfaces import IPurgePathRewriter
from plone.memoize.instance import memoize
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IDiscussionResponse
from Products.CMFCore.interfaces import IDynamicType
from Products.CMFCore.utils import getToolByName
from z3c.caching.interfaces import IPurgePaths
from z3c.caching.purge import Purge
from zope.component import adapter
from zope.component import getAdapters
from zope.event import notify
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectMovedEvent


try:
    from plone.app.blob.interfaces import IBlobField
    from Products.Archetypes.interfaces import IBaseObject
    from Products.Archetypes.interfaces import IFileField
    from Products.Archetypes.interfaces import IImageField
    from Products.Archetypes.interfaces import ITextField
    HAVE_AT = True
except ImportError:
    HAVE_AT = False


@implementer(IPurgePaths)
@adapter(IDynamicType)
class ContentPurgePaths(object):
    """Paths to purge for content items

    Includes:

    * ${object_path}/ (e.g. for folders)
    * ${object_path}/view
    * ${object_path}/${object_default_view}

    If the object is the default view of its parent, also purge:

    * ${parent_path}
    * ${parent_path}/
    """

    def __init__(self, context):
        self.context = context

    def getRelativePaths(self):
        prefix = '/' + self.context.virtual_url_path()
        paths = [prefix + '/', prefix + '/view']

        defaultView = getObjectDefaultView(self.context)
        if defaultView:
            path = prefix + '/' + defaultView
            if path not in paths:  # it could be
                paths.append(path)

        parent = aq_parent(self.context)
        if parent is None:
            return paths

        parentDefaultView = getObjectDefaultView(parent)
        if parentDefaultView == self.context.getId():
            parentPrefix = '/' + parent.virtual_url_path()
            paths.append(parentPrefix)
            if parentPrefix == '/':
                # special handling for site root since parentPrefix
                # does not make sense in that case.
                # Additionally, empty site roots were not getting
                # purge paths
                # /VirtualHostBase/http/site.com:80/site1/VirtualHostRoot/_vh_site1/
                # was getting generated but not
                # /VirtualHostBase/http/site.com:80/site1/VirtualHostRoot/_vh_site1
                # which would translate to http://site.come/ getting
                # invalidated but not http://site.come
                paths.append('')
                paths.append('/view')
            else:
                paths.append(parentPrefix + '/')
                paths.append(parentPrefix + '/view')

        return paths

    def getAbsolutePaths(self):
        return []


@implementer(IPurgePaths)
@adapter(IDiscussionResponse)
class DiscussionItemPurgePaths(object):
    """Paths to purge for Discussion Item.

    Looks up paths for the ultimate parent.
    """

    def __init__(self, context):
        self.context = context

    def getRelativePaths(self):
        root = self._getRoot()
        if root is None:
            return

        request = getRequest()
        if request is None:
            return

        rewriter = IPurgePathRewriter(request, None)
        for name, pathProvider in getAdapters((root,), IPurgePaths):
            # add relative paths, which are rewritten
            relativePaths = pathProvider.getRelativePaths()
            if relativePaths:
                for relativePath in relativePaths:
                    if rewriter is None:
                        yield relativePath
                    else:
                        rewrittenPaths = rewriter(
                            relativePath) or []  # None -> []
                        for rewrittenPath in rewrittenPaths:
                            yield rewrittenPath

    def getAbsolutePaths(self):
        root = self._getRoot()
        if root is None:
            return

        request = getRequest()
        if request is None:
            return

        for name, pathProvider in getAdapters((root,), IPurgePaths):
            # add absoute paths, which are not
            absolutePaths = pathProvider.getAbsolutePaths()
            if absolutePaths:
                for absolutePath in absolutePaths:
                    yield absolutePath

    @memoize
    def _getRoot(self):

        plone_utils = getToolByName(self.context, 'plone_utils', None)
        if plone_utils is None:
            return None

        thread = plone_utils.getDiscussionThread(self.context)
        if not thread:
            return None

        return thread[0]


if HAVE_AT:

    @implementer(IPurgePaths)
    @adapter(IBaseObject)
    class ObjectFieldPurgePaths(object):
        """Paths to purge for Archetypes object fields
        """

        def __init__(self, context):
            self.context = context

        def getRelativePaths(self):
            prefix = '/' + self.context.virtual_url_path()
            schema = self.context.Schema()

            def fieldFilter(field):
                return (
                    (
                        IBlobField.providedBy(field) or
                        IFileField.providedBy(field) or
                        IImageField.providedBy(field)
                    ) and
                    not ITextField.providedBy(field)
                )
            seenDownloads = False
            for field in schema.filterFields(fieldFilter):
                if not seenDownloads:
                    yield prefix + '/download'
                    yield prefix + '/at_download'
                    seenDownloads = True

                yield prefix + '/at_download/' + field.getName()

                fieldURL = '{0}/{1}'.format(prefix, field.getName(),)
                yield fieldURL

                if IImageField.providedBy(field):
                    for size in field.getAvailableSizes(self.context).keys():
                        yield '{0}_{1}'.format(fieldURL, size,)

        def getAbsolutePaths(self):
            return []

# Event redispatch for content items - we check the list of content items
# instead of the marker interface


@adapter(IContentish, IObjectModifiedEvent)
def purgeOnModified(object, event):
    if isPurged(object):
        notify(Purge(object))


@adapter(IContentish, IObjectMovedEvent)
def purgeOnMovedOrRemoved(object, event):
    # Don't purge when added
    if event.oldName is not None and event.oldParent is not None:
        if isPurged(object):
            notify(Purge(object))
