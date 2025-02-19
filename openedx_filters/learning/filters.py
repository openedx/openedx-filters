"""
Package where filters related to the learning architectural subdomain are implemented.
"""

from typing import Any, Optional

from django.db.models.query import QuerySet
from django.http import HttpResponse, QueryDict
from opaque_keys.edx.keys import CourseKey

from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter
from openedx_filters.utils import SensitiveDataManagementMixin


class AccountSettingsRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the rendering of the account settings page in the LMS.

    Purpose:
        This filter is triggered when a user visits the account settings page, just before the page is rendered allowing
        the filter to modify the context and the template used to render the page.

    Filter Type:
        org.openedx.learning.student.settings.render.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_api/accounts/settings_views.py
        - Function or Method: account_settings

    Additional Information:
        This filter doesn't work alongside the account MFE, only with the legacy account settings page.
    """

    filter_type = "org.openedx.learning.student.settings.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Raise to trigger a redirect before the account settings page is rendered.

        This exception is propagated to the account settings view and handled by the view to redirect the user to
        a new page.

        Attributes:
            message (str): error message for the exception.
            redirect_to (str): URL to redirect to.
        """

        def __init__(self, message: str, redirect_to: str) -> None:
            """
            Initialize the exception with the message and the URL to redirect to.

            Arguments:
                message (str): error message for the exception.
                redirect_to (str): URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderInvalidAccountSettings(OpenEdxFilterException):
        """
        Raise to render a different template instead of the account settings page.

        This exception is propagated to the account settings view and handled by the view to render a different
        template instead.

        Attributes:
            message (str): error message for the exception.
            account_settings_template (str): template path rendered instead.
            template_context (dict): context used to the new account settings template.
        """

        def __init__(
            self,
            message: str,
            account_settings_template: str = "",
            template_context: Optional[dict] = None
        ) -> None:
            """
            Initialize the exception with the message and the template path to render instead.

            Arguments:
                message (str): error message for the exception.
                account_settings_template (str): template path rendered instead.
                template_context (dict): context used to the new account settings template.
            """
            super().__init__(
                message,
                account_settings_template=account_settings_template,
                template_context=template_context,
            )

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Raise to return a custom response instead of the usual account settings page.

        This exception is propagated to the account settings view and handled by the view to return a custom response
        instead.

        Attributes:
            message (str): error message for the exception.
            response (HttpResponse): custom response which will be returned by the account settings view.
        """

        def __init__(self, message: str, response: Optional[HttpResponse] = None) -> None:
            """
            Initialize the exception with the message and the custom response to return.

            Arguments:
                message (str): error message for the exception.
                response (HttpResponse): custom response which will be returned by the account settings view.
            """
            super().__init__(message, response=response)

    @classmethod
    def run_filter(cls, context: dict[str, Any], template_name: str) -> tuple[dict[str, Any] | None, str | None]:
        """
        Process the input context and template_name using the configured pipeline steps to modify the account settings.

        Arguments:
            context (dict): template context for the account settings page.
            template_name (str): template path used to render the account settings page.

        Returns:
            tuple[dict, str]:
                - dict: context dictionary for the account settings page, possibly modified.
                - str: template name to be rendered by the account settings page, possibly modified.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class StudentRegistrationRequested(OpenEdxPublicFilter, SensitiveDataManagementMixin):
    """
    Filter used to modify the registration process of a given user in the LMS.

    Purpose:
        This filter is triggered when a user tries to register, just before the registration process is completed
        allowing the filter to act on the registration form data.

    Filter Type:
        org.openedx.learning.student.registration.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/register.py
        - Function or Method: RegistrationView.post
    """

    filter_type = "org.openedx.learning.student.registration.requested.v1"
    sensitive_form_data = [
        "password",
        "newpassword",
        "new_password",
        "oldpassword",
        "old_password",
        "new_password1",
        "new_password2",
    ]

    class PreventRegistration(OpenEdxFilterException):
        """
        Raise to prevent the registration process to continue.

        This exception is propagated to the registration view and handled by the view to stop the registration process.
        """

    @classmethod
    def run_filter(cls, form_data: QueryDict) -> QueryDict:
        """
        Process the registration form data using the configured pipeline steps to modify the registration process.

        Arguments:
            form_data (QueryDict): contains the request.data submitted by the registration form.

        Returns:
            QueryDict: form data dictionary, possibly modified.
        """
        sensitive_data = cls.extract_sensitive_data(form_data)
        data = super().run_pipeline(form_data=form_data)
        form_data = data.get("form_data", QueryDict())
        form_data.update(sensitive_data)
        return form_data


class StudentLoginRequested(OpenEdxPublicFilter):
    """
    Filter used to modify the login process of a given user in the LMS.

    Purpose:
        This filter is triggered when a user tries to log in, just before the login process is completed allowing the
        filter to act on the user object.

    Filter Type:
        org.openedx.learning.student.login.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/login.py
        - Function or Method: login_user
    """

    filter_type = "org.openedx.learning.student.login.requested.v1"

    class PreventLogin(OpenEdxFilterException):
        """
        Raise to prevent the login process to continue.

        This exception is propagated to the login view and handled by the view to stop the login process.

        Attributes:
            message (str): error message for the exception.
            redirect_to (str): URL to redirect to.
            error_code (str): error code for the exception.
            context (dict): context dictionary to be used in the exception.
        """

        def __init__(
            self,
            message: str,
            redirect_to: str = "",
            error_code: str = "",
            context: Optional[dict] = None
        ) -> None:
            """
            Initialize the exception with the message and the URL to redirect to.

            Arguments:
                message (str): error message for the exception.
                redirect_to (str): URL to redirect to.
                error_code (str): error code for the exception.
                context (dict): context dictionary to be used in the exception.
            """
            super().__init__(message, redirect_to=redirect_to, error_code=error_code, context=context)

    @classmethod
    def run_filter(cls, user: Any) -> Any:
        """
        Process the user object using the configured pipeline steps to modify the login process.

        Arguments:
            user (User): Django User object trying to log in.

        Returns:
            User: Django User object, possibly modified.
        """
        data = super().run_pipeline(user=user)
        return data.get("user")


class CourseEnrollmentStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the enrollment process for a given user in a course.

    Purpose:
        This filter is triggered when a user initiates the enrollment process, just before the enrollment is completed
        allowing the filter to act on the user, course key, and mode.

    Filter Type:
        org.openedx.learning.course.enrollment.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: common/djangoapps/student/models/course_enrollment.py
        - Function or Method: enroll
    """

    filter_type = "org.openedx.learning.course.enrollment.started.v1"

    class PreventEnrollment(OpenEdxFilterException):
        """
        Raise to prevent the enrollment process to continue.

        This exception is propagated to the course enrollment model and handled by the model to stop the enrollment
        process. All components using the enroll method handle this exception in the appropriate way.
        """

    @classmethod
    def run_filter(cls, user: Any, course_key: CourseKey, mode: str) -> tuple[Any, CourseKey | None, str | None]:
        """
        Process the user, course_key, and mode using the configured pipeline steps to modify the enrollment process.

        Arguments:
            user (User): Django User enrolling in the course.
            course_key (CourseKey): course key associated with the enrollment.
            mode (str): specifies what kind of enrollment. The course modes available are: audit, professional,
                verified, honor and professional

        Returns:
            tuple[Any, CourseKey, str]:
                - User: Django User object.
                - CourseKey: course key associated with the enrollment.
                - str: mode of the enrollment.
        """
        data = super().run_pipeline(
            user=user, course_key=course_key, mode=mode,
        )
        return data.get("user"), data.get("course_key"), data.get("mode")


class CourseUnenrollmentStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the unenrollment process for a given user from a course.

    Purpose:
        This filter is triggered when a user initiates the unenrollment process, just before the unenrollment is
        completed allowing the filter to act on the user's enrollment in the course.

    Filter Type:
        org.openedx.learning.course.unenrollment.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: common/djangoapps/student/models/course_enrollment.py
        - Function or Method: unenroll
    """

    filter_type = "org.openedx.learning.course.unenrollment.started.v1"

    class PreventUnenrollment(OpenEdxFilterException):
        """
        Raised to prevent the unenrollment process to continue.

        This exception is propagated to the course enrollment model and handled by the model to stop the unenrollment
        process. All components using the unenroll method handle this exception in the appropriate way.
        """

    @classmethod
    def run_filter(cls, enrollment: Any) -> Any:
        """
        Process the enrollment object using the configured pipeline steps to modify the unenrollment process.

        Arguments:
            enrollment (CourseEnrollment): user's enrollment in the course.

        Returns:
            CourseEnrollment: user's enrollment in the course.
        """
        data = super().run_pipeline(enrollment=enrollment)
        return data.get("enrollment")


class CertificateCreationRequested(OpenEdxPublicFilter):
    """
    Filter used to modify the certificate creation process for a given user in a course.

    Purpose:
        This filter is triggered when a user requests a certificate, just before the certificate is created allowing the
        filter to act on the user, course key, mode, status, grade, and generation mode.

    Filter Type:
        org.openedx.learning.certificate.creation.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: lms/djangoapps/certificates/generated_certificate.py
        - Function or Method: _generate_certificate_task
    """

    filter_type = "org.openedx.learning.certificate.creation.requested.v1"

    class PreventCertificateCreation(OpenEdxFilterException):
        """
        Raise to prevent the certificate creation process to continue.

        This exception is propagated from the certificate generation function and handled by the caller to stop the
        certificate creation process before starting the async task.
        """

    @classmethod
    def run_filter(  # pylint: disable=too-many-positional-arguments
        cls,
        user: Any,
        course_key: CourseKey,
        mode: str,
        status: str,
        grade: float,
        generation_mode: str,
    ) -> tuple[Any, CourseKey | None, str | None, str | None, float | None, str | None]:
        """
        Process the inputs using the configured pipeline steps to modify the certificate creation process.

        Arguments:
            user (User): Django User object.
            course_key (CourseKey): course key associated with the certificate.
            mode (str): specifies what kind of certificate.
            status (str): specifies the status of the certificate.
            grade (float): grade of the certificate.
            generation_mode (str): specifies the mode of generation.

        Returns:
            tuple[User, CourseKey, str, str, float, str]:
                - User: Django User object.
                - CourseKey: course key associated with the certificate.
                - str: mode of the certificate.
                - str: status of the certificate.
                - float: grade of the certificate.
                - str: mode of generation.
        """
        data = super().run_pipeline(
            user=user,
            course_key=course_key,
            mode=mode,
            status=status,
            grade=grade,
            generation_mode=generation_mode,
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
    Filter used to modify the rendering of a certificate.

    Purpose:
        This filter is triggered when a user requests to view the certificate, just before the certificate is rendered
        allowing the filter to act on the context and the template used to render the certificate.

    Filter Type:
        org.openedx.learning.certificate.render.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: lms/djangoapps/certificates/views/webview.py
        - Function or Method: render_html_view
    """

    filter_type = "org.openedx.learning.certificate.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Raise to redirect to a different page instead of rendering the certificate.

        This exception is propagated to the certificate view and handled by the view to redirect the user to a new page.

        Attributes:
            message (str): error message for the exception.
            redirect_to (str): URL to redirect to.
        """

        def __init__(self, message: str, redirect_to: str = "") -> None:
            """
            Initialize the exception with the message and the URL to redirect to.

            Arguments:
                message (str): error message for the exception.
                redirect_to (str): URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderAlternativeInvalidCertificate(OpenEdxFilterException):
        """
        Raise to render a different certificate template instead of the default one.

        This exception is propagated to the certificate view and handled by the view to render a different template
        instead.

        Attributes:
            message (str): error message for the exception.
            template_name (str): template path of the new certificate.
        """

        def __init__(self, message: str, template_name: str = "") -> None:
            """
            Initialize the exception with the message and the template path to render instead.

            Arguments:
                message (str): error message for the exception.
                template_name (str): template path of the new certificate.
            """
            super().__init__(message, template_name=template_name)

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Raise to stop the certificate rendering process and return a custom response.

        This exception is propagated to the certificate view and handled by the view to return a custom response
        instead.

        Attributes:
            message (str): error message for the exception.
            response (HttpResponse): custom response which will be returned by the certificate view.
        """

        def __init__(self, message: str, response: HttpResponse) -> None:
            """
            Initialize the exception with the message and the custom response to return.

            Arguments:
                message (str): error message for the exception.
                response (HttpResponse): custom response which will be returned by the certificate view.
            """
            super().__init__(
                message,
                response=response,
            )

    @classmethod
    def run_filter(cls, context: dict, custom_template: Any) -> tuple[dict[str, Any] | None, Any]:
        """
        Process the context and custom_template using the configured pipeline steps to modify the certificate rendering.

        Arguments:
            context (dict): context dictionary for certificate template.
            custom_template (CertificateTemplate): custom web certificate template.

        Returns:
            tuple[dict, CertificateTemplate]:
                - dict: context dictionary for the certificate template, possibly modified.
                - CertificateTemplate: custom web certificate template, possibly modified.
        """
        data = super().run_pipeline(context=context, custom_template=custom_template)
        return data.get("context"), data.get("custom_template")


class CohortChangeRequested(OpenEdxPublicFilter):
    """
    Filter used to modify the cohort change process.

    Purpose:
        This filter is triggered when a user's cohort is changed, just before the change is completed allowing the
        filter to act on the user and the target cohort.

    Filter Type:
        org.openedx.learning.cohort.change.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/course_groups/models.py
        - Function or Method: assign
    """

    filter_type = "org.openedx.learning.cohort.change.requested.v1"

    class PreventCohortChange(OpenEdxFilterException):
        """
        Raise to prevent the cohort change process to continue.

        This exception is propagated to the assign method and handled by it to stop the cohort change process.
        """

    @classmethod
    def run_filter(cls, current_membership: Any, target_cohort: Any) -> tuple[Any, Any]:
        """
        Process the inputs using the configured pipeline steps to modify the cohort change process.

        Arguments:
            current_membership (CohortMembership): CohortMembership instance representing the current user's cohort.
            target_cohort (CourseUserGroup): CourseUserGroup instance representing the new user's cohort.

        Returns:
            tuple[CohortMembership, CourseUserGroup]:
                - CohortMembership: CohortMembership instance representing the current user's cohort.
                - CourseUserGroup: CourseUserGroup instance representing the new user's cohort.
        """
        data = super().run_pipeline(current_membership=current_membership, target_cohort=target_cohort)
        return data.get("current_membership"), data.get("target_cohort")


class CohortAssignmentRequested(OpenEdxPublicFilter):
    """
    Filter used to modify the cohort assignment process.

    Purpose:
        This filter is triggered when a user is assigned to a cohort, just before the assignment is completed allowing
        the filter to act on the user and the target cohort.

    Filter Type:
        org.openedx.learning.cohort.assignment.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/course_groups/models.py
        - Function or Method: assign
    """

    filter_type = "org.openedx.learning.cohort.assignment.requested.v1"

    class PreventCohortAssignment(OpenEdxFilterException):
        """
        Raise to prevent the cohort assignment process to continue.

        This exception is propagated to the assign method and handled by it to stop the cohort assignment process.

        Attributes:
            message (str): error message for the exception.
            redirect_to (str): URL to redirect to.
        """

    @classmethod
    def run_filter(cls, user: Any, target_cohort: Any) -> tuple[Any, Any]:
        """
        Process the user and target_cohort using the configured pipeline steps to modify the cohort assignment process.

        Arguments:
            user (User): Django User object representing the user.
            target_cohort (CourseUserGroup): CourseUserGroup instance representing the new user's cohort.

        Returns:
            tuple[User, CourseUserGroup]:
                - User: Django User object representing the user.
                - CourseUserGroup: CourseUserGroup instance representing the new user's cohort.
        """
        data = super().run_pipeline(user=user, target_cohort=target_cohort)
        return data.get("user"), data.get("target_cohort")


class CourseAboutRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the course about rendering process.

    Purpose:
        This filter is triggered when a user requests to view the course about page, just before the page is rendered
        allowing the filter to act on the context and the template used to render the page.

    Filter Type:
        org.openedx.learning.course_about.render.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: lms/djangoapps/courseware/views/views.py
        - Function or Method: course_about
    """

    filter_type = "org.openedx.learning.course_about.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Raise to redirect to a different page instead of rendering the course about.

        This exception is propagated to the course about view and handled by the view to redirect the user to a new
        page.

        Attributes:
            message (str): error message for the exception.
            redirect_to (str): URL to redirect to.
        """

        def __init__(self, message: str, redirect_to: str = "") -> None:
            """
            Initialize the exception with the message and the URL to redirect to.

            Arguments:
                message (str): error message for the exception.
                redirect_to (str): URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderInvalidCourseAbout(OpenEdxFilterException):
        """
        Raise to render a different course about template instead of the default one.

        This exception is propagated to the course about view and handled by the view to render a different template
        instead.

        Attributes:
            message (str): error message for the exception.
            course_about_template (str): template path rendered instead.
            template_context (dict): context used to the new course_about_template.
        """

        def __init__(
            self,
            message: str,
            course_about_template: str = "",
            template_context: Optional[dict] = None
        ) -> None:
            """
            Initialize the exception with the message and the template to render instead.

            Arguments:
                message (str): error message for the exception.
                course_about_template (str): template path rendered instead.
                template_context (dict): context used to the new course_about_template.
            """
            super().__init__(
                message,
                course_about_template=course_about_template,
                template_context=template_context,
            )

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Raise to stop the course about rendering process and return a custom response.

        This exception is propagated to the course about view and handled by the view to return a custom response
        instead.
        """

        def __init__(self, message: str, response: HttpResponse) -> None:
            """
            Initialize the exception with the message and the custom response to return.

            Arguments:
                message (str): error message for the exception.
                response (HttpResponse): custom response which will be returned by the course about view.
            """
            super().__init__(
                message,
                response=response,
            )

    @classmethod
    def run_filter(cls, context: dict[str, Any], template_name: str) -> tuple[dict[str, Any] | None, str | None]:
        """
        Process the context and template_name using the configured pipeline steps to modify the course about rendering.

        Arguments:
            context (dict): context dictionary for course about template.
            template_name (str): template name to be rendered by the course about.

        Returns:
            tuple[dict, str]:
                - dict: context dictionary for the course about template, possibly modified.
                - str: template name to be rendered by the course about, possibly modified.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class DashboardRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the dashboard rendering process.

    Purpose:
        This filter is triggered when a user requests to view the dashboard, just before the page is rendered allowing
        the filter to act on the context and the template used to render the page.

    Filter Type:
        org.openedx.learning.dashboard.render.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: common/djangoapps/student/views/dashboard.py
        - Function or Method: student_dashboard

    Additional Information:
        This filter doesn't work alongside the dashboard MFE, only with the legacy student dashboard.
    """

    filter_type = "org.openedx.learning.dashboard.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Raise to redirect to a different page instead of rendering the dashboard.

        This exception is propagated to the dashboard view and handled by the view to redirect the user to a new page.

        Attributes:
            message (str): error message for the exception.
            redirect_to (str): URL to redirect to.
        """

        def __init__(self, message: str, redirect_to: str = "") -> None:
            """
            Initialize the exception with the message and the URL to redirect to.

            Arguments:
                message (str): error message for the exception.
                redirect_to (str): URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderInvalidDashboard(OpenEdxFilterException):
        """
        Raise to render a different dashboard template instead of the default one.

        This exception is propagated to the dashboard view and handled by the view to render a different template
        instead.

        Attributes:
            message (str): error message for the exception.
            dashboard_template (str): template path rendered instead.
            template_context (dict): context used to the new dashboard_template.
        """

        def __init__(
            self,
            message: str,
            dashboard_template: str = "",
            template_context: Optional[dict] = None
        ) -> None:
            """
            Initialize the exception with the message and the template to render instead.

            Arguments:
                message (str): error message for the exception.
                dashboard_template (str): template path rendered instead.
                template_context (dict): context used to the new dashboard_template.
            """
            super().__init__(
                message,
                dashboard_template=dashboard_template,
                template_context=template_context,
            )

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Raise to stop the dashboard rendering process and return a custom response.

        This exception is propagated to the dashboard view and handled by the view to return a custom response instead.

        Attributes:
            message (str): error message for the exception.
            response (HttpResponse): custom response which will be returned by the dashboard view.
        """

        def __init__(self, message: str, response: Optional[HttpResponse] = None) -> None:
            """
            Initialize the exception with the message and the custom response to return.

            Arguments:
                message (str): error message for the exception.
                response (HttpResponse): custom response which will be returned by the dashboard view.
            """
            super().__init__(
                message,
                response=response,
            )

    @classmethod
    def run_filter(cls, context: dict[str, Any], template_name: str) -> tuple[dict[str, Any] | None, str | None]:
        """
        Process the context and template_name using the configured pipeline steps to modify the dashboard rendering.

        Arguments:
            context (dict): context dictionary for student's dashboard template.
            template_name (str): template name to be rendered by the student's dashboard.

        Returns:
            tuple[dict, str]:
                - dict: context dictionary for the student's dashboard template, possibly modified.
                - str: template name to be rendered by the student's dashboard, possibly modified.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class VerticalBlockChildRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the rendering of a child block within a vertical block.

    Purpose:
        This filter is triggered when a child block is about to be rendered within a vertical block, allowing the filter
        to act on the block and the context used to render the child block.

    Filter Type:
        org.openedx.learning.vertical_block_child.render.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: xmodule/vertical_block.py
        - Function or Method: VerticalBlock._student_or_public_view
    """

    filter_type = "org.openedx.learning.vertical_block_child.render.started.v1"

    class PreventChildBlockRender(OpenEdxFilterException):
        """
        Raise to prevent a child block from rendering.

        This exception is propagated to the vertical block view and handled by the view to stop the rendering of the
        child block.
        """

    @classmethod
    def run_filter(cls, block: Any, context: dict[str, Any]) -> tuple[Any, dict[str, Any] | None]:
        """
        Process the block and context using the configured pipeline steps to modify the rendering of a child block.

        Arguments:
            block (XBlock): the XBlock that is about to be rendered into HTML
            context (dict): rendering context values like is_mobile_app, show_title..etc

        Returns:
            tuple[XBlock, dict]:
                - XBlock: the XBlock that is about to be rendered into HTML
                - dict: rendering context values like is_mobile_app, show_title..etc
        """
        data = super().run_pipeline(block=block, context=context)
        return data.get("block"), data.get("context")


