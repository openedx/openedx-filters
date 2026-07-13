"""
Tests for learning subdomain filters.
"""
from datetime import datetime
from unittest.mock import Mock, patch

# Ignore the type error for ddt import since it is not recognized by mypy.
from ddt import data, ddt, unpack  # type: ignore
from django.test import TestCase
from opaque_keys.edx.keys import CourseKey

from openedx_filters.learning.filters import (
    AccountSettingsReadOnlyFieldsRequested,
    AccountSettingsRenderStarted,
    CertificateCreationRequested,
    CertificateRenderStarted,
    CohortAssignmentRequested,
    CohortChangeRequested,
    CourseAboutPageURLRequested,
    CourseAboutRenderStarted,
    CourseEnrollmentAPIRenderStarted,
    CourseEnrollmentQuerysetRequested,
    CourseEnrollmentStarted,
    CourseEnrollmentViewStarted,
    CourseHomeUrlCreationStarted,
    CourseModePriceRequested,
    CourseRunAPIRenderStarted,
    CourseStartDateValidationFailed,
    CourseUnenrollmentStarted,
    CoursewareAccessChecksRequested,
    CoursewareViewStarted,
    DashboardRenderStarted,
    DiscountEligibilityCheckRequested,
    GradeEventContextRequested,
    IDVPageURLRequested,
    InstructorDashboardRenderStarted,
    InstructorDashboardTabsRequested,
    ORASubmissionViewRenderStarted,
    RenderXBlockStarted,
    ScheduleQuerySetRequested,
    StudentLoginRequested,
    StudentRegistrationRequested,
    VerticalBlockChildRenderStarted,
    VerticalBlockRenderCompleted,
)


@ddt
class TestCertificateFilters(TestCase):
    """
    Test class to verify standard behavior of the certificate filters.
    You'll find test suites for:

    - CertificateCreationRequested
    - CertificateRenderStarted
    """

    def test_certificate_creation_requested(self):
        """
        Test CertificateCreationRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return user, course_key, mode, status, grade and
            generation mode in that order.
        """
        user = Mock()
        course_key = Mock()
        mode = "honor"
        status = "downloadable"
        grade = Mock()
        generation_mode = "self"

        result = CertificateCreationRequested.run_filter(
            user,
            course_key,
            mode,
            status,
            grade,
            generation_mode,
        )

        assert result == (user, course_key, mode, status, grade, generation_mode,)

    def test_certificate_render_started(self):
        """
        Test CertificateRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and custom_template.
        """
        context = {
            "name": "Certificate name",
        }
        template_name = "custom-certificate-template.html"

        result = CertificateRenderStarted.run_filter(context, template_name)

        assert result == (context, template_name,)

    @data(
        (CertificateRenderStarted.RedirectToPage, {"redirect_to": "custom-certificate.pdf"}),
        (CertificateRenderStarted.RenderAlternativeInvalidCertificate, {"template_name": "custom-certificate.html"}),
        (CertificateRenderStarted.RenderCustomResponse, {"response": Mock()}),
        (CertificateCreationRequested.PreventCertificateCreation, {})
    )
    @unpack
    def test_halt_certificate_process(self, CertificateException, attributes):
        """
        Test for certificate exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = CertificateException(message="You can't generate certificate", **attributes)

        assert attributes.items() <= exception.__dict__.items()


@ddt
class TestAuthFilters(TestCase):
    """
    Test class to verify standard behavior of the auth filters.
    You'll find test suites for:

    - StudentRegistrationRequested
    - StudentLoginRequested
    """

    def test_student_registration_requested(self):
        """
        Test StudentRegistrationRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return form data.
        """
        expected_form_data = {
            "password": "sensitive-data",
            "newpassword": "sensitive-data",
            "username": "not-sensitive-data",
        }

        form_data = StudentRegistrationRequested.run_filter(expected_form_data)

        assert expected_form_data == form_data

    @patch(
        "openedx_filters.tooling.OpenEdxPublicFilter.run_pipeline",
        Mock(
            return_value={
                "form_data":
                {
                    "password": "-not-anymore-sensitive-data",
                    "newpassword": "-not-anymore-sensitive-data",
                    "username": "not-sensitive-data",
                }
            }
        )
    )
    def test_student_registration_protected(self):
        """
        Test StudentRegistrationRequested filter behavior when modifying
        sensitive information.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return form data.
        """
        expected_form_data = {
            "password": "sensitive-data",
            "newpassword": "sensitive-data",
            "username": "not-sensitive-data",
        }

        form_data = StudentRegistrationRequested.run_filter(
            {
                "password": "sensitive-data",
                "newpassword": "sensitive-data",
                "username": "not-sensitive-data",
            }
        )

        assert expected_form_data == form_data

    def test_student_login_requested(self):
        """
        Test StudentLoginRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return user.
        """
        expected_user = Mock()

        user = StudentLoginRequested.run_filter(expected_user)

        assert expected_user == user

    @data(
        (
            StudentLoginRequested.PreventLogin,
            {
                "message": "Can't login into this site.",
                "redirect_to": "custom-error-page.com",
                "error_code": 400,
                "context": {
                    "username": "test",
                },
            }
        ),
        (
            StudentRegistrationRequested.PreventRegistration, {"message": "Can't register in this site."}
        ),
    )
    @unpack
    def test_halt_student_auth_process(self, auth_exception, attributes):
        """
        Test for student auth exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = auth_exception(**attributes)

        assert attributes.items() <= exception.__dict__.items()


