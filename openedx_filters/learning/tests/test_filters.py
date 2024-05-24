"""
Tests for learning subdomain filters.
"""
from unittest.mock import Mock, patch

from ddt import data, ddt, unpack
from django.test import TestCase

from openedx_filters.learning.filters import (
    AccountSettingsRenderStarted,
    CertificateCreationRequested,
    CertificateRenderStarted,
    CohortAssignmentRequested,
    CohortChangeRequested,
    CourseAboutRenderStarted,
    CourseEnrollmentAPIRenderStarted,
    CourseEnrollmentQuerysetRequested,
    CourseEnrollmentStarted,
    CourseHomeUrlCreationStarted,
    CourseRunAPIRenderStarted,
    CourseUnenrollmentStarted,
    DashboardRenderStarted,
    InstructorDashboardRenderStarted,
    ORASubmissionViewRenderStarted,
    RenderXBlockStarted,
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

        self.assertTupleEqual(
            (user, course_key, mode, status, grade, generation_mode,),
            result,
        )

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

        self.assertTupleEqual((context, template_name,), result)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)


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

        self.assertEqual(expected_form_data, form_data)

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

        self.assertEqual(expected_form_data, form_data)

    def test_student_login_requested(self):
        """
        Test StudentLoginRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return user.
        """
        expected_user = Mock()

        user = StudentLoginRequested.run_filter(expected_user)

        self.assertEqual(expected_user, user)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)


@ddt
class TestEnrollmentFilters(TestCase):
    """
    Test class to verify standard behavior of the enrollment filters.
    You'll find test suites for:

    - CourseEnrollmentStarted
    - CourseUnenrollmentStarted
    - CourseEnrollmentQuerysetRequested
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

        self.assertTupleEqual((user, course_key, mode,), result)

    def test_course_unenrollment_started(self):
        """
        Test CourseUnenrollmentStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return enrollment.
        """
        expected_enrollment = Mock()

        enrollment = CourseUnenrollmentStarted.run_filter(expected_enrollment)

        self.assertEqual(expected_enrollment, enrollment)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)

    def test_course_enrollments_requested(self):
        """
        Test user course enrollment requested filter.

        Expected behavior:
            - The filter should return the enrollments to orgs.
        """
        expected_enrollments = Mock()

        enrollments = CourseEnrollmentQuerysetRequested.run_filter(expected_enrollments)

        self.assertEqual(expected_enrollments, enrollments)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)


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

        self.assertTupleEqual((self.context, self.template_name,), result)

    def test_dashboard_render_started(self):
        """
        Test DashboardRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and template_name in that order.
        """
        result = DashboardRenderStarted.run_filter(self.context, self.template_name)

        self.assertTupleEqual((self.context, self.template_name,), result)

    @data(
        (DashboardRenderStarted.RedirectToPage, {"redirect_to": "custom-dashboard.html"}),
        (
            DashboardRenderStarted.RenderInvalidDashboard,
            {
                "dashboard_template": "custom-dasboard.html",
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

        self.assertDictContainsSubset(attributes, exception.__dict__)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)

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
            "child_of_veritcal": True,
            "bookmarked": False
        }

        result = VerticalBlockChildRenderStarted.run_filter(block, context)

        self.assertTupleEqual((block, context,), result)

    @data(
        (
            VerticalBlockChildRenderStarted.PreventChildBlockRender,
            {
                "message": "Assessement question not available for Audit students"
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

        self.assertDictContainsSubset(attributes, exception.__dict__)

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

        self.assertTupleEqual((block, fragment, context, view), result)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)

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

        self.assertTupleEqual((context, student_view_context), result)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)

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

        self.assertEqual(result, context)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)

    def test_instructor_dashboard_render_started(self):
        """
        Test InstructorDashboardRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and template_name in that order.
        """
        result = InstructorDashboardRenderStarted.run_filter(self.context, self.template_name)

        self.assertTupleEqual((self.context, self.template_name,), result)

    @data(
        (InstructorDashboardRenderStarted.RedirectToPage, {"redirect_to": "custom-dashboard.html"}),
        (
            InstructorDashboardRenderStarted.RenderInvalidDashboard,
            {
                "instructor_template": "custom-dasboard.html",
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

        self.assertDictContainsSubset(attributes, exception.__dict__)

    def test_ora_submission_view_render_started(self):
        """
        Test ORASubmissionViewRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and template_name in that order.
        """
        result = ORASubmissionViewRenderStarted.run_filter(self.context, self.template_name)

        self.assertTupleEqual((self.context, self.template_name,), result)

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

        self.assertDictContainsSubset(attributes, exception.__dict__)


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

        self.assertTupleEqual((current_membership, target_cohort,), result)

    def test_cohort_assignment_requested(self):
        """
        Test CohortAssignmentRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return user and target_cohort in that order.
        """
        user, target_cohort = Mock(), Mock()

        result = CohortAssignmentRequested.run_filter(user, target_cohort)

        self.assertTupleEqual((user, target_cohort,), result)


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

        self.assertTupleEqual((course_key, course_home_url,), result)

    def test_course_enrollment_api_render_started(self):
        """
        Test CourseEnrollmentAPIRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return course_key and is_started in that order.
        """
        course_key, serialized_enrollment = Mock(), Mock()

        result = CourseEnrollmentAPIRenderStarted.run_filter(course_key, serialized_enrollment)

        self.assertTupleEqual((course_key, serialized_enrollment,), result)

    def test_course_run_api_render_started(self):
        """
        Test CourseRunAPIRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return serialized_courserun.
        """
        serialized_courserun = Mock()

        result = CourseRunAPIRenderStarted.run_filter(serialized_courserun)

        self.assertEqual(serialized_courserun, result)
