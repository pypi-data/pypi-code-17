"""Interface to logging to allow color logs to
terminal, or non-color to files"""
# termcolor
# if we have the termcolor package, then colorize some text.
import six
try:
    from termcolor import cprint, colored
    def colorize(color, on_color=None):
        return lambda text: colored(text,color=color, on_color=on_color)

    text_message = colorize('blue')
    text_info    = colorize("green")
    text_warning = colorize('magenta')
    text_error = colorize('red')
    text_critical = colorize('red')
    text_note = colorize('grey')
except:

    def nocolor(text, *args, **kwargs):
        return "nocolor: "+text

    def colored(text, color=None, on_color=None, attrs=None):
        return text
    pass
    text_message = nocolor
    text_warning = nocolor
    text_error = nocolor
    text_critical = nocolor
    text_info = nocolor
    text_note = nocolor

from logging import *
import sys

def handler(level=None, form=None, filename=None, stream=None, datefmt=None, use_color=True):
    """Setup for a handler:
        Level sets the minimum level noted in this log
        form sets the format of the log message
        filename is the filename for a file logger
        stream is the stream object for a stream logger (also colorizes)
        use_color overrides the stream color usage if False.
    """
    
    if datefmt is None:
        datefmt = "%Y/%m/%d %H:%M:%S "
    #configure the lowest level to print
    if level is None:
        level = DEBUG
    #configure the format of the output
    if form is None:
        form = "%(levelname)-8s %(asctime)s %(message)s"
    #set the output
    
    handler = None
    
    if stream is not None:
        handler = StreamHandler()
        class MyFormatter(Formatter):
            def __init__(self, fmt, datefmt=None):
                Formatter.__init__(self, fmt, datefmt)
            def colorize(self,str, levelname):
                """Attempts to colorize the string based on the
                warning level of the log message."""
                colors = {  "DEBUG": text_message,
                             "INFO": text_info,
                             "WARNING": text_warning,
                             "ERROR": text_error,
                             "CRITICAL": text_critical}
                if levelname in colors:
                    return colors[levelname](str)
                else:
                    return str#terminal.note(str)

            def format(self,record):
                str = Formatter.format(self, record)
                return self.colorize(str, record.levelname)
        if use_color:
            lform = MyFormatter(form, datefmt=datefmt)
        else:
            lform = Formatter(form,datefmt=datefmt)
        handler.setFormatter(lform)
        handler.setLevel(level)
    
    if filename is not None:
        handler = FileHandler(filename)
        lform = Formatter(form, datefmt=datefmt)
        handler.setFormatter(lform)
        handler.setLevel(level)

    return handler


def ProgramLogger(name, destinations):
    """Function to define multiple loggers in one step, and name them.
    destinations is a dictionary of dictionaries, where each dictionary
    contains level, form, filename OR stream, and use_color as required
    by handler above.
    This function iterates through the dictionary defining the handlers
    and adding them to the logger before returning."""

    log = getLogger(name)
    if len(log.handlers):
        return log
    log.setLevel(DEBUG)
    for key, dest in six.iteritems(destinations):
        handle = handler(level=dest.get("level", DEBUG),
                         form=dest.get("form", None),
                         filename=dest.get("filename", None),
                         stream=dest.get("stream", None),
                         use_color=dest.get("use_color", True))
        log.addHandler(handle)

    return log

def log_level(lookfor):
    """Tries to find a suitable log level based on input string. 
    Input can be a level (0=critical, 4=debug), or a substring of
    debug,info, warning, error, or critical.
    """
    levels={0:CRITICAL,
            1:ERROR,
            2:WARNING,
            3:INFO,
            4:DEBUG,
            "critical":CRITICAL,
            "error":ERROR,
            "warning":WARNING,
            "info":INFO,
            "debug":DEBUG
                }
    if lookfor.lower() in levels:
        return levels[lookfor.lower()],lookfor.lower()
    else:
        for k,v in six.iteritems(levels):
            l=len(str(k)) if len(str(k)) < len(lookfor) else len(lookfor)
            if str(k)[0:l].lower() == lookfor.lower():
                return v,k
    
    raise IndexError
    
def default_logger(name, logfile=None,
                    file_verbosity = "WARNING",
                    verbosity="CRITICAL"):
    """Sets up a simple logger in a file and the stderr, with standard error levels.
    This is intended for use with input options corresponding to the input options"""
    
    log_error=""
    try:
        level,log_level_name = log_level(verbosity)
    except IndexError:
        log_error =  log_error + "verbosity level invalid({0}, should be 0-4)".format(verbosity)
        level = CRITICAL
        log_level_name="critical"
    try:
        file_level, file_level_name = log_level(file_verbosity)
    except:
        log_error =  log_error + "file_verbosity level invalid({0}, should be 0-4)".format(file_verbosity)
        file_level = ERROR
        file_level_name="error"
    #stdout
    dest = {}
    stderr_h = dict(level=level, stream=sys.stderr, use_color=True)
    dest["stderr"]=stderr_h
    if logfile is not None:
        file_err = dict(level=file_level, filename=logfile, use_color=True)
        dest["logfile"]=file_err

    log = ProgramLogger(name, dest)
    log.setLevel(level if level < file_level else file_level)

    if log_error!="":
        log.error(log_error)
    log.info("log screenlevel is set to {0}".format(log_level_name))
    log.info("log filelevel is set to {0}".format(file_level_name))
    
    return log

def command_line(parser, progname, default_verbosity="CRITICAL", default_file_verbosity="CRITICAL"):
    """Adds command line options to the supplied parser instance"""
    parser.add_argument("--logfile",type=str, default="{0}.log".format(progname))
    parser.add_argument("--verbosity","-v",type=str, default=default_verbosity)
    parser.add_argument("--file_verbosity","-fv",type=str, default=default_file_verbosity)
    