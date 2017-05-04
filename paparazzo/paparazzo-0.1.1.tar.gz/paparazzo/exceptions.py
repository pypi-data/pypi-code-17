"""
All exceptions raised by the Paparazzo package extend PaparazzoError
"""


class PaparazzoError(Exception):
    """
    Base Papparazzo exception, all other exceptions in this package should extend it
    """

    def __init__(self, *args, **kwargs):
        super(PaparazzoError, self).__init__(*args, **kwargs)

    def __str__(self):
        return super(PaparazzoError, self).__str__()