@ddt
class TestEnrollmentFilters(TestCase):
    """
    Test class to verify standard behavior of the enrollment filters.
    You'll find test suites for:

    - CourseEnrollmentStarted
    - CourseUnenrollmentStarted
    - CourseEnrollmentQuerysetRequested
    - CourseEnrollmentViewStarted
    """

    def test_course_enrollment_started(self):
        """
        Test CourseEnrollmentStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return user, course_key and mode in that order.
        """
        user = Mock()
        course_key = Mock()
        mode = "honor"

        result = CourseEnrollmentStarted.run_filter(user, course_key, mode)

        assert result == (user, course_key, mode,)

    def test_course_unenrollment_started(self):
        """
        Test CourseUnenrollmentStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return enrollment.
        """
        expected_enrollment = Mock()

        enrollment = CourseUnenrollmentStarted.run_filter(expected_enrollment)

        assert expected_enrollment == enrollment

    def test_course_enrollment_view_started(self):
        """
        Test CourseEnrollmentViewStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return user, course_key, and requester_is_backend_service, in that order.
        """
        user = Mock()
        course_key = Mock()
        requester_is_backend_service = True

        result = CourseEnrollmentViewStarted.run_filter(user, course_key, requester_is_backend_service)

        assert result == (user, course_key, requester_is_backend_service)

    @data(
        (CourseEnrollmentStarted.PreventEnrollment, {"message": "Can't enroll into course."}),
        (
            CourseUnenrollmentStarted.PreventUnenrollment, {"message": "Can't un-enroll into course."}
        ),
    )
    @unpack
    def test_halt_enrollment_process(self, enrollment_exception, attributes):
        """
        Test for enrollment/unenrollment exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = enrollment_exception(**attributes)

        assert attributes.items() <= exception.__dict__.items()

    def test_course_enrollments_requested(self):
        """
        Test user course enrollment requested filter.

        Expected behavior:
            - The filter should return the enrollments to orgs.
        """
        expected_enrollments = Mock()

        enrollments = CourseEnrollmentQuerysetRequested.run_filter(expected_enrollments)

        assert expected_enrollments == enrollments

    @data(
        (
            CourseEnrollmentQuerysetRequested.PreventEnrollmentQuerysetRequest,
            {"message": "Can't request QuerySet Enrollment."}
        )
    )
    @unpack
    def test_halt_queryset_request(self, request_exception, attributes):
        """
        Test for queryset request exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = request_exception(**attributes)

        assert attributes.items() <= exception.__dict__.items()

    def test_halt_course_enrollment_view_process(self):
        """
        Test CourseEnrollmentViewStarted.PreventEnrollment exception handling.

        Expected behavior:
            - The exception must carry the message attribute specified.
        """
        test_message = "Enterprise enrollment processing failed"
        exception = CourseEnrollmentViewStarted.PreventEnrollment(message=test_message)
        assert exception.message == test_message


