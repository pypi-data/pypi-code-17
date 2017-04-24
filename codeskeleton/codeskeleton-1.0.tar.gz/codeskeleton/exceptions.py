class CodeSkeletonError(Exception):
    pass


class ConfigFileError(CodeSkeletonError):
    pass


class SpecError(CodeSkeletonError):
    pass


class VariableSpecError(SpecError):
    def __init__(self, name, message):
        self.name = name
        self.message = message

    def __str__(self):
        return 'Variable {!r}: {}'.format(self.name, self.message)


class FileSpecError(SpecError):
    def __init__(self, path, message):
        self.path = path
        self.message = message

    def __str__(self):
        return 'File {!r}: {}'.format(self.path, self.message)


class SpecValidationError(SpecError):
    def __init__(self, path, message):
        self.path = path
        self.message = message

    def __str__(self):
        return '{}: {}'.format(self.path, self.message)


class ValueValidationError(SpecError):
    pass


class InvalidVariableName(SpecError):
    pass
