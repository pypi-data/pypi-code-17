import sys

# Used for logging stdout to a file


class Tee(object):
    """
    Helper class for capturing output headed to a file-like object and writing it
    to a file. Use the helper function `start_logging()` to log your stdout to a
    file automatically and transparently.

    Constructor parameters
    ----------------------
    file_obj : file-like object
        The 
    filename : string
        Filename of the logfile all output will be recorded to
    mode : string
        The `open()` modestring the logfile will be opened with. Ex: 'wt'
    """

    def __init__(self, file_obj, filename, mode):
        self.file = open(filename, mode)
        self.file_obj = file_obj

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def write(self, data):
        self.file.write(data)
        self.file_obj.write(data)

    def flush(self):
        self.file.flush()
        self.file_obj.flush()

    def __del__(self):
        self.close()


def start_logging(logfile):
    """
    Begin logging all output to a logfile, while still printing it out to the console

    Parameters
    ----------
    logfile : string
        Filename of the logfile all output will be recorded to
    """
    sys.stdout = Tee(sys.stdout, logfile, 'wt')


def stop_logging(tee=sys.stdout):
    """
    Stop logging all output by the given Tee object

    Parameters
    ----------
    tee : Tee object
        Optional Tee object, defaults to guessing that sys.stdout is a Tee object
    """
    if type(tee) is Tee:
        tee.close()
