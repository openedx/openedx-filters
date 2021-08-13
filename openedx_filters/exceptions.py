"""
Exceptions thrown by filters.
"""


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

    def __init__(self, message="", redirect_to=None, status_code=None, **kwargs):
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

    def __str__(self):
        """
        Show string representation of OpenEdxFilterException using its message.
        """
        return "OpenEdxFilterException: {}".format(self.message)


class InstantiationError(OpenEdxFilterException):
    """
    Describes errors that occur while instantiating filters.

    This exception is raised when there's an error instantiating an Open edX
    filter, it can be that a required argument for the filter definition is
    missing.
    """

    def __init__(self, filter_name="", message=""):
        """
        Init method for InstantiationError custom exception class.

        Arguments:
            filter_name (str): name of the filter raising the exception.
            message (str): message describing why the exception was raised.
        """
        super().__init__(
            message="InstantiationError {filter_name}: {message}".format(
                filter_name=filter_name, message=message
            )
        )


class ExecutionValidationError(OpenEdxFilterException):
    """
    Describes errors that occur while validating arguments of send methods.
    """

    def __init__(self, filter_name="", message=""):
        """
        Init method for ExecutionValidationError custom exception class.

        Arguments:
            filter_name (str): name of the filter raising the exception.
            message (str): message describing why the exception was raised.
        """
        super().__init__(
            message="ExecutionValidationError {filter_name}: {message}".format(
                filter_name=filter_name, message=message
            )
        )
