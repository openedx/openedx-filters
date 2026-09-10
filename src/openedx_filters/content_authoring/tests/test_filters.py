"""
Tests for authoring subdomain filters.
"""
from unittest.mock import Mock

from django.test import TestCase

from openedx_filters.content_authoring.filters import LMSPageURLRequested


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
        url = Mock()
        org = Mock()

        url_result, org_result = LMSPageURLRequested.run_filter(url, org)

        self.assertEqual(url, url_result)
        self.assertEqual(org, org_result)
