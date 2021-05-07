"""
Tests for filters related to the login process.

Classes:
    TestBeforeCreation: Test before_creation login filter.
"""
from unittest.mock import Mock, patch

from django.test import TestCase

from openedx_filters.lms.auth.v1.login import before_creation
from openedx_filters.names import PRE_USER_LOGIN


class TestBeforeCreation(TestCase):
    """Test cases for auth session `before_creation` filter."""

    def setUp(self):
        super().setUp()
        self.user = Mock()
        self.modified_user = Mock()

    @patch("openedx_filters.lms.auth.v1.login.run_pipeline")
    def test_pipeline_call(self, pipeline_mock):
        """
        This method tests how the pipeline runner call is
        made.

        Expected behavior:
            - The pipeline runner is called with PRE_USER_LOGIN,
            *args and **kwargs.
            - The keyword dictionary has as its element the
            required argument.
        """
        before_creation(self.user)

        pipeline_mock.assert_called_once_with(
            PRE_USER_LOGIN, user=self.user,
        )

    @patch("openedx_filters.lms.auth.v1.login.run_pipeline")
    def test_filter_return_arguments(self, pipeline_mock):
        """
        This method tests what the filter returns when called.

        Expected behavior:
            - The filter returns the input argument "user"
            modified by the pipeline.
        """
        pipeline_mock.return_value = {
            "user": self.modified_user,
        }

        return_values = before_creation(self.user)

        self.assertEqual(self.modified_user, return_values)
