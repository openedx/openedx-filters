"""
Tests for authoring subdomain filters.
"""
from unittest.mock import Mock

from django.test import TestCase

from openedx_filters.course_authoring.filters import LMSPageURLRequested


class TestCourseAuthoringFilters(TestCase):
    """
    Test class to verify standard behavior of the filters located in rendering views.
    You'll find test suites for:

    - LMSPageURLRequested
    """

    def test_lms_page_url_requested(self):
        """
        Test LMSPageURLRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return lms page url requested.
        """
        target_url = Mock()
        org = Mock()

        result = LMSPageURLRequested.run_filter(target_url, org)

        self.assertEqual((target_url, org), result)
