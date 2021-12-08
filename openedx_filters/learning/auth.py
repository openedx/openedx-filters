"""
Package where filters related to the auth process are implemented.
"""
from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter


class PreRegisterFilter(OpenEdxPublicFilter):
    """
    Custom class used to create PreRegister filters.
    """

    filter_type = "org.openedx.learning.student.registration.requested.v1"
    sensitive_form_data = [
        "password",
    ]

    class PreventRegister(OpenEdxFilterException):
        """
        Custom class used to stop the registration process.
        """

    @classmethod
    def run(cls, form_data):
        """
        Execute a filter with the signature specified.

        Arguments:
            form_data (QueryDict): contains the request.data submitted by the registration
            form.
        """
        sensitive_data = cls.remove_sensitive_form_data(form_data)
        data = super().run_pipeline(form_data=form_data)
        form_data = data.get("form_data")
        form_data.update(sensitive_data)
        return form_data

    @classmethod
    def remove_sensitive_form_data(cls, form_data):
        """
        Extract sensitive data from PreRegisterFilter input arguments.

        Example usage:

            >> form_data = {"username": "example", "password": "password"}
            >> sensitive_data = PreRegisterFilter.remove_sensitive_form_data(form_data)
            >> sensitive_data
            {"password": "password"}
            >> form_data
            {"username": "example"}
        """
        sensitive_data = {}
        base_form_data = form_data.copy()
        for key, value in base_form_data.items():
            if key in cls.sensitive_form_data:
                form_data.pop(key)
                sensitive_data[key] = value

        return sensitive_data


class PreLoginFilter(OpenEdxPublicFilter):
    """
    Custom class used to create PreLogin filters.
    """

    filter_type = "org.openedx.learning.student.login.requested.v1"

    class PreventLogin(OpenEdxFilterException):
        """
        Custom class used to stop the login process.
        """

        def __init__(self, message, redirect_to=None, error_code="", context=None):
            super().__init__(message, redirect_to=redirect_to, error_code=error_code, context=context)

    @classmethod
    def run(cls, user):
        """
        Execute a filter with the signature specified.

        Arguments:
            user (User): is a Django User object.
        """
        data = super().run_pipeline(user=user)
        return data.get("user")
