#!/usr/local/bin/python
# encoding: utf-8
"""
*tools for working with the esv api*

Documentation for markdust can be found here: http://markdust.readthedocs.org/en/stable

Usage:
    esv [-i] audio <book> <passage>
    esv [-i] md <book> <passage>

Options:
    audio                 generate the audio MP£ URL for ESV passage
    md                    output plain-text with MD link back to online version of ESV bible

    -h, --help            show this help message
    -v, --version         show version
    -s, --settings        the settings file
    -i, --iframe          output in an iframe wrapper for audio narration of passage

    <book>                the book of the bible
    <passage>             chapter and verses (e.g. 7:7-11)
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
import re
import requests
from docopt import docopt
from fundamentals import tools, times
from subprocess import Popen, PIPE, STDOUT
# from ..__init__ import *


def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when ``cl_utils.py`` is run as a single script from the cl, or when installed as a cl command*
    """
    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="WARNING",
        options_first=False,
        projectName="markdust"
    )
    arguments, settings, log, dbConn = su.setup()

    # tab completion for raw_input
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tab_complete)

    # unpack remaining cl arguments using `exec` to setup the variable names
    # automatically
    for arg, val in arguments.iteritems():
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        if varname == "import":
            varname = "iimport"
        if isinstance(val, str) or isinstance(val, unicode):
            exec(varname + " = '%s'" % (val,))
        else:
            exec(varname + " = %s" % (val,))
        if arg == "--dbConn":
            dbConn = val
        log.debug('%s = %s' % (varname, val,))

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cl_utils.py AT %s' %
        (startTime,))

    # set options interactively if user requests
    if "interactiveFlag" in locals() and interactiveFlag:

        # load previous settings
        moduleDirectory = os.path.dirname(__file__) + "/resources"
        pathToPickleFile = "%(moduleDirectory)s/previousSettings.p" % locals()
        try:
            with open(pathToPickleFile):
                pass
            previousSettingsExist = True
        except:
            previousSettingsExist = False
        previousSettings = {}
        if previousSettingsExist:
            previousSettings = pickle.load(open(pathToPickleFile, "rb"))

        # x-raw-input
        # x-boolean-raw-input
        # x-raw-input-with-default-value-from-previous-settings

        # save the most recently used requests
        pickleMeObjects = []
        pickleMe = {}
        theseLocals = locals()
        for k in pickleMeObjects:
            pickleMe[k] = theseLocals[k]
        pickle.dump(pickleMe, open(pathToPickleFile, "wb"))

    # CALL FUNCTIONS/OBJECTS
    if audio:
        from markdust.bible import esv
        esvPassage = esv(
            log=log,
            passage=book + " " + passage
        )
        url = esvPassage.audio(iframe=iframeFlag)
        print url

    if md:
        from markdust.bible import esv
        mdPassage = esv(
            log=log,
            passage=book + " " + passage
        )
        mdPassage = mdPassage.text(md=True)

        if iframeFlag:
            esvPassage = esv(
                log=log,
                passage=book + " " + passage
            )
            mdPassage += "\n\n> " + esvPassage.audio(iframe=iframeFlag)
        print mdPassage

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return


