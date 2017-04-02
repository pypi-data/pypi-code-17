import sys
from setuptools import setup

try:
    import xcffib.xproto, xcffib, xcffib.xinerama, xcffib.randr
except:
    print ('')
    print ('xpybutil requires the Xcffib python bindings')
    #~ print ('See: http://cgit.freedesktop.org/xcb/xpyb/')
    #~ print ('Or xpyb-ng can be used. See', 'https://github.com/dequis/xpyb-ng')
    sys.exit(1)

setup(
    name = "uncrumpled_xpybutil",
    author = "Andrew Gallant",
    author_email = "andrew@pytyle.com",
    version = "0.0.1",
    license = "WTFPL",
    description = "An incomplete xcb-util port plus some extras",
    long_description = "See README",
    url = "http://pytyle.com",
    platforms = 'POSIX',
    packages = ['xpybutil'],
    data_files = [('share/doc/xpybutil', ['README', 'COPYING'])]
)
