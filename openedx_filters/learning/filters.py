"""
Package where filters related to the learning architectural subdomain are implemented.
"""
from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter
from openedx_filters.utils import SensitiveDataManagementMixin


class StudentRegistrationRequested(OpenEdxPublicFilter, SensitiveDataManagementMixin):
    """
    Custom class used to create registration filters and its custom methods.
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
    Custom class used to create login filters and its custom methods.
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
    Custom class used to create enrollment filters and its custom methods.
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
            course_key (CourseKey): course key associated with the enrollment.
            mode (str): is a string specifying what kind of enrollment.
        """
        data = super().run_pipeline(
            user=user, course_key=course_key, mode=mode,
        )
        return data.get("user"), data.get("course_key"), data.get("mode")


class CourseUnenrollmentStarted(OpenEdxPublicFilter):
    """
    Custom class used to create unenrollment filters and its custom methods.
    """

    filter_type = "org.openedx.learning.course.unenrollment.started.v1"

    class PreventUnenrollment(OpenEdxFilterException):
        """
        Custom class used to stop the unenrollment process.
        """

    @classmethod
    def run_filter(cls, enrollment):
        """
        Execute a filter with the signature specified.

        Arguments:
            enrollment (CourseEnrollment): edxapp object representing course enrollments.
        """
        data = super().run_pipeline(enrollment=enrollment)
        return data.get("enrollment")


class CertificateCreationRequested(OpenEdxPublicFilter):
    """
    Custom class used to create certificate creation filters and its custom methods.
    """

    filter_type = "org.openedx.learning.certificate.creation.requested.v1"

    class PreventCertificateCreation(OpenEdxFilterException):
        """
        Custom class used to stop the certificate creation process.
        """

    @classmethod
    def run_filter(cls, user, course_id, mode, status):
        """
        Execute a filter with the signature specified.

        Arguments:
            user (User): is a Django User object.
            course_id (CourseKey): course key associated with the certificate.
            mode (str): mode of the certificate.
            status (str): status of the certificate.
        """
        data = super().run_pipeline(
            user=user, course_id=course_id, mode=mode, status=status,
        )
        return data.get("user"), data.get("course_id"), data.get("mode"), data.get("status")


class CertificateRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create certificate render filters and its custom methods.
    """

    filter_type = "org.openedx.learning.certificate.render.started.v1"

    class PreventCertificateRender(OpenEdxFilterException):
        """
        Custom class used to stop the certificate rendering process.
        """

    @classmethod
    def run_filter(cls, context, custom_template):
        """
        Execute a filter with the signature specified.

        Arguments:
            context (dict): context dictionary for certificate template.
            custom_template (CertificateTemplate): edxapp object representing custom web
            certificate template.
        """
        data = super().run_pipeline(context=context, custom_template=custom_template)
        return data.get("context"), data.get("custom_template")


class CohortChangeRequested(OpenEdxPublicFilter):
    """
    Custom class used to create cohort change filters and its custom methods.
    """

    filter_type = "org.openedx.learning.cohort.change.requested.v1"

    class PreventCohortChange(OpenEdxFilterException):
        """
        Custom class used to stop the cohort change process.
        """

    @classmethod
    def run_filter(cls, current_membership, target_cohort):
        """
        Execute a filter with the signature specified.

        Arguments:
            current_membership (CohortMembership): edxapp object representing the user's cohort
            current membership object.
            target_cohort (CourseUserGroup): edxapp object representing the new user's cohort.
        """
        data = super().run_pipeline(current_membership=current_membership, target_cohort=target_cohort)
        return data.get("current_membership"), data.get("target_cohort")


class CourseAboutRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create course about render filters and its custom methods.
    """

    filter_type = "org.openedx.learning.course_about.render.started.v1"

    class PreventCourseAboutRender(OpenEdxFilterException):
        """
        Custom class used to stop the course about rendering process.
        """

        def __init__(self, message, redirect_to=None):
            """
            Override init that defines specific arguments used in the course about render process.
            """
            super().__init__(message, redirect_to=redirect_to)

    @classmethod
    def run_filter(cls, context, template_name):
        """
        Execute a filter with the signature specified.

        Arguments:
            context (dict): context dictionary for course about template.
            template_name (str): certificate name to be rendered by the course about.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class CourseHomeRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create course home render filters and its custom methods.
    """

    filter_type = "org.openedx.learning.course_home.render.started.v1"

    class PreventCourseHomeRender(OpenEdxFilterException):
        """
        Custom class used to stop the course home render process.
        """

        def __init__(self, message, redirect_to=None):
            """
            Override init that defines specific arguments used in the course home render process.
            """
            super().__init__(message, redirect_to=redirect_to)

    @classmethod
    def run_filter(cls, context, template_name):
        """
        Execute a filter with the signature specified.

        Arguments:
            context (dict): context dictionary for course home template.
            template_name (str): certificate name to be rendered by the course home.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class DashboardRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create dashboard render filters and its custom methods.
    """

    filter_type = "org.openedx.learning.dashboard.render.started.v1"

    class PreventDashboardRender(OpenEdxFilterException):
        """
        Custom class used to stop the dashboard render process.
        """

        def __init__(self, message, redirect_to=None):
            """
            Override init that defines specific arguments used in the dashboard render process.
            """
            super().__init__(message, redirect_to=redirect_to)

    @classmethod
    def run_filter(cls, context, template_name):
        """
        Execute a filter with the signature specified.

        Arguments:
            context (dict): context dictionary for student's dashboard template.
            template_name (str): certificate name to be rendered by the student's dashboard.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")
