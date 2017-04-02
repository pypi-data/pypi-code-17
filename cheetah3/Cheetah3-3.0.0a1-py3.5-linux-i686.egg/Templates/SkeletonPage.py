#!/usr/bin/env python


"""A Skeleton HTML page template, that provides basic structure and utility methods.
"""


##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Cheetah.compat import unicode
from Cheetah.Templates._SkeletonPage import _SkeletonPage

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.0.0'
__CHEETAH_versionTuple__ = (3, 0, 0, 'development', 1)
__CHEETAH_genTime__ = 1490043964.453685
__CHEETAH_genTimestamp__ = 'Tue Mar 21 00:06:04 2017'
__CHEETAH_src__ = 'Cheetah/Templates/SkeletonPage.tmpl'
__CHEETAH_srcLastModified__ = 'Tue Mar 14 23:26:16 2017'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class SkeletonPage(_SkeletonPage):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(SkeletonPage, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)


    def writeHeadTag(self, **KWS):



        ## CHEETAH: generated from #block writeHeadTag at line 22, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter

        ########################################
        ## START - generated method body

        write(u'''<head>
<title>''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"title",True) # u'$title' on line 24, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'$title')) # from line 24, col 8.
        write(u'''</title>
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"metaTags",True) # u'$metaTags' on line 25, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$metaTags')) # from line 25, col 1.
        write(u'''
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"stylesheetTags",True) # u'$stylesheetTags' on line 26, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$stylesheetTags')) # from line 26, col 1.
        write(u'''
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"javascriptTags",True) # u'$javascriptTags' on line 27, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$javascriptTags')) # from line 27, col 1.
        write(u'''
</head>
''')

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""


    def writeBody(self, **KWS):



        ## CHEETAH: generated from #block writeBody at line 36, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter

        ########################################
        ## START - generated method body

        write(u'''This skeleton page has no flesh. Its body needs to be implemented.
''')

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""


    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter

        ########################################
        ## START - generated method body


        ## START CACHE REGION: ID=header. line 6, col 1 in the source.
        _RECACHE_header = False
        _cacheRegion_header = self.getCacheRegion(regionID=u'header', cacheInfo={'type': 2, u'id': u'header'})
        if _cacheRegion_header.isNew():
            _RECACHE_header = True
        _cacheItem_header = _cacheRegion_header.getCacheItem(u'header')
        if _cacheItem_header.hasExpired():
            _RECACHE_header = True
        if (not _RECACHE_header) and _cacheItem_header.getRefreshTime():
            try:
                _output = _cacheItem_header.renderOutput()
            except KeyError:
                _RECACHE_header = True
            else:
                write(_output)
                del _output
        if _RECACHE_header or not _cacheItem_header.getRefreshTime():
            _orig_transheader = trans
            trans = _cacheCollector_header = DummyTransaction()
            write = _cacheCollector_header.response().write
            _v = VFSL([locals()]+SL+[globals(), builtin],"docType",True) # u'$docType' on line 7, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$docType')) # from line 7, col 1.
            write(u'''
''')
            _v = VFSL([locals()]+SL+[globals(), builtin],"htmlTag",True) # u'$htmlTag' on line 8, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$htmlTag')) # from line 8, col 1.
            write(u'''
<!-- This document was autogenerated by Cheetah (http://cheetahtemplate.org/).
Do not edit it directly!

Copyright ''')
            _v = VFSL([locals()]+SL+[globals(), builtin],"currentYr",True) # u'$currentYr' on line 12, col 11
            if _v is not None: write(_filter(_v, rawExpr=u'$currentYr')) # from line 12, col 11.
            write(u''' - ''')
            _v = VFSL([locals()]+SL+[globals(), builtin],"siteCopyrightName",True) # u'$siteCopyrightName' on line 12, col 24
            if _v is not None: write(_filter(_v, rawExpr=u'$siteCopyrightName')) # from line 12, col 24.
            write(u''' - All Rights Reserved.
Feel free to copy any javascript or html you like on this site,
provided you remove all links and/or references to ''')
            _v = VFSL([locals()]+SL+[globals(), builtin],"siteDomainName",True) # u'$siteDomainName' on line 14, col 52
            if _v is not None: write(_filter(_v, rawExpr=u'$siteDomainName')) # from line 14, col 52.
            write(u'''
However, please do not copy any content or images without permission.

''')
            _v = VFSL([locals()]+SL+[globals(), builtin],"siteCredits",True) # u'$siteCredits' on line 17, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$siteCredits')) # from line 17, col 1.
            write(u'''

-->


''')
            self.writeHeadTag(trans=trans)
            write(u'''
''')
            trans = _orig_transheader
            write = trans.response().write
            _cacheData = _cacheCollector_header.response().getvalue()
            _cacheItem_header.setData(_cacheData)
            write(_cacheData)
            del _cacheData
            del _cacheCollector_header
            del _orig_transheader
        ## END CACHE REGION: header

        write(u'''
''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"bodyTag",True) # u'$bodyTag' on line 34, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$bodyTag')) # from line 34, col 1.
        write(u'''

''')
        self.writeBody(trans=trans)
        write(u'''
</body>
</html>



''')

        ########################################
        ## END - generated method body

        return _dummyTrans and trans.response().getvalue() or ""

    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_SkeletonPage= u'respond'

## END CLASS DEFINITION

if not hasattr(SkeletonPage, '_initCheetahAttributes'):
    templateAPIClass = getattr(SkeletonPage, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(SkeletonPage)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=SkeletonPage()).run()