@ddt
class TestRenderingFilters(TestCase):
    """
    Test class to verify standard behavior of the filters located in rendering views.
    You'll find test suites for:

    - CourseAboutRenderStarted
    - DashboardRenderStarted
    - VerticalBlockChildRenderStarted
    - VerticalBlockRenderCompleted
    - AccountSettingsRenderStarted
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.template_name = "custom-template-name.html"
        self.context = {
            "user": Mock(),
        }

    def test_course_about_render_started(self):
        """
        Test CourseAboutRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and template_name in that order.
        """
        result = CourseAboutRenderStarted.run_filter(self.context, self.template_name)

        assert result == (self.context, self.template_name,)

    def test_dashboard_render_started(self):
        """
        Test DashboardRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and template_name in that order.
        """
        result = DashboardRenderStarted.run_filter(self.context, self.template_name)

        assert result == (self.context, self.template_name,)

    @data(
        (DashboardRenderStarted.RedirectToPage, {"redirect_to": "custom-dashboard.html"}),
        (
            DashboardRenderStarted.RenderInvalidDashboard,
            {
                "dashboard_template": "custom-dashboard.html",
                "template_context": {"user": Mock()},
            }
        ),
        (DashboardRenderStarted.RenderCustomResponse, {"response": Mock()}),
    )
    @unpack
    def test_halt_dashboard_render(self, dashboard_exception, attributes):
        """
        Test for dashboard exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = dashboard_exception(message="You can't access the dashboard", **attributes)

        assert attributes.items() <= exception.__dict__.items()

    @data(
        (CourseAboutRenderStarted.RedirectToPage, {"redirect_to": "custom-course-about.html"}),
        (
            CourseAboutRenderStarted.RenderInvalidCourseAbout,
            {
                "course_about_template": "custom-course-about.html",
                "template_context": {"course_id": Mock()},
            }
        ),
        (CourseAboutRenderStarted.RenderCustomResponse, {"response": Mock()}),
    )
    @unpack
    def test_halt_course_about_render(self, course_about_exception, attributes):
        """
        Test for course about exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = course_about_exception(message="You can't access the course about", **attributes)

        assert attributes.items() <= exception.__dict__.items()

    def test_verticalblock_child_render_started(self):
        """
        Test VerticalBlockChildRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return the child block and its context in that order.
        """
        block = Mock("child_block")
        context = {
            "is_mobile_view": False,
            "username": "edx",
            "child_of_vertical": True,
            "bookmarked": False
        }

        result = VerticalBlockChildRenderStarted.run_filter(block, context)

        assert result == (block, context,)

    @data(
        (
            VerticalBlockChildRenderStarted.PreventChildBlockRender,
            {
                "message": "Assessment question not available for Audit students"
            }
        )
    )
    @unpack
    def test_halt_vertical_child_block_render(self, block_render_exception, attributes):
        """
        Test for vertical child block render exception attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = block_render_exception(**attributes)

        assert attributes.items() <= exception.__dict__.items()

    def test_vertical_block_render_completed(self):
        """
        Test VerticalBlockRenderCompleted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter must return a webfragment, the context and view in order.
        """
        block = Mock("VerticalBlock")
        fragment = Mock("webfragment")
        context = {
            "is_mobile_view": False,
            "username": "edx",
            "bookmarked": False
        }
        view = "student_view"

        result = VerticalBlockRenderCompleted.run_filter(block, fragment, context, view)

        assert result == (block, fragment, context, view)

    @data(
        (
            VerticalBlockRenderCompleted.PreventVerticalBlockRender,
            {
                "message": "Assignment units are not available for Audit students"
            }
        )
    )
    @unpack
    def test_halt_vertical_block_render(self, render_exception, attributes):
        """
        Test for vertical child block render exception attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = render_exception(**attributes)

        assert attributes.items() <= exception.__dict__.items()

    def test_xblock_render_started(self):
        """
        Test RenderXBlockStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return the expected values
        """
        context = {
            "foo": False,
            "bar": "baz",
            "buzz": 1337,
        }
        student_view_context = {
            "arbitrary_context": "value",
            "more_arbitrary_context": True
        }

        result = VerticalBlockChildRenderStarted.run_filter(context, student_view_context)

        assert result == (context, student_view_context)

    @data(
        (
            RenderXBlockStarted.PreventXBlockBlockRender,
            {
                "message": "Danger, Will Robinson!"
            }
        )
    )
    @unpack
    def test_halt_xblock_render(self, xblock_render_exception, attributes):
        """
        Test for xblock render exception attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = xblock_render_exception(**attributes)

        assert attributes.items() <= exception.__dict__.items()

    @data(
        (
            RenderXBlockStarted.RenderCustomResponse,
            {
                "message": "Danger, Will Robinson!"
            }
        )
    )
    @unpack
    def test_halt_xblock_render_custom_response(self, xblock_render_exception, attributes):
        """
        Test for xblock render exception attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = xblock_render_exception(**attributes)

        assert attributes.items() <= exception.__dict__.items()

    def test_account_settings_render_started(self):
        """
        Test AccountSettingsRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter should return context.
        """
        context = {
            'duplicate_provider': None,
            'disable_courseware_js': True,
            'show_dashboard_tabs': True
        }

        result, _ = AccountSettingsRenderStarted.run_filter(context=context, template_name=None)

        assert result == context

    @data(
        (AccountSettingsRenderStarted.RedirectToPage, {"redirect_to": "custom_account_settings.html"}),
        (AccountSettingsRenderStarted.RenderInvalidAccountSettings, {}),
        (AccountSettingsRenderStarted.RenderCustomResponse, {"response": Mock()})
    )
    @unpack
    def test_halt_account_rendering_process(self, AccountSettingsException, attributes):
        """
        Test for account settings exceptions attributes.
        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = AccountSettingsException(message="You can't access this page", **attributes)

        assert attributes.items() <= exception.__dict__.items()

    def test_instructor_dashboard_render_started(self):
        """
        Test InstructorDashboardRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and template_name in that order.
        """
        result = InstructorDashboardRenderStarted.run_filter(self.context, self.template_name)

        assert result == (self.context, self.template_name,)

    @data(
        (InstructorDashboardRenderStarted.RedirectToPage, {"redirect_to": "custom-dashboard.html"}),
        (
            InstructorDashboardRenderStarted.RenderInvalidDashboard,
            {
                "instructor_template": "custom-dashboard.html",
                "template_context": {"course": Mock()},
            }
        ),
        (InstructorDashboardRenderStarted.RenderCustomResponse, {"response": Mock()}),
    )
    @unpack
    def test_halt_instructor_dashboard_render(self, dashboard_exception, attributes):
        """
        Test for the instructor dashboard exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = dashboard_exception(message="You can't access the dashboard", **attributes)

        assert attributes.items() <= exception.__dict__.items()

    def test_ora_submission_view_render_started(self):
        """
        Test ORASubmissionViewRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and template_name in that order.
        """
        result = ORASubmissionViewRenderStarted.run_filter(self.context, self.template_name)

        assert result == (self.context, self.template_name,)

    @data(
        (
            ORASubmissionViewRenderStarted.RenderInvalidTemplate,
            {"context": {"course": Mock()}, "template_name": "custom-template.html"},
        ),
    )
    @unpack
    def test_halt_ora_submission_view_render(self, dashboard_exception, attributes):
        """
        Test for the ora submission view exceptions attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = dashboard_exception(message="You can't access the view", **attributes)

        assert attributes.items() <= exception.__dict__.items()


