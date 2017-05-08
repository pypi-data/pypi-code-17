class BioboxesException(Exception):
    """
    Base class for bioboxes exceptions.
    """

class UnsupportedDockerVersionException(BioboxesException):
    """
    An unsupported version of Docker is being used.
    """

class BioboxInputVolumeNotFound(BioboxesException):
    """
    A host directory has been given as an input volume, but it does not exist.
    """
