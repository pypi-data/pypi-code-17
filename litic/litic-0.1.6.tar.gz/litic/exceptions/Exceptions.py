class LiticError(Exception):
    """Base class for all errors from a LiticService."""
    pass


class LiticConnectionError(LiticError):
    """Errors with the connection to the LITIC server."""
    pass


class LiticInputError(LiticError):
    """Errors with the input to the service call."""
    pass


class LiticOutputError(LiticError):
    """Errors with the retrieval of outputs."""
    pass


class LiticProcedureError(LiticError):
    """Base class for errors from within a procedure."""
    pass


class LiticProcedureTimeout(LiticProcedureError):
    """Error for timeout in procedure execution."""
    pass


class LiticRuntimeError(LiticError):
    """Miscellaneous errors in LITIC service usage."""
    pass
