class HitchDocException(Exception):
    pass


class VarMustBePickleable(HitchDocException):
    """
    Variable passed to step was not pickleable.
    """
    pass
