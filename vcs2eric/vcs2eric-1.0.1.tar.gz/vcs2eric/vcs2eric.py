#!/usr/bin/python
"""Create Eric 3/4/5/6 Project files from cvs/svn/bzr/hg/git checkouts

Because this project uses the Eric4 code-base it falls under
GPL3 License.  See:

    http://opensource.org/licenses/gpl-3.0.html

this script *always* runs under /usr/bin/python rather than
using /usr/bin/env python.  It also does some munging of
sys.path to try to add Eric4's installation directory.

This is a *horrible* hack, but I find it extremely useful as
I normally use command-line vcs tools and yet want to have
Eric4 projects for the various directories.
"""
import sys, os, time, logging
log = logging.getLogger( 'vcs2eric' )
sys.e4nokde = True

if sys.version_info[0] >= 3:
    raw_input = input


SOURCE_FILES = [
    '.py','.pyx','.pxd', '.ptl', '.sql',
    '.js','.jsx','.es','.es6',
    '.css','.less','.sass','.scss',
    '.html','.kid','.jinja2','.xhtml','.xml',
    '.vrml',
    '.sdl',
    '.c','.cpp','.h','.hpp','.rst','.ini',
    '.php','.pt',
]

HUGE_FILE = 1024 * 128

def isFile( entry ):
    return entry['kind'] == 'file'
class Client( object ):
    """Mock svn client"""
    def ls( self, path ):
        """Retrieve an ls of the path from client"""
        fh = os.popen( 'svn ls -R %(path)s'%locals() )
        try:
            lines = fh.read().splitlines()
        finally:
            fh.close()
        entries = []
        for line in lines:
            if line.endswith( '/' ):
                kind = 'dir'
                name = line[:-1]
            else:
                kind = 'file'
                name = line

            entries.append({
                'name': name,
                'kind': kind,
            })
        return entries

def query( path, options ):
    """Query a given path"""
    log.info( 'Root Directory: %s', path )
    path = path.rstrip( '/' )
    vcs_type = None
    noStrip = False
    metadata = None
    if os.path.isdir( os.path.join( path, 'CVS' )):
        metadata = handleCVS( path )
        vcs_type = 'CVS'
    elif os.path.isdir( os.path.join( path, '.svn' )):
        metadata = handleSVN( path )
        vcs_type = 'Subversion'
        noStrip = True
    elif os.path.isdir( os.path.join( path, '.bzr' )):
        metadata = handleBZR( path )
        vcs_type = 'Bazaar' # not actually supported...
        vcs_type = 'Subversion'
        noStrip = True
    elif os.path.isdir( os.path.join( path, '.hg' )):
        metadata = handleHG( path )
        vcs_type = 'Mercurial'
        noStrip = True
    elif os.path.exists( os.path.join( path, '.git')):
        metadata = handleGIT( path )
        vcs_type = 'Git'
        noStrip = True

    if not metadata:
        log.warn( 'Could not find VCS information in: %s', path )
    else:

        project = MockProject(path, vcs_type=vcs_type, options=options)
        project.addFromCVS( metadata, noStrip=noStrip )
        base = os.path.basename( path )
        extension = 'e%sp'%(eric_version) if eric_version < 5 else 'e4p'
        targetFile = os.path.join( path, '%s.%s'%(base,extension))
        if os.path.exists( targetFile ):
            if not raw_input(
                'Overwrite current project? (y/n) > '
            ).lower().strip().startswith('y'):
                return
        project.writeXMLProject( targetFile )
        log.warn( 'Writing project: %s', targetFile )

def filter_huge( metadata ):
    pass

def handleSVN( path ):
    """Process (possible) SVN directory given by path"""
    names = [
        [ x.strip() ]
        for x in os.popen(
            'svn ls -R %(path)s'%locals()
        ).read().splitlines()
    ]
    return None, None, names
def handleBZR( path ):
    """Process BZR directory given by path"""
    cwd = os.getcwd()
    try:
        os.chdir( path )
        names = [
            [ x.strip() ]
            for x in os.popen(
                'bzr ls --from-root --versioned --recursive '%locals()
            ).read().splitlines()
        ]
        return None, None, names
    finally:
        os.chdir(cwd )
