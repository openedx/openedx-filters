"""
Exceptions thrown by filters.
"""


class HookFilterException(Exception):
    """
    Base exception for filters.

    It is re-raised by the Pipeline Runner if any filter that is
    executing raises it.

    Arguments:
        message (str): message describing why the exception was raised.
        redirect_to (str): redirect URL.
        status_code (int): HTTP status code.
        keyword arguments (kwargs): extra arguments used to customize
        exception.
    """

    def __init__(self, message="", redirect_to=None, status_code=None, **kwargs):
        """
        Init method for HookFilterException.

        It's designed to allow flexible instantiation through **kwargs.
        """
        super().__init__()
        self.message = message
        self.redirect_to = redirect_to
        self.status_code = status_code
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """
        Show string representation of HookFilterException using its message.
        """
        return "HookFilterException: {}".format(self.message)
