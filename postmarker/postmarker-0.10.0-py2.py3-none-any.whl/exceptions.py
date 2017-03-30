# coding=utf-8


class PostmarkerException(Exception):
    """
    Base class for all exceptions in Postmarker.
    """


class ClientError(PostmarkerException):
    """
    Indicates client's error.
    """

    def __init__(self, *args, **kwargs):
        self.error_code = kwargs.pop('error_code')
        super(ClientError, self).__init__(*args, **kwargs)


class SpamAssassinError(PostmarkerException):
    pass