class TestCohortFilters(TestCase):
    """
    Test class to verify standard behavior of the cohort membership filters.
    You'll find test suites for:

    - CohortChangeRequested
    - CohortAssignmentRequested
    """

    def test_cohort_change_requested(self):
        """
        Test CohortChangeRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return current_membership and target_cohort in that order.
        """
        current_membership, target_cohort = Mock(), Mock()

        result = CohortChangeRequested.run_filter(current_membership, target_cohort)

        assert result == (current_membership, target_cohort,)

    def test_cohort_assignment_requested(self):
        """
        Test CohortAssignmentRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return user and target_cohort in that order.
        """
        user, target_cohort = Mock(), Mock()

        result = CohortAssignmentRequested.run_filter(user, target_cohort)

        assert result == (user, target_cohort,)


class TestFederatedContentFilters(TestCase):
    """
    Test class to verify standard behavior of the federated content filters.
    You'll find test suites for:

    - CourseHomeUrlCreationStarted
    """

    def test_course_homeurl_creation_started(self):
        """
        Test CourseHomeUrlCreationStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return course_key and course_home_url in that order.
        """
        course_key, course_home_url = Mock(), Mock()

        result = CourseHomeUrlCreationStarted.run_filter(course_key, course_home_url)

        assert result == (course_key, course_home_url,)

    def test_course_enrollment_api_render_started(self):
        """
        Test CourseEnrollmentAPIRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return course_key and is_started in that order.
        """
        course_key, serialized_enrollment = Mock(), Mock()

        result = CourseEnrollmentAPIRenderStarted.run_filter(course_key, serialized_enrollment)

        assert result == (course_key, serialized_enrollment,)

    def test_course_run_api_render_started(self):
        """
        Test CourseRunAPIRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return serialized_courserun.
        """
        serialized_courserun = Mock()

        result = CourseRunAPIRenderStarted.run_filter(serialized_courserun)

        assert serialized_courserun == result


