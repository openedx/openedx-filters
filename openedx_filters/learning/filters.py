"""
Package where filters related to the learning architectural subdomain are implemented.
"""
from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter
from openedx_filters.utils import SensitiveDataManagementMixin


class StudentRegistrationRequested(OpenEdxPublicFilter, SensitiveDataManagementMixin):
    """
    Custom class used to create PreRegister filters.
    """

    filter_type = "org.openedx.learning.student.registration.requested.v1"
    sensitive_form_data = [
        "password", "newpassword", "new_password", "oldpassword", "old_password", "new_password1", "new_password2",
    ]

    class PreventRegistration(OpenEdxFilterException):
        """
        Custom class used to stop the registration process.
        """

    @classmethod
    def run_filter(cls, form_data):
        """
        Execute a filter with the signature specified.

        Arguments:
            form_data (QueryDict): contains the request.data submitted by the registration
            form.
        """
        sensitive_data = cls.extract_sensitive_data(form_data)
        data = super().run_pipeline(form_data=form_data)
        form_data = data.get("form_data")
        form_data.update(sensitive_data)
        return form_data


class StudentLoginRequested(OpenEdxPublicFilter):
    """
    Custom class used to create PreLogin filters.
    """

    filter_type = "org.openedx.learning.student.login.requested.v1"

    class PreventLogin(OpenEdxFilterException):
        """
        Custom class used to stop the login process.
        """

        def __init__(self, message, redirect_to=None, error_code="", context=None):
            """
            Override init that defines specific arguments used in the login process.
            """
            super().__init__(message, redirect_to=redirect_to, error_code=error_code, context=context)

    @classmethod
    def run_filter(cls, user):
        """
        Execute a filter with the signature specified.

        Arguments:
            user (User): is a Django User object.
        """
        data = super().run_pipeline(user=user)
        return data.get("user")


class CourseEnrollmentStarted(OpenEdxPublicFilter):
    """
    Custom class used to create PreEnrollment filters.
    """

    filter_type = "org.openedx.learning.course.enrollment.started.v1"

    class PreventEnrollment(OpenEdxFilterException):
        """
        Custom class used to stop the enrollment process.
        """

    @classmethod
    def run_filter(cls, user, course_key, mode):
        """
        Execute a filter with the signature specified.

        Arguments:
            user (User): is a Django User object.
            course_key (CourseKey): name of the filter.
            mode (str): is a string specifying what kind of enrollment.
        """
        data = super().run_pipeline(
            user=user, course_key=course_key, mode=mode,
        )
        return data.get("user"), data.get("course_key"), data.get("mode")
