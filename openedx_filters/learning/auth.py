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
        data = super().run_pipeline(form_data=form_data)
        return data.get("form_data")


class PreLoginFilter(OpenEdxPublicFilter):
    """
    Custom class used to create PreLogin filters.
    """

    filter_type = "org.openedx.learning.student.login.requested.v1"

    class PreventLogin(OpenEdxFilterException):
        """
        Custom class used to stop the login process.
        """

    @classmethod
    def run(cls, user):
        """
        Execute a filter with the signature specified.

        Arguments:
            user (User): is a Django User object.
        """
        data = super().run_pipeline(user=user)
        return data.get("user")
