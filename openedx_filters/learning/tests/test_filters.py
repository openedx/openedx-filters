"""
Tests for learning subdomain filters.
"""
from unittest.mock import Mock, patch

from django.test import TestCase

from openedx_filters.learning.filters import (
    CertificateCreationRequested,
    CertificateRenderStarted,
    CohortChangeRequested,
    CourseAboutRenderStarted,
    CourseEnrollmentStarted,
    CourseHomeRenderStarted,
    CourseUnenrollmentStarted,
    DashboardRenderStarted,
    StudentLoginRequested,
    StudentRegistrationRequested,
)


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


class TestEnrollmentFilters(TestCase):
    """
    Test class to verify standard behavior of the enrollment filters.
    You'll find test suites for:

    - CourseEnrollmentStarted
    - CourseUnenrollmentStarted
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


class TestRenderingFilters(TestCase):
    """
    Test class to verify standard behavior of the filters located in rendering views.
    You'll find test suites for:

    - CourseHomeRenderStarted
    - CourseAboutRenderStarted
    - DashboardRenderStarted
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

    def test_course_home_render_started(self):
        """
        Test CourseHomeRenderStarted filter behavior under normal conditions.

        Expected behavior:
            - The filter must have the signature specified.
            - The filter should return context and template_name in that order.
        """
        result = CourseHomeRenderStarted.run_filter(self.context, self.template_name)

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


class TestCohortFilters(TestCase):
    """
    Test class to verify standard behavior of the cohort membership filters.
    You'll find test suites for:

    - CohortChangeRequested
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
