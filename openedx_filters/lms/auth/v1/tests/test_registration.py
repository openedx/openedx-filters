"""
Tests for filters related to the registration process.

Classes:
    TestBeforeCreation: Test before_creation filter.
"""
from unittest.mock import Mock, patch

from django.test import TestCase

from openedx_filters.lms.auth.v1.registration import before_creation
from openedx_filters.names import PRE_USER_REGISTRATION


class TestBeforeCreation(TestCase):
    """Test cases for registration `before_creation` filter."""

    def setUp(self):
        super().setUp()
        self.data = Mock()
        self.modified_data = Mock()

    @patch("openedx_filters.lms.auth.v1.registration.run_pipeline")
    def test_pipeline_call(self, pipeline_mock):
        """
        This method tests how the pipeline runner call is
        made.

        Expected behavior:
            - The pipeline runner is called with
            PRE_USER_REGISTRATION, *args and **kwargs.
            - The keyword dictionary has as its element the
            required argument.
        """
        before_creation(self.data)

        pipeline_mock.assert_called_once_with(
            PRE_USER_REGISTRATION, data=self.data,
        )

    @patch("openedx_filters.lms.auth.v1.registration.run_pipeline")
    def test_filter_return_arguments(self, pipeline_mock):
        """
        This method tests what the filter returns when called.

        Expected behavior:
            - The filter returns the input argument 'user'
            modified by the pipeline.
        """
        pipeline_mock.return_value = {
            "data": self.modified_data,
        }

        return_values = before_creation(self.data)

        self.assertEqual(self.modified_data, return_values)