class TestIDVFilters(TestCase):
    """
    Test class to verify standard behavior of the ID verification filters.
    You'll find test suites for:

    - IDVPageURLRequested
    """

    def test_idv_page_url_requested(self):
        """
        Test IDVPageURLRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return the url.
        """
        url = Mock()

        result = IDVPageURLRequested.run_filter(url)

        assert url == result


class TestCourseAboutPageURLRequested(TestCase):
    """
    Test class to verify standard behavior of the ID verification filters.
    You'll find test suites for:

    - CourseAboutPageURLRequested
    """

    def test_lms_page_url_requested(self):
        """
        Test CourseAboutPageURLRequested filter behavior under normal conditions.
        Expected behavior:
            - The filter should return lms page url requested.
        """
        url = Mock()
        org = Mock()

        url_result, org_result = CourseAboutPageURLRequested.run_filter(url, org)

        assert url == url_result
        assert org == org_result


@ddt
class TestScheduleFilters(TestCase):
    """
    Test class to verify standard behavior of the schedule filters.

    You'll find test suites for:
    - `ScheduleQuerySetRequested`
    """

    def test_schedule_requested(self):
        """
        Test schedule requested filter.

        Expected behavior:
            - The filter should return the filtered schedules.
        """
        schedules = Mock()

        result = ScheduleQuerySetRequested.run_filter(schedules)

        assert schedules == result


class TestGradeEventContextRequestedFilter(TestCase):
    """
    Tests for the GradeEventContextRequested filter.
    """

    def test_run_filter_returns_context_unchanged_when_no_pipeline(self):
        """
        When no pipeline steps are configured, run_filter returns all original inputs unchanged.
        """
        context = {"course_id": "course-v1:org+course+run"}
        user_id = 42
        course_id = "course-v1:org+course+run"

        with patch.object(
            GradeEventContextRequested,
            "run_pipeline",
            return_value={"context": context, "user_id": user_id, "course_id": course_id},
        ):
            result_context, result_user_id, result_course_id = GradeEventContextRequested.run_filter(
                context=context,
                user_id=user_id,
                course_id=course_id,
            )

        assert result_context == context
        assert result_user_id == user_id
        assert result_course_id == course_id

    def test_filter_type(self):
        """
        Confirm the filter type string is correct.
        """
        assert GradeEventContextRequested.filter_type == "org.openedx.learning.grade.context.requested.v1"


class TestAccountSettingsReadOnlyFieldsRequestedFilter(TestCase):
    """
    Tests for the AccountSettingsReadOnlyFieldsRequested filter.
    """

    def test_run_filter_returns_inputs_unchanged_when_no_pipeline(self):
        """
        When no pipeline steps are configured, run_filter returns the original inputs unchanged.
        """
        readonly_fields = {"username"}
        user = Mock()

        result_fields, result_user = AccountSettingsReadOnlyFieldsRequested.run_filter(
            readonly_fields=readonly_fields, user=user
        )

        assert result_fields == readonly_fields
        assert result_user == user

    def test_filter_type(self):
        filter_type = "org.openedx.learning.account.settings.read_only_fields.requested.v1"
        assert AccountSettingsReadOnlyFieldsRequested.filter_type == filter_type


