"""
Tests for content authoring subdomain filters.
"""
from unittest.mock import Mock

from ddt import data, ddt, unpack
from django.test import TestCase

from openedx_filters.content_authoring.filters import LmsUrlCreationStarted


@ddt
class TestRenderingFilters(TestCase):
    """
    Test class to verify standard behavior of the filters located in rendering views.
    You'll find test suites for:

    - LmsUrlCreationStarted
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

    def test_lms_url_creation_started(self):
        """
        Test LmsUrlCreationStarted filter behavior under normal conditions.
        Expected behavior:
            - The filter should return lms url creation context.
        """
        context = Mock()
        org = Mock()
        val_name = Mock()
        default = Mock()

        result = LmsUrlCreationStarted.run_filter(context, org, val_name, default)
        print(result)

        self.assertEqual(context, result)

    @data(
        (
            LmsUrlCreationStarted.PreventLmsUrlCreationRender,
            {
                "message": "Can't render lms url creation."
            }
        )
    )
    @unpack
    def test_halt_lms_url_creation(self, lms_url_creation_exception, attributes):
        """
        Test for lms url creation exceptions attributes.
        Expected behavior:
            - The exception must have the attributes specified.
        """
        exception = lms_url_creation_exception(**attributes)

        self.assertDictContainsSubset(attributes, exception.__dict__)
