import os
import nose2
import unittest
import shutil
import yaml
from markdust.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="markdust"
)
arguments, settings, log, dbConn = su.setup()

# # load settings
# stream = file(
#     "/Users/Dave/.config/markdust/markdust.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
stream = file(
    pathToInputDir + "/example_settings.yaml", 'r')
settings = yaml.load(stream)
stream.close()

import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)
# xt-setup-unit-testing-files-and-folders


class test_esv(unittest.TestCase):

    def test_esv_function(self):

        from markdust.bible import esv
        passage = esv(
            log=log,
            passage="matt 7:7-11"
        )
        url = passage.audio()

    def test_esv_text_function(self):

        from markdust.bible import esv
        passage = esv(
            log=log,
            passage="matt 7:7-11"
        )
        text = passage.text()
        print text

        from markdust.bible import esv
        passage = esv(
            log=log,
            passage="matt 7:7-11"
        )
        text = passage.text(md=True)
        print text

    def test_esv_function_exception(self):

        from markdust.bible import esv
        try:
            this = esv(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