def handleHG( path ):
    """Process Hg directory given by path"""
    cwd = os.getcwd()
    try:
        os.chdir( path )
        def extract_name( line ):
            fragments = line.strip().split(None,1)
            if len(fragments) == 1:
                return fragments[0]
            else:
                return fragments[1]
        names = [
            [ extract_name( x ) ]
            for x in os.popen(
                'hg manifest'
            ).read().splitlines()
        ]
        return None, None, names
    finally:
        os.chdir(cwd )

def handleGIT( path, parentPath=None, client=None ):
    """Use git ls-files to get the whole set in one go..."""
    cwd = os.getcwd()
    try:
        log.warn("Inspecting %s", path)
        os.chdir( path )
        names = [
            [ x.strip() ]
            for x in os.popen( 'git ls-files' ).read().splitlines()
        ]
#        gm = '.gitmodules'
#        if os.path.exists(gm):
#            log.info("Found submodules config")
#            for line in open(gm):
#                line = line.strip()
#                if line.startswith("path"):
#                    sub_path = line.split('=', 1)[1].strip()
#                    names += handleGIT( sub_path, path, client)[2]
        return None, None, names
    finally:
        os.chdir(cwd )

def handleCVS( path ):
    """Given that CVS directory exists, parse and process"""
    cvsDir = os.path.join(path,'CVS')
    if os.path.isdir( cvsDir ):
        for file in ('Entries','Repository','Root'):
            if not os.path.isfile( os.path.join(cvsDir,file)):
                return False
    try:
        root = handleCVSRoot( cvsDir )
    except IOError as err:
        log.error( 'IOError: %s', err )
        return None
    else:
        entries = handleCVSEntries( cvsDir )
        repository = handleCVSRepository( cvsDir )
    return root, repository, entries

def handleCVSRoot( cvsDir ):
    """Read the root-file in and return as a CVSRoot URL"""
    return open( os.path.join(cvsDir,'Root')).read().strip()
def handleCVSRepository( cvsDir ):
    """Read the repository file for the CVS directory"""
    return open( os.path.join(cvsDir,'Repository')).read().strip()

def handleCVSEntries( cvsDir ):
    """Read the entries file and return all files and their timestamp information"""
    result = []
    for line in open(os.path.join(cvsDir,'Entries')):
        try:
            directory,name,version,date,flags,tail = line.split('/')
        except ValueError:
            pass
        else:
            if directory:
                result.append(
                    handleCVS(
                        os.path.join(os.path.split(cvsDir)[0],name)
                    )
                )
            else:
                try:
                    date = time.strptime( date )
                except ValueError:
                    pass
                else:
                    name = os.path.join(os.path.split(cvsDir)[0],name)
                    result.append( (name,version,date,flags) )
    return result

# Now the Eric-writing code...
# Blah, don't look, this is seriously ugly!
if os.environ.get('ERIC_SOURCE'):
    # allow for use with Eric(5) source checkouts...
    sys.path.insert(0, os.environ.get('ERIC_SOURCE'))
else:
    sys.path.insert( 0, '/usr/share/eric/modules/' )
#import ipdb;ipdb.set_trace()
try:
    import eric6 as eric
    sys.path.insert( 0, os.path.dirname(eric.__file__))
    from E5XML.ProjectWriter import ProjectWriter,  XMLStreamWriterBase as XMLWriterBase
    # normally if you're running this you're using Qt5, but this should
    # likely look at what Eric is actually using
    from PyQt5.QtCore import QFile, QIODevice
    #from PyQt5.QtCore import QFile, QIODevice
    eric_version = 6
