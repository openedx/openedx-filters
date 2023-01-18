"""
Tests for learning subdomain filters.
"""
from unittest.mock import Mock, patch

from ddt import data, ddt, unpack
from django.test import TestCase

from openedx_filters.learning.filters import (
    CertificateCreationRequested,
    CertificateRenderStarted,
    CohortAssignmentRequested,
    CohortChangeRequested,
    CourseAboutRenderStarted,
    CourseEnrollmentQuerysetRequested,
    CourseEnrollmentStarted,
    CourseUnenrollmentStarted,
    DashboardRenderStarted,
    StudentLoginRequested,
    StudentRegistrationRequested,
    VerticalBlockChildRenderStarted,
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