@ddt
class TestInstructorDashboardTabsRequested(TestCase):
    """
    Test class to verify standard behavior of the InstructorDashboardTabsRequested filter.

    You'll find test suites for:
    - InstructorDashboardTabsRequested
    """

    def test_run_filter_returns_unchanged_tabs_when_no_pipeline(self):
        """
        Test InstructorDashboardTabsRequested filter behavior under normal conditions.

        When no pipeline steps are configured, run_filter returns the original tabs unchanged.

        Expected behavior:
            - The filter should return the tabs list unchanged.
        """
        tabs = [
            {"tab_id": "courseware", "title": "Course", "url": "/course/123", "sort_order": 0},
            {"tab_id": "instructor", "title": "Instructor", "url": "/instructor/123", "sort_order": 1},
        ]
        user = Mock()
        course_key = Mock()

        with patch("openedx_filters.tooling.OpenEdxPublicFilter.run_pipeline") as mock_run_pipeline:
            mock_run_pipeline.return_value = {"tabs": tabs, "user": user, "course_key": course_key}
            result_tabs, result_user, result_course_key = InstructorDashboardTabsRequested.run_filter(
                tabs=tabs, user=user, course_key=course_key
            )

        assert result_tabs == tabs
        assert result_user == user
        assert result_course_key == course_key

    def test_filter_type(self):
        """Test that the filter type is properly set."""
        filter_type = "org.openedx.learning.instructor.dashboard.tabs.requested.v1"
        assert InstructorDashboardTabsRequested.filter_type == filter_type

    def test_run_filter_with_pipeline_returning_dict_with_tabs(self):
        """
        Test InstructorDashboardTabsRequested filter when pipeline returns dict with tabs.

        Expected behavior:
            - The filter should return the filtered tabs from the pipeline result.
        """
        tabs = [
            {"tab_id": "courseware", "title": "Course", "url": "/course/123", "sort_order": 0},
        ]
        modified_tabs = [
            {"tab_id": "custom", "title": "Custom Tab", "url": "/custom/123", "sort_order": 0},
        ]
        user = Mock()
        course_key = Mock()

        with patch("openedx_filters.tooling.OpenEdxPublicFilter.run_pipeline") as mock_run_pipeline:
            mock_run_pipeline.return_value = {
                "tabs": modified_tabs, "user": user, "course_key": course_key
            }
            result_tabs, result_user, result_course_key = InstructorDashboardTabsRequested.run_filter(
                tabs=tabs, user=user, course_key=course_key
            )

        assert result_tabs == modified_tabs
        assert result_user == user
        assert result_course_key == course_key

    @data(
        (
            InstructorDashboardTabsRequested.PreventTabsGeneration,
            {
                "message": "Custom tabs provided by plugin",
                "tabs": [{"tab_id": "custom", "title": "Custom", "url": "/custom", "sort_order": 0}],
            }
        ),
        (
            InstructorDashboardTabsRequested.PreventTabsGeneration,
            {
                "message": "Disable tab generation",
            }
        ),
    )
    @unpack
    def test_prevent_tabs_generation_exception(self, exception_class, attributes):
        """
        Test that the PreventTabsGeneration exception can be initialized with required attributes.

        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = exception_class(**attributes)

        assert attributes.items() <= exception.__dict__.items()


class TestCoursewareViewStarted(TestCase):
    """
    Test class to verify standard behavior of the CoursewareViewStarted filter.
    """

    def test_returns_course_key_unchanged_when_no_pipeline_steps(self):
        """
        Test CoursewareViewStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter returns ``course_key`` unchanged when no pipeline steps raise.
        """
        course_key = CourseKey.from_string("course-v1:edX+DemoX+Demo_Course")
        view_name = "test_view"
        result_course_key, result_view_name = CoursewareViewStarted.run_filter(
            course_key=course_key,
            view_name=view_name,
        )
        assert result_course_key == course_key
        assert result_view_name == view_name

    def test_redirect_to_url_stores_url(self):
        """
        Test that RedirectToUrl stores the redirect_to attribute on the exception instance.

        Expected behavior:
            - Instantiating RedirectToUrl sets ``exc.redirect_to`` to the provided value.
        """
        exc = CoursewareViewStarted.RedirectToUrl(message="test message", redirect_to="/some/path/")
        assert exc.message == "test message"
        assert exc.redirect_to == "/some/path/"


class TestCourseStartDateValidationFailed(TestCase):
    """
    Test class to verify standard behavior of the CourseStartDateValidationFailed filter.
    """

    def test_returns_inputs_unchanged_when_no_pipeline_steps(self):
        """
        Test CourseStartDateValidationFailed filter behavior under normal conditions.

        Expected behavior:
            - Each input field is returned unchanged when no pipeline steps raise.
        """
        course_key = CourseKey.from_string("course-v1:edX+DemoX+Demo_Course")
        start_date = datetime(2026, 9, 1)
        result_course_key, result_start_date = CourseStartDateValidationFailed.run_filter(
            course_key=course_key,
            start_date=start_date,
        )
        assert result_course_key == course_key
        assert result_start_date == start_date

    def test_override_start_date_error_stores_fields(self):
        """
        Test that OverrideStartDateError stores all fields on the exception instance.

        Expected behavior:
            - Instantiating OverrideStartDateError sets ``message``, ``error_code``,
              ``developer_message``, and ``user_message`` on the instance.
        """
        exc = CourseStartDateValidationFailed.OverrideStartDateError(
            message="Course has not started (message).",
            error_code="course_not_started",
            developer_message="Course has not started (developer message).",
            user_message="Course has not started (user message).",
        )
        assert exc.message == "Course has not started (message)."
        assert exc.error_code == "course_not_started"
        assert exc.developer_message == "Course has not started (developer message)."
        assert exc.user_message == "Course has not started (user message)."


class TestCoursewareAccessChecksRequested(TestCase):
    """
    Test class to verify standard behavior of the CoursewareAccessChecksRequested filter.
    """

    def test_returns_inputs_unchanged_when_no_pipeline_steps(self):
        """
        Filter passes through user and course_key when no pipeline steps are configured.
        """
        user = Mock()
        course_key = CourseKey.from_string("course-v1:edX+DemoX+Demo_Course")
        result_user, result_course_key = CoursewareAccessChecksRequested.run_filter(
            user=user,
            course_key=course_key,
        )
        assert result_user == user
        assert result_course_key == course_key

    def test_prevent_exception_preserves_kwargs(self):
        """
        PreventCoursewareAccess stores message, error_code, developer_message, and
        user_message as attributes on the exception instance.
        """
        exc = CoursewareAccessChecksRequested.PreventCoursewareAccess(
            message="test message",
            error_code="some_code",
            developer_message="developer message",
            user_message="user message",
        )
        assert exc.message == "test message"
        assert exc.error_code == "some_code"
        assert exc.developer_message == "developer message"
        assert exc.user_message == "user message"


class TestDiscountEligibilityCheckRequestedFilter(TestCase):
    """
    Tests for the DiscountEligibilityCheckRequested filter.
    """

    def test_filter_type(self):
        self.assertEqual(
            DiscountEligibilityCheckRequested.filter_type,
            "org.openedx.learning.discount.eligibility.check.requested.v1",
        )

    def test_run_filter_passes_through_user_and_course_key(self):
        user = Mock()
        course_key = Mock()

        returned_user, returned_course_key = (
            DiscountEligibilityCheckRequested.run_filter(user, course_key)
        )

        assert returned_user == user
        assert returned_course_key == course_key

    def test_run_filter_raises_discount_ineligible_from_pipeline(self):
        user = Mock()
        course_key = Mock()
        exc = DiscountEligibilityCheckRequested.DiscountIneligible("Enterprise contract prohibits discount.")

        with patch(
            "openedx_filters.tooling.OpenEdxPublicFilter.run_pipeline",
            side_effect=exc,
        ):
            with self.assertRaises(DiscountEligibilityCheckRequested.DiscountIneligible):
                DiscountEligibilityCheckRequested.run_filter(user, course_key)

    def test_discount_ineligible_exception_stores_message(self):
        exc = DiscountEligibilityCheckRequested.DiscountIneligible("Enterprise contract prohibits discount.")

        assert exc.message == "Enterprise contract prohibits discount."


class TestCourseModeFilters(TestCase):
    """
    Test class to verify standard behavior of the CourseModePriceRequested filter.
    """

    def test_course_mode_price_requested(self):
        """
        Test CourseModePriceRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return the (possibly discounted) price.
        """
        user = Mock()
        course_mode_data = Mock()
        price = 100
        assert CourseModePriceRequested.filter_type == "org.openedx.learning.course_mode.price.requested.v1"

        result_user, result_course_mode_data, result_price = CourseModePriceRequested.run_filter(
            user, course_mode_data, price
        )

        assert user == result_user
        assert course_mode_data == result_course_mode_data
        assert price == result_price