class esv():
    """
    *tools for working with the esv api*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``passage`` -- the passage you're interested in (e.g. matt 7:7-11)

    **Usage:**

        To setup your logger please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

        To initiate a esv passage object, use the following:

        .. code-block:: python 

            from markdust.bible import esv
            passage = esv(
                log=log,
                passage="matt 7:7-11"
            )   
    """
    # Initialisation

    def __init__(
            self,
            log,
            passage,
            settings=False
    ):
        self.log = log
        log.debug("instansiating a new 'esv' object")
        self.settings = settings
        self.passage = passage
        # xt-self-arg-tmpx

        return None

    def audio(self,
              iframe=False):
        """
        *grab the URL to the audio MP3 of the bible passage*

        **Key Arguments:**
            - ``iframe`` -- add an iframe wrapper. Default *False*

        **Return:**
            - ``url`` -- the URL to the bible audio

        **Usage:**

        .. code-block:: python 

            from markdust.bible import esv
            passage = esv(
                log=log,
                passage="matt 7:7-11"
            )
            url = passage.audio() 
            print url
            # http://audio.esvbible.org/hw/40007007-40007011.mp3
        """
        self.log.info('starting the ``audio`` method')

        passage = self.passage.replace(" ", "")

        try:
            response = requests.get(
                url="http://www.esvapi.org/v2/rest/passageQuery",
                params={
                    "key": "IP",
                    "passage": passage,
                    "output-format": "mp3",
                },
            )
        except requests.exceptions.RequestException:
            print 'HTTP Request failed'

        output = response.url
        if iframe:
            output = output.replace("/hw/", "/embed/ml/hq/")
            output = """<iframe width="300" height="26" frameBorder="0" allowTransparency="true" src="%(output)s?scrubberWidth=100&bgcolor=615d61"></iframe>""" % locals(
            )

        self.log.info('completed the ``audio`` method')
        return output

    def text(
            self,
            md=False):
        """*text*

        **Key Arguments:**
            - ``md`` -- return in markdown format. Default *False*

        **Return:**
            - ``passage`` -- the passage text

        **Usage:**

            To output a plain-text passage:

            .. code-block:: python 

                from markdust.bible import esv
                passage = esv(
                    log=log,
                    passage="matt 7:7-11"
                )
                text = passage.text()
                print text

            .. code-block:: text

                "Ask, and it will be given to you; seek, and you will find; knock, and it will be opened to you. For everyone who asks receives, and the one who seeks finds, and to the one who knocks it will be opened. Or which one of you, if his son asks him for bread, will give him a stone? Or if he asks for a fish, will give him a serpent? If you then, who are evil, know how to give good gifts to your children, how much more will your Father who is in heaven give good things to those who ask him! Matthew 7:7-11

            Or to output fancy-pants markdown with links back to the ESV passage online:

            .. code-block:: python 

                from markdust.bible import esv
                passage = esv(
                    log=log,
                    passage="matt 7:7-11"
                )
                mdPassage = passage.text(md=True)
                print mdPassage

            This outputs the following:

            .. code-block:: text

                "Ask, and it will be given to you; seek, and you will find; knock, and it will be opened to you. For everyone who asks receives, and the one who seeks finds, and to the one who knocks it will be opened. Or which one of you, if his son asks him for bread, will give him a stone? Or if he asks for a fish, will give him a serpent? If you then, who are evil, know how to give good gifts to your children, how much more will your Father who is in heaven give good things to those who ask him! [**Matthew 7:7-11** (ESV)](http://www.esvbible.org/matt7:7-11)
        """
        self.log.info('starting the ``text`` method')

        passage = self.passage.replace(" ", "")

        clean = re.sub('\s', '%20', passage)
        link = 'http://www.esvbible.org/' + clean

        try:
            response = requests.get(
                url="http://www.esvapi.org/v2/rest/passageQuery",
                params={
                    "key": "IP",
                    "passage": passage,
                    'include-short-copyright': 0,
                    'output-format': 'plain-text',
                    'include-passage-horizontal-lines': 0,
                    'include-heading-horizontal-lines': 0,
                    'include-headings': 0,
                    'include-subheadings': 0,
                    'include-selahs': 0,
                    'line-length': 0,
                    'include-passage-references': 1,
                    'include-footnotes': 0,
                    'include-verse-numbers': 0
                },
            )
        except requests.exceptions.RequestException:
            print 'HTTP Request failed'

        output = response.content

        bibletext = re.sub('\[\d+\:\d+\]\s?', '', output)
        bibletext = bibletext.split('\n')

        cleanBibletext = []
        cleanBibletext[:] = [c.strip() for c in bibletext]
        bibletext = cleanBibletext
        if len(bibletext[-1].split('"')) == 2:
            bibletext[-1] += '"'

        passageRef = bibletext[0]
        passageText = ('\n').join(bibletext[1:])
        passagelink = " **[%(passageRef)s](%(link)s)** [(ESV)](%(link)s)" % locals()
        bibletext = "> " + \
            ('\n\n> ').join(bibletext[1:]) + '\n\n> ' + passagelink

        if md:
            return bibletext.strip()

        self.log.info('completed the ``text`` method')
        return passageText + " " + passageRef.strip()

    # use the tab-trigger below for new method
    # xt-class-method


if __name__ == '__main__':
    main()
