"""
Exceptions thrown by filters.
"""


from typing import Optional


class OpenEdxFilterException(Exception):
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

    def __init__(
        self,
        message: str = "",
        redirect_to: str = "",
        status_code: Optional[int] = None,
        **kwargs
    ) -> None:
        """
        Init method for OpenEdxFilterException.

        It's designed to allow flexible instantiation through **kwargs.
        """
        super().__init__()
        self.message = message
        self.redirect_to = redirect_to
        self.status_code = status_code
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        """
        Show string representation of OpenEdxFilterException using its message.
        """
        return self.message
