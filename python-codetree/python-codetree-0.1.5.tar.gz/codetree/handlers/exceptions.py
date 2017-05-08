class BranchDiverged(Exception):
    pass


class CommandFailure(Exception):
    def __init__(self, message, original_exception):
        self.message = message
        self.original_exception = original_exception


class DuplicateHandlerError(Exception):
    pass


class InvalidOption(Exception):
    pass


class NotABranch(Exception):
    pass


class NotSameBranch(Exception):
    pass


class NoSuchHandlerError(Exception):
    pass


class NoSuchCharm(Exception):
    pass
