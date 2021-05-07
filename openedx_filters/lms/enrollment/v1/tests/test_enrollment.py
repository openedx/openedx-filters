"""
Tests for filters related to the enrollment process.

Classes:
    TestBeforeCreation: Test before_creation filter.
    TestBeforeDeactivation: Test before_deactivation filter.
"""
from unittest.mock import Mock, patch

from django.test import TestCase

from openedx_filters.lms.enrollment.v1.enrollment import before_creation, before_deactivation
from openedx_filters.names import PRE_ENROLLMENT_CREATION, PRE_ENROLLMENT_DEACTIVATION


class TestBeforeCreation(TestCase):
    """Test cases for enrollment `before_creation` filter."""

    def setUp(self):
        super().setUp()
        self.user = Mock()
        self.course_key = Mock()
        self.modified_user = Mock()
        self.modified_course_key = Mock()

    @patch("openedx_filters.lms.enrollment.v1.enrollment.run_pipeline")
    def test_pipeline_call(self, pipeline_mock):
        """
        This method tests how the pipeline runner call is
        made.

        Expected behavior:
            - The pipeline runner is called with
            PRE_ENROLLMENT_CREATION, *args and **kwargs.
            - The keyword dictionary has as its element the
            required argument.
        """
        before_creation(self.user, self.course_key)

        pipeline_mock.assert_called_once_with(
            PRE_ENROLLMENT_CREATION, user=self.user, course_key=self.course_key
        )

    @patch("openedx_filters.lms.enrollment.v1.enrollment.run_pipeline")
    def test_filter_return_arguments(self, pipeline_mock):
        """
        This method tests what the filter returns when called.

        Expected behavior:
            - The filter returns the input argument 'user' and
            'course_key' modified by the pipeline.
        """
        pipeline_mock.return_value = {
            "user": self.modified_user,
            "course_key": self.modified_course_key,
        }

        return_values = before_creation(self.user, self.course_key)

        self.assertTupleEqual(
            (self.modified_user, self.modified_course_key,), return_values
        )


class TestBeforeDeactivation(TestCase):
    """Test cases for enrollment `before_deactivation` filter."""

    def setUp(self):
        super().setUp()
        self.enrollment = Mock()
        self.enrollment_modified = Mock()

    @patch("openedx_filters.lms.enrollment.v1.enrollment.run_pipeline")
    def test_pipeline_call(self, pipeline_mock):
        """
        This method tests how the pipeline runner call is
        made.

        Expected behavior:
            - The pipeline runner is called with
            PRE_ENROLLMENT_DEACTIVATION, *args and **kwargs.
            - The keyword dictionary has as its element the
            required argument.
        """
        before_deactivation(self.enrollment)

        pipeline_mock.assert_called_once_with(
            PRE_ENROLLMENT_DEACTIVATION, enrollment=self.enrollment,
        )

    @patch("openedx_filters.lms.enrollment.v1.enrollment.run_pipeline")
    def test_filter_return_arguments(self, pipeline_mock):
        """
        This method tests what the filter returns when called.

        Expected behavior:
            - The filter returns the input argument 'enrollment'
            modified by the pipeline.
        """
        pipeline_mock.return_value = {
            "enrollment": self.enrollment_modified,
        }

        return_values = before_deactivation(self.enrollment)

        self.assertEqual(self.enrollment_modified, return_values)
