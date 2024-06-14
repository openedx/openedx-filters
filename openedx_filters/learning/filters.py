"""
Package where filters related to the learning architectural subdomain are implemented.
"""

from typing import Optional

from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter
from openedx_filters.utils import SensitiveDataManagementMixin


class AccountSettingsRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create Account settings filters.
    """

    filter_type = "org.openedx.learning.student.settings.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Custom class used to redirect before the account settings rendering process.
        """

        def __init__(self, message, redirect_to=""):
            """
            Override init that defines specific arguments used in the account settings render process.

            Arguments:
                message: error message for the exception.
                redirect_to: URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderInvalidAccountSettings(OpenEdxFilterException):
        """
        Custom class used to stop the account settings rendering process.
        """

        def __init__(self, message, account_settings_template="", template_context=None):
            """
            Override init that defines specific arguments used in the account settings render process.

            Arguments:
                message: error message for the exception.
                account_settings_template: template path rendered instead.
                template_context: context used to the new account settings template.
            """
            super().__init__(
                message,
                account_settings_template=account_settings_template,
                template_context=template_context,
            )

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Custom class used to stop the account settings rendering process and return a custom response.
        """

        def __init__(self, message, response=None):
            """
            Override init that defines specific arguments used in the account settings render process.

            Arguments:
                message: error message for the exception.
                response: custom response which will be returned by the account settings view.
            """
            super().__init__(message, response=response)

    @classmethod
    def run_filter(cls, context, template_name):
        """
        Execute a filter with the signature specified.

        Arguments:
            context (dict): template context for the account settings page.
            template_name (str): template path used to render the account settings page.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


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

    class PreventChildBlockRender(OpenEdxFilterException):
        """
        Custom class used to stop a particular child block from being rendered.
        """

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


class RenderXBlockStarted(OpenEdxPublicFilter):
    """
    Filter in between context generation and rendering of XBlock scope.
    """

    filter_type = "org.openedx.learning.xblock.render.started.v1"

    class PreventXBlockBlockRender(OpenEdxFilterException):
        """
        Custom class used to prevent the XBlock from rendering for the user.
        """

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Custom class used to stop the XBlock rendering process and return a custom response.
        """

        def __init__(self, message, response=None):
            """
            Override init that defines specific arguments used in the XBlock render process.

            Arguments:
                message: error message for the exception.
                response: custom response which will be returned by the XBlock render view.
            """
            super().__init__(message, response=response)

    @classmethod
    def run_filter(cls, context, student_view_context):
        """
        Execute a filter with the specified signature.

        Arguments:
            context (dict): rendering context values like is_mobile_app, show_title, etc.
            student_view_context (dict): context passed to the student_view of the block context
        """
        data = super().run_pipeline(context=context, student_view_context=student_view_context)
        return data.get("context"), data.get("student_view_context")


class VerticalBlockRenderCompleted(OpenEdxPublicFilter):
    """
    Custom class used to create filters to act on vertical block rendering completed.
    """

    filter_type = "org.openedx.learning.vertical_block.render.completed.v1"

    class PreventVerticalBlockRender(OpenEdxFilterException):
        """
        Custom class used to prevent the vertical block from rendering for the user.
        """

    @classmethod
    def run_filter(cls, block, fragment, context, view):
        """
        Execute a filter with the specified signature.

        Arguments:
            block (VerticalBlock): The VeriticalBlock instance which is being rendered
            fragment (web_fragments.Fragment): The web-fragment containing the rendered content of VerticalBlock
            context (dict): rendering context values like is_mobile_app, show_title..etc.,
            view (str): the rendering view. Can be either 'student_view', or 'public_view'
        """
        data = super().run_pipeline(block=block, fragment=fragment, context=context, view=view)
        return data.get("block"), data.get("fragment"), data.get("context"), data.get("view")


class CourseHomeUrlCreationStarted(OpenEdxPublicFilter):
    """
    Custom class used to create filters to act on course home url creation.
    """

    filter_type = "org.openedx.learning.course.homepage.url.creation.started.v1"

    @classmethod
    def run_filter(cls, course_key, course_home_url):
        """
        Execute a filter with the specified signature.

        Arguments:
            course_key (CourseKey): The course key for which the home url is being requested.
            course_home_url (String): The url string for the course home
        """
        data = super().run_pipeline(course_key=course_key, course_home_url=course_home_url)
        return data.get("course_key"), data.get("course_home_url")


class CourseEnrollmentAPIRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create filters for enrollment data.
    """

    filter_type = "org.openedx.learning.home.enrollment.api.rendered.v1"

    @classmethod
    def run_filter(cls, course_key, serialized_enrollment):
        """
        Execute a filter with the specified signature.

        Arguments:
            course_key (CourseKey): The course key for which isStarted is being modify.
            serialized_enrollment (dict): enrollment data
        """
        data = super().run_pipeline(course_key=course_key, serialized_enrollment=serialized_enrollment)
        return data.get("course_key"), data.get("serialized_enrollment")


class CourseRunAPIRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create filters for course run data.
    """

    filter_type = "org.openedx.learning.home.courserun.api.rendered.started.v1"

    @classmethod
    def run_filter(cls, serialized_courserun):
        """
        Execute a filter with the specified signature.

        Arguments:
            serialized_courserun (dict): courserun data
        """
        data = super().run_pipeline(serialized_courserun=serialized_courserun)
        return data.get("serialized_courserun")


class InstructorDashboardRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create instructor dashboard filters and its custom methods.
    """

    filter_type = "org.openedx.learning.instructor.dashboard.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Custom class used to stop the instructor dashboard render by redirecting to a new page.
        """

        def __init__(self, message, redirect_to=""):
            """
            Override init that defines specific arguments used in the instructor dashboard render process.

            Arguments:
                message: error message for the exception.
                redirect_to: URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderInvalidDashboard(OpenEdxFilterException):
        """
        Custom class used to render a custom template instead of the instructor dashboard.
        """

        def __init__(self, message, instructor_template="", template_context=None):
            """
            Override init that defines specific arguments used in the instructor dashboard render process.

            Arguments:
                message: error message for the exception.
                instructor_template: template path rendered instead.
                template_context: context used to the new instructor_template.
            """
            super().__init__(
                message,
                instructor_template=instructor_template,
                template_context=template_context,
            )

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Custom class used to stop the instructor dashboard rendering by returning a custom response.
        """

        def __init__(self, message, response=None):
            """
            Override init that defines specific arguments used in the instructor dashboard render process.

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
            context (dict): context dictionary for instructor's tab template.
            template_name (str): template name to be rendered by the instructor's tab.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class ORASubmissionViewRenderStarted(OpenEdxPublicFilter):
    """
    Custom class used to create ORA submission view filters and its custom methods.
    """

    filter_type = "org.openedx.learning.ora.submission_view.render.started.v1"

    class RenderInvalidTemplate(OpenEdxFilterException):
        """
        Custom class used to stop the submission view render process.
        """

        def __init__(self, message: str, context: Optional[dict] = None, template_name: str = ""):
            """
            Override init that defines specific arguments used in the submission view render process.

            Arguments:
                message (str): error message for the exception.
                context (dict): context used to the submission view template.
                template_name (str): template path rendered instead.
            """
            super().__init__(message, context=context, template_name=template_name)

    @classmethod
    def run_filter(cls, context: dict, template_name: str):
        """
        Execute a filter with the signature specified.

        Arguments:
            context (dict): context dictionary for submission view template.
            template_name (str): template name to be rendered by the student's dashboard.
        """
        data = super().run_pipeline(context=context, template_name=template_name, )
        return data.get("context"), data.get("template_name")