except ImportError:
    try:
        # eric5 (assumed to be a source checkout)
        import eric5
        sys.path.insert( 0, os.path.dirname(eric5.__file__))
        from E5XML.ProjectWriter import ProjectWriter,  XMLStreamWriterBase as XMLWriterBase
        from PyQt4.QtCore import QFile, QIODevice
        eric_version = 5
    except ImportError:
        try:
            # Ubuntu Eric 4.1.x
            import eric4
            sys.path.append( os.path.dirname(eric4.__file__))
            try:
                from E4XML.ProjectWriter import ProjectWriter
                from E4XML.XMLWriterBase import XMLWriterBase
            except ImportError as err:
                from XML.ProjectWriter import ProjectWriter
                from XML.XMLWriterBase import XMLWriterBase
            eric_version = 4
        except ImportError as err:
            # Gentoo Eric 4.0.x
            import eric4
            sys.path.append( os.path.dirname(eric4.__file__))
            from eric4.XML.ProjectWriter import ProjectWriter
            from eric4.XML.XMLWriterBase import XMLWriterBase
            eric_version = 4

class MockProject( object ):
    doStrip = True
    def __init__( self, directory, vcs_type = 'Subversion', options=None ):
        self.ppath = directory
        self.subdirs = []
        self.otherssubdirs = []
        self.options = options
        self.sourceExtensions = {
            "python" : ['.py', '.ptl','.kid','.html'],
            "javascript": ['.js','.jsx','.es','.es6',],
            'css': ['.css','.less','.sass','.scss'],
            'java': ['.java'],
            'c': ['.c','.h','.cpp','.hpp'],
            "ruby"   : ['.rb'],
            "mixed"  : ['.py', '.ptl', '.rb']
        }
        pdata = {}
        for key in [
            "DESCRIPTION", "VERSION",
            "AUTHOR", "EMAIL",
            "SOURCES", "FORMS",
            "TRANSLATIONS", "MAINSCRIPT",
            "VCS", "VCSOPTIONS", "VCSOTHERDATA",
            "ERIC%sAPIPARMS"%(eric_version, ), "ERIC%sDOCPARMS"%(eric_version, ),
            "HAPPYDOCPARMS",
            "OTHERS", "INTERFACES", "TRANSLATIONPREFIX",
            "CXFREEZEPARMS","PYLINTPARMS","TRANSLATIONSBINPATH",
            "TRANSLATIONEXCEPTIONS", "RESOURCES",
            'DOCUMENTATIONPARMS', 'PACKAGERSPARMS',
            'RESOURCES','OTHERTOOLSPARMS',
            'CHECKERSPARMS',
            'PROJECTTYPESPECIFICDATA',
            'TRANSLATIONPATTERN',
            'LEXERASSOCS',
        ]:
            pdata[key] = []
        pdata['VERSION'] = [str(eric_version)]
        pdata['EOL'] = [1]
        pdata['SPELLLANGUAGE'] = ['en.CA']
        pdata['SPELLWORDS'] = [[]]
        pdata['SPELLEXCLUDES'] = [[]]
        for key in ['HASH', 'AUTHOR']:
            pdata[key] = ['']
        pdata['FILETYPES'] = dict([
            ('*%s'%(ext),'SOURCES')
            for ext in SOURCE_FILES
        ])
        pdata["AUTHOR"] = ['']
        pdata["EMAIL"] = ['']

        pdata['VCS'] = [vcs_type]
        pdata['VCSOPTIONS'] = [{
            'status': [''], 'log': [''], 'global': [''], 'update': [''],
            'remove': [''], 'add': [''], 'tag': [''], 'export': [''], 'diff': [''],
            'commit': [''], 'checkout': [''], 'history': ['']
        }]


        pdata["MIXEDLANGUAGE"] = [ False ]
        pdata["UITYPE"] = [ "Qt" ]
        pdata["PROGLANGUAGE"] = [ "Python" ]
        pdata["PROJECTTYPE"] = ['Console']

        self.pdata = self.clean_pdata(pdata)
    
    def clean_pdata(self, pdata):
        """Clean our pdata according to the Eric version"""
        if eric_version >= 6:
            exceptions = set([
            ])
            for key,value in list(pdata.items()):
                if (
                    key not in exceptions and 
                    isinstance(value,list) and 
                    len(value) == 1
                ):
                    value = value[0]
                pdata[key] = value
        return pdata

    def appendFile(self, fn, isPythonFile=0, noStrip=False):
        """
        Public method to append a file to the project.

        @param fn filename to be added to the project (string or QString)
        @param isPythonFile flag indicating that this is a Python file
                even if it doesn't have the .py extension (boolean)
        """
        log.info( ' adding: %s', fn )
        if not noStrip:
            if fn.startswith( self.ppath + '/' ):
                newfn = fn[len(self.ppath):].lstrip( '/' )
            else:
                newfn = fn
        else:
            newfn = fn
        #newfn = os.path.abspath(unicode(fn))
        #newfn = newfn.replace(self.ppath+os.sep, '')

        resolved = os.path.join( self.ppath, newfn )
        if os.path.exists(resolved) and not self.options.huge:
            if os.stat( resolved ).st_size > HUGE_FILE:
                log.warn( 'Skipping huge file %s', newfn )
                return

        newdir = os.path.dirname(newfn)
        if newfn.endswith('.ui.h'):
            ext = '.ui.h'
        else:
            (dummy, ext) = os.path.splitext(newfn)
        def shebang( resolved ):
            if os.path.isfile( resolved ):
                try:
                    return open( resolved ).read( 2 ) == '#!'
                except Exception as err:
                    print('Unable to scan', resolved, err)
                    return False
        isPythonFile = isPythonFile or ext in SOURCE_FILES or shebang( resolved )
        if ext in ['.ui', '.ui.h', '.idl'] or isPythonFile:
            if ext in ['.ui', '.ui.h']:
                if newfn not in self.pdata["FORMS"]:
                    self.pdata["FORMS"].append(newfn)
            elif isPythonFile:
                if newfn not in self.pdata["SOURCES"]:
                    self.pdata["SOURCES"].append(newfn)
            elif ext == '.idl':
                if newfn not in self.pdata["INTERFACES"]:
                    self.pdata["INTERFACES"].append(newfn)
            if newdir not in self.subdirs:
                self.subdirs.append(newdir)
        else:
            log.info( 'Do not consider %s extension a source file', ext )
            if newfn not in self.pdata["OTHERS"]:
                self.pdata['OTHERS'].append(newfn)
            if newdir not in self.otherssubdirs:
                self.otherssubdirs.append(newdir)
    def addFromCVS( self, metadata, noStrip=False ):
        """Add all files in metadata tree to self"""
        root, repository, entries = metadata
        for entry in entries:
            if not entry:
                pass
            elif len(entry) == 3:
                # directory
                self.addFromCVS( entry, noStrip=noStrip )
            else:
                self.appendFile( entry[0], noStrip=noStrip )
    def writeXMLProject(self, fn = None):
        """Public method to write the project data to an XML file.

        @param fn the filename of the project file (string)
        """
        try:
            if eric_version < 5:
                if fn.lower().endswith("e%spz"%(eric_version, )):
                    try:
                        import gzip
                    except ImportError:
                        raise
                    f = gzip.open(fn, "wb")
                else:
                    f = open(fn, "wb")
            else:
                f = QFile(fn)
                if not f.open(QIODevice.WriteOnly):
                    raise RuntimeError("Unable to open file %s"%(fn, ))
            NonGUIProjectWriter(
                f,
                os.path.splitext(os.path.basename(fn))[0],
                self.pdata,
            ).writeXML()
            f.close()
        except IOError:
            raise

        return 1

class NonGUIProjectWriter( ProjectWriter ):
    _super = ProjectWriter
    def __init__(self, file, projectName, pdata):
        """Create a new writer object
        """
        XMLWriterBase.__init__( self, file )
        self.pdata = pdata
        self.name = projectName

def main():
    usage = """vcs2eric [options] directory"""
    import optparse
    parser = optparse.OptionParser(usage=usage)
    parser.add_option(
        "-H", "--huge",
        action  = 'store_true',
        dest    = 'huge',
        default = False,
        help    = 'Include huge (> 64KB) files in project',
    )
    (options, args) = parser.parse_args()
    logging.basicConfig( level = logging.INFO )
    if args:
        for path in args:
            query( path, options )
    else:
        parser.error( "Require at least one path to process" )

if __name__ == "__main__":
    main()