class CourseEnrollmentQuerysetRequested(OpenEdxPublicFilter):
    """
    Filter used to modify the QuerySet of course enrollments.

    Purpose:
        This filter is triggered when a QuerySet of course enrollments is requested, allowing the filter to act on the
        enrollments data.

    Filter Type:
        org.openedx.learning.course_enrollment_queryset.requested.v1

    Trigger: NA

    Additional Information:
        This filter is not currently triggered by any specific function or method in any codebase. It should be
        marked to be removed if it's not used. See openedx-filters#245 for more information.
    """

    filter_type = "org.openedx.learning.course_enrollment_queryset.requested.v1"

    class PreventEnrollmentQuerysetRequest(OpenEdxFilterException):
        """
        Raise to prevent the course enrollment queryset request to continue.
        """

    @classmethod
    def run_filter(cls, enrollments: QuerySet) -> QuerySet | None:
        """
        Process the enrollments QuerySet using the configured pipeline steps to modify the course enrollment data.

        Arguments:
            enrollments (QuerySet): data with all user's course enrollments.

        Returns:
            QuerySet: data with all user's course enrollments, possibly modified.
        """
        data = super().run_pipeline(enrollments=enrollments)
        return data.get("enrollments")


class RenderXBlockStarted(OpenEdxPublicFilter):
    """
    Filter in between context generation and rendering of XBlock scope.

    Purpose:
        This filter is triggered when an XBlock is about to be rendered, just before the rendering process is completed
        allowing the filter to act on the context and student_view_context used to render the XBlock.

    Filter Type:
        org.openedx.learning.xblock.render.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: lms/djangoapps/courseware/views/views.py
        - Function or Method: render_xblock
    """

    filter_type = "org.openedx.learning.xblock.render.started.v1"

    class PreventXBlockBlockRender(OpenEdxFilterException):
        """
        Raise to prevent the XBlock from rendering for the user.

        This exception is propagated to the XBlock render view and handled by the view to stop the rendering of the
        XBlock.
        """

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Raise to stop the XBlock rendering process by returning a custom response.

        This exception is propagated to the XBlock render view and handled by the view to return a custom response
        instead.

        Attributes:
            message (str): error message for the exception.
            response (HttpResponse): custom response which will be returned by the XBlock render view.
        """

        def __init__(self, message: str, response: Optional[HttpResponse] = None):
            """
            Initialize the exception with the message and the custom response to return.

            Arguments:
                message (str): error message for the exception.
                response (HttpResponse): custom response which will be returned by the XBlock render view.
            """
            super().__init__(message, response=response)

    @classmethod
    def run_filter(
        cls,
        context: dict[str, Any],
        student_view_context: dict
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        """
        Process the inputs using the configured pipeline steps to modify the rendering of an XBlock.

        Arguments:
            context (dict): rendering context values like is_mobile_app, show_title, etc.
            student_view_context (dict): context passed to the student_view of the block context.

        Returns:
            tuple[dict, dict]:
                - dict: rendering context values like is_mobile_app, show_title, etc.
                - dict: context passed to the student_view of the block context.
        """
        data = super().run_pipeline(context=context, student_view_context=student_view_context)
        return data.get("context"), data.get("student_view_context")


class VerticalBlockRenderCompleted(OpenEdxPublicFilter):
    """
    Filter used to act on vertical block rendering completed.

    Purpose:
        This filter is triggered when a vertical block is rendered, just after the rendering process is completed
        allowing the filter to act on the block, fragment, context, and view used to render the vertical block.

    Filter Type:
        org.openedx.learning.vertical_block.render.completed.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: xmodule/vertical_block.py
        - Function or Method: VerticalBlock._student_or_public_view
    """

    filter_type = "org.openedx.learning.vertical_block.render.completed.v1"

    class PreventVerticalBlockRender(OpenEdxFilterException):
        """
        Raise to prevent the vertical block from rendering for the user.

        This exception is propagated to the vertical block view and handled by the view to stop the rendering of the
        vertical block.
        """

    @classmethod
    def run_filter(
        cls,
        block: Any,
        fragment: Any,
        context: dict[str, Any],
        view: str
    ) -> tuple[Any, Any, dict[str, Any] | None, str | None]:
        """
        Process the inputs using the configured pipeline steps to modify the rendering of a vertical block.

        Arguments:
            block (VerticalBlock): The VeriticalBlock instance which is being rendered.
            fragment (web_fragments.Fragment): The web-fragment containing the rendered content of VerticalBlock.
            context (dict): rendering context values like is_mobile_app, show_title..etc.
            view (str): the rendering view. Can be either 'student_view', or 'public_view'.

        Returns:
            tuple[VeticalBlock, web_fragments.Fragment, dict, str]:
                - VerticalBlock: The VeriticalBlock instance which is being rendered.
                - web_fragments.Fragment: The web-fragment containing the rendered content of VerticalBlock.
                - dict: rendering context values like is_mobile_app, show_title..etc.
                - str: the rendering view. Can be either 'student_view', or 'public_view'.
        """
        data = super().run_pipeline(block=block, fragment=fragment, context=context, view=view)
        return data.get("block"), data.get("fragment"), data.get("context"), data.get("view")


class CourseHomeUrlCreationStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the course home url creation process.

    Purpose:
        This filter is triggered when a course home url is being generated, just before the generation process is
        completed allowing the filter to act on the course key and course home url.

    Filter Type:
        org.openedx.learning.course.homepage.url.creation.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/features/course_experience/__init__.py
        - Function or Method: course_home_url
    """

    filter_type = "org.openedx.learning.course.homepage.url.creation.started.v1"

    @classmethod
    def run_filter(cls, course_key: CourseKey, course_home_url: str) -> tuple[CourseKey | None, str | None]:
        """
        Process the course_key and course_home_url using the configured pipeline steps to modify the course home url.

        Arguments:
            course_key (CourseKey): The course key for which the home url is being requested.
            course_home_url (str): The url string for the course home.

        Returns:
            tuple[CourseKey, str]:
                - CourseKey: The course key for which the home url is being requested.
                - str: The url string for the course home.
        """
        data = super().run_pipeline(course_key=course_key, course_home_url=course_home_url)
        return data.get("course_key"), data.get("course_home_url")


class CourseEnrollmentAPIRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the course enrollment API rendering process.

    Purpose:
        This filter is triggered when a user requests to view the course enrollment API, just before the API is rendered
        allowing the filter to act on the course key and serialized enrollment data.

    Filter Type:
        org.openedx.learning.home.enrollment.api.rendered.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: lms/djangoapps/learner_home/serializers.py
        - Function or Method: EnrollmentSerializer.to_representation
    """

    filter_type = "org.openedx.learning.home.enrollment.api.rendered.v1"

    @classmethod
    def run_filter(
        cls,
        course_key: CourseKey,
        serialized_enrollment: dict[str, Any]
    ) -> tuple[CourseKey | None, dict[str, Any] | None]:
        """
        Process the inputs using the configured pipeline steps to modify the course enrollment data.

        Arguments:
            course_key (CourseKey): The course key for which isStarted is being modify.
            serialized_enrollment (dict): enrollment data.

        Returns:
            tuple[CourseKey, dict]:
                - CourseKey: The course key for which isStarted is being modify.
                - dict: enrollment data.
        """
        data = super().run_pipeline(course_key=course_key, serialized_enrollment=serialized_enrollment)
        return data.get("course_key"), data.get("serialized_enrollment")


class CourseRunAPIRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the course run API rendering process.

    Purpose:
        This filter is triggered when a user requests to view the course run API, just before the API is rendered
        allowing the filter to act on the serialized course run data.

    Filter Type:
        org.openedx.learning.home.courserun.api.rendered.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: lms/djangoapps/learner_home/serializers.py
        - Function or Method: CourseRunSerializer.to_representation
    """

    filter_type = "org.openedx.learning.home.courserun.api.rendered.started.v1"

    @classmethod
    def run_filter(cls, serialized_courserun: dict[str, Any]) -> dict[str, Any] | None:
        """
        Process the serialized_courserun using the configured pipeline steps to modify the course run data.

        Arguments:
            serialized_courserun (dict): courserun data.

        Returns:
            dict: courserun data.
        """
        data = super().run_pipeline(serialized_courserun=serialized_courserun)
        return data.get("serialized_courserun")


class InstructorDashboardRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the instructor dashboard rendering process.

    Purpose:
        This filter is triggered when an instructor requests to view the dashboard, just before the page is rendered
        allowing the filter to act on the context and the template used to render the page.

    Filter Type:
        org.openedx.learning.instructor.dashboard.render.started.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: lms/djangoapps/instructor/views/instructor_dashboard.py
        - Function or Method: instructor_dashboard_2
    """

    filter_type = "org.openedx.learning.instructor.dashboard.render.started.v1"

    class RedirectToPage(OpenEdxFilterException):
        """
        Raise to redirect to a different page instead of rendering the instructor dashboard.

        This exception is propagated to the instructor dashboard view and handled by the view to redirect the user to a
        new page.

        Attributes:
            message (str): error message for the exception.
            redirect_to (str): URL to redirect to.
        """

        def __init__(self, message: str, redirect_to: str = ""):
            """
            Initialize the exception with the message and the URL to redirect to.

            Arguments:
                message (str): error message for the exception.
                redirect_to (str): URL to redirect to.
            """
            super().__init__(message, redirect_to=redirect_to)

    class RenderInvalidDashboard(OpenEdxFilterException):
        """
        Raise to render a different instructor dashboard template instead of the default one.

        This exception is propagated to the instructor dashboard view and handled by the view to render a different
        template instead.

        Attributes:
            message (str): error message for the exception.
            instructor_template (str): template path rendered instead.
            template_context (dict): context used to the new instructor_template
        """

        def __init__(
            self,
            message: str,
            instructor_template: str = "",
            template_context: Optional[dict] = None
        ):
            """
            Initialize the exception with the message and the template to render instead.

            Arguments:
                message (str): error message for the exception.
                instructor_template (str): template path rendered instead.
                template_context (dict): context used to the new instructor_template.
            """
            super().__init__(
                message,
                instructor_template=instructor_template,
                template_context=template_context,
            )

    class RenderCustomResponse(OpenEdxFilterException):
        """
        Raise to stop the instructor dashboard rendering process and return a custom response.

        This exception is propagated to the instructor dashboard view and handled by the view to return a custom
        response instead.

        Attributes:
            message (str): error message for the exception.
            response (HttpResponse): custom response which will be returned by the dashboard view.
        """

        def __init__(self, message: str, response: Optional[HttpResponse] = None):
            """
            Initialize the exception with the message and the custom response to return.

            Arguments:
                message (str): error message for the exception.
                response (HttpResponse): custom response which will be returned by the dashboard view.
            """
            super().__init__(
                message,
                response=response,
            )

    @classmethod
    def run_filter(cls, context: dict[str, Any], template_name: str) -> tuple[dict[str, Any] | None, str | None]:
        """
        Process the context and template_name using the configured pipeline steps to modify the instructor dashboard.

        Arguments:
            context (dict): context dictionary for instructor's tab template.
            template_name (str): template name to be rendered by the instructor's tab.

        Returns:
            tuple[dict, str]:
                - dict: context dictionary for the instructor's tab template, possibly modified.
                - str: template name to be rendered by the instructor's tab, possibly modified.
        """
        data = super().run_pipeline(context=context, template_name=template_name)
        return data.get("context"), data.get("template_name")


class ORASubmissionViewRenderStarted(OpenEdxPublicFilter):
    """
    Filter used to modify the submission view rendering process.

    Purpose:
        This filter is triggered when a user requests to view the submission, just before the page is rendered allowing
        the filter to act on the context and the template used to render the page.

    Filter Type:
        org.openedx.learning.ora.submission_view.render.started.v1

    Trigger:
        - Repository: openedx/edx-ora2
        - Path: openassessment/xblock/ui_mixins/legacy/views/submission.py
        - Function or Method: render_submission
    """

    filter_type = "org.openedx.learning.ora.submission_view.render.started.v1"

    class RenderInvalidTemplate(OpenEdxFilterException):
        """
        Raise to render a different submission view template instead of the default one.

        This exception is propagated to the submission view and handled by the view to render a different template
        instead.

        Arguments:
            message (str): error message for the exception.
            context (dict): context used to the submission view template.
            template_name (str): template path rendered instead.
        """

        def __init__(
            self, message: str,
            context: Optional[dict] = None,
            template_name: str = ""
        ) -> None:
            """Initialize the exception with the message and the template to render instead."""
            super().__init__(message, context=context, template_name=template_name)

    @classmethod
    def run_filter(cls, context: dict[str, Any], template_name: str) -> tuple[dict[str, Any] | None, str | None]:
        """
        Process the context and template_name using the configured pipeline steps to modify the submission view.

        Arguments:
            context (dict): context dictionary for submission view template.
            template_name (str): template name to be rendered by the student's dashboard.

        Returns:
            tuple[dict, str]:
                - dict: context dictionary for the submission view template, possibly modified.
                - str: template name to be rendered by the submission view, possibly modified.
        """
        data = super().run_pipeline(context=context, template_name=template_name, )
        return data.get("context"), data.get("template_name")


class IDVPageURLRequested(OpenEdxPublicFilter):
    """
    Filter used to act on ID verification page URL requests.

    Purpose:
        This filter is triggered when a user requests to view the ID verification page, just before the page is rendered
        allowing the filter to act on the URL of the page.

    Filter Type:
        org.openedx.learning.idv.page.url.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: lms/djangoapps/verify_student/services.py
        - Function or Method: XBlockVerificationService.get_verify_location
    """

    filter_type = "org.openedx.learning.idv.page.url.requested.v1"

    @classmethod
    def run_filter(cls, url: str) -> str | None:
        """
        Process the URL using the configured pipeline steps to modify the ID verification page URL.

        Arguments:
            url (str): The url for the ID verification page to be modified.

        Returns:
            str: The modified URL for the ID verification page.
        """
        data = super().run_pipeline(url=url)
        return data.get("url")


class CourseAboutPageURLRequested(OpenEdxPublicFilter):
    """
    Filter used to act on course about page URL requests.

    Purpose:
        This filter is triggered when a user requests to view the course about page, just before the page is rendered
        allowing the filter to act on the URL of the page and the course org.

    Filter Type:
        org.openedx.learning.course_about.page.url.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: common/djangoapps/util/course.py
        - Function or Method: get_link_for_about_page
    """

    filter_type = "org.openedx.learning.course_about.page.url.requested.v1"

    @classmethod
    def run_filter(cls, url: str, org: str) -> tuple[str | None, str | None]:
        """
        Process the URL and org using the configured pipeline steps to modify the course about page URL.

        Arguments:
            url (str): the URL of the page to be modified.
            org (str): Course org filter used as context data to get LMS configurations.

        Returns:
            tuple[str, str]:
                - str: the modified URL of the page.
                - str: Course org filter used as context data to get LMS configurations.
        """
        data = super().run_pipeline(url=url, org=org)
        return data.get("url"), data.get("org")


class ScheduleQuerySetRequested(OpenEdxPublicFilter):
    """
    Filter used to apply additional filtering to a given QuerySet of Schedules.

    Purpose:
        This filter is triggered when a QuerySet of Schedules is requested, allowing the filter to act on the schedules
        data. If you want to know more about the Schedules feature, please refer to the official documentation:
            - https://github.com/openedx/edx-platform/tree/master/openedx/core/djangoapps/schedules#readme

    Filter Type:
        org.openedx.learning.schedule.queryset.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/schedules/resolvers.py
        - Function or Method: BinnedSchedulesBaseResolver.get_schedules_with_target_date_by_bin_and_orgs
    """

    filter_type = "org.openedx.learning.schedule.queryset.requested.v1"

    @classmethod
    def run_filter(cls, schedules: QuerySet) -> QuerySet | None:
        """
        Process the schedules QuerySet using the configured pipeline steps to modify the schedules data.

        Arguments:
            schedules (QuerySet): The original QuerySet of schedules to be filtered.

        Returns:
            QuerySet: A refined QuerySet of schedules after applying the filter.
        """
        data = super().run_pipeline(schedules=schedules)
        return data.get("schedules")
