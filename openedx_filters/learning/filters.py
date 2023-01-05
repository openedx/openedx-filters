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
    def run_filter(cls, user, course_key, mode, status, grade, generation_mode):
        """
        Execute a filter with the signature specified.

        Arguments:
            user (User): is a Django User object.
            course_key (CourseKey): course key associated with the certificate.
            mode (str): mode of the certificate.
            status (str): status of the certificate.
            grade (CourseGrade): user's grade in this course run.
            generation_mode (str): Options are "self" (implying the user generated the cert themself) and "batch"
            for everything else.
        """
        data = super().run_pipeline(
            user=user, course_key=course_key, mode=mode, status=status, grade=grade, generation_mode=generation_mode,
        )
        return (
            data.get("user"),
            data.get("course_key"),
            data.get("mode"),
            data.get("status"),
            data.get("grade"),
            data.get("generation_mode"),
        )


class CertificateRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create certificate render filters and its custom methods.
    """

    filter_type = "org.openedx.learning.certificate.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Custom class used to stop the certificate rendering process.
        """

        def __init__(self, message, redirect_to=""):
            """
            Override init that defines specific arguments used in the certificate render process.

            Arguments:
                message: error message for the exception.
                redirect_to: URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderAlternativeInvalidCertificate(OpenEdxFilterException):
        """
        Custom class used to stop the certificate rendering process.
        """

        def __init__(self, message, template_name=""):
            """
            Override init that defines specific arguments used in the certificate render process.

            Arguments:
                message: error message for the exception.
                template_name: template path of the new certificate.
            """
            super().__init__(message, template_name=template_name)

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Custom class used to stop the certificate rendering process.
        """

        def __init__(self, message, response=None):
            """
            Override init that defines specific arguments used in the certificate render process.

            Arguments:
                message: error message for the exception.
                response: custom response which will be returned by the certificate view.
            """
            super().__init__(
                message,
                response=response,
            )

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


class CohortAssignmentRequested(OpenEdxPublicFilter):
    """
    Custom class used to create cohort assignment filters and its custom methods.
    """

    filter_type = "org.openedx.learning.cohort.assignment.requested.v1"

    class PreventCohortAssignment(OpenEdxFilterException):
        """
        Custom class used to stop the cohort assignment process.
        """

    @classmethod
    def run_filter(cls, user, target_cohort):
        """
        Execute a filter with the signature specified.

        Arguments:
            user (User): is a Django User object to be added in the cohort.
            target_cohort (CourseUserGroup): edxapp object representing the new user's cohort.
        """
        data = super().run_pipeline(user=user, target_cohort=target_cohort)
        return data.get("user"), data.get("target_cohort")


class CourseAboutRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create course about render filters and its custom methods.
    """

    filter_type = "org.openedx.learning.course_about.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Custom class used to stop the course about rendering process.
        """

        def __init__(self, message, redirect_to=""):
            """
            Override init that defines specific arguments used in the course about render process.

            Arguments:
                message: error message for the exception.
                redirect_to: URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderInvalidCourseAbout(OpenEdxFilterException):
        """
        Custom class used to stop the course about rendering process.
        """

        def __init__(self, message, course_about_template="", template_context=None):
            """
            Override init that defines specific arguments used in the course about render process.

            Arguments:
                message: error message for the exception.
                course_about_template: template path rendered instead.
                template_context: context used to the new course_about_template.
            """
            super().__init__(
                message,
                course_about_template=course_about_template,
                template_context=template_context,
            )

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Custom class used to stop the course about rendering process.
        """

        def __init__(self, message, response=None):
            """
            Override init that defines specific arguments used in the course about render process.

            Arguments:
                message: error message for the exception.
                response: custom response which will be returned by the course about view.
            """
            super().__init__(
                message,
                response=response,
            )

    @classmethod
    def run_filter(cls, context, template_name):
        """
        Execute a filter with the signature specified.

        Arguments:
            context (dict): context dictionary for course about template.
            template_name (str): template name to be rendered by the course about.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class DashboardRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create dashboard render filters and its custom methods.
    """

    filter_type = "org.openedx.learning.dashboard.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Custom class used to stop the dashboard rendering process.
        """

        def __init__(self, message, redirect_to=""):
            """
            Override init that defines specific arguments used in the dashboard render process.

            Arguments:
                message: error message for the exception.
                redirect_to: URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderInvalidDashboard(OpenEdxFilterException):
        """
        Custom class used to stop the dashboard render process.
        """

        def __init__(self, message, dashboard_template="", template_context=None):
            """
            Override init that defines specific arguments used in the dashboard render process.

            Arguments:
                message: error message for the exception.
                dashboard_template: template path rendered instead.
                template_context: context used to the new dashboard_template.
            """
            super().__init__(
                message,
                dashboard_template=dashboard_template,
                template_context=template_context,
            )

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Custom class used to stop the dashboard rendering process.
        """

        def __init__(self, message, response=None):
            """
            Override init that defines specific arguments used in the dashboard render process.

            Arguments:
                message: error message for the exception.
                response: custom response which will be returned by the dashboard view.
            """
            super().__init__(
                message,
                response=response,
            )

    @classmethod
    def run_filter(cls, context, template_name):
        """
        Execute a filter with the signature specified.

        Arguments:
            context (dict): context dictionary for student's dashboard template.
            template_name (str): template name to be rendered by the student's dashboard.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class VerticalBlockChildRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create vertical block children's render filters.
    """

    filter_type = "org.openedx.learning.vertical_block_child.render.started.v1"

    @classmethod
    def run_filter(cls, block, context):
        """
        Execute a filter with the signature specified.

        Arguments:
            block (XBlock): the XBlock that is about to be rendered into HTML
            context (dict): rendering context values like is_mobile_app, show_title..etc
        """
        data = super().run_pipeline(block=block, context=context)
        return data.get("block"), data.get("context")


class CourseEnrollmentQuerysetRequested(OpenEdxPublicFilter):
    """
    Custom class used to create course enrollments queryset filters and its custom methods.
    """

    filter_type = "org.openedx.learning.course_enrollment_queryset.requested.v1"

    class PreventEnrollmentQuerysetRequest(OpenEdxFilterException):
        """
        Custom class used to stop the course enrollment queryset request process.
        """

    @classmethod
    def run_filter(cls, enrollments):
        """
        Execute a filter with the signature specified.

        Arguments:
        enrollments (QuerySet): data with all user's course enrollments
        """
        data = super().run_pipeline(enrollments=enrollments)
        return data.get("enrollments")
