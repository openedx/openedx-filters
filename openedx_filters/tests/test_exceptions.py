"""
Tests for custom filter hooks Exceptions.
"""
from django.test import TestCase

from openedx_filters.exceptions import OpenEdxFilterException


class TestCustomOpenEdxFilterException(TestCase):
    """
    Test class used to check flexibility when using  OpenEdxFilterException.
    """

    def test_exception_extra_arguments(self):
        """
        This method raises OpenEdxFilterException with custom dynamic arguments.

        Expected behavior:
            Custom parameters can be accessed as instance arguments.
        """
        filter_exception = OpenEdxFilterException(custom_arg="custom_argument")

        self.assertEqual(
            filter_exception.custom_arg, "custom_argument",  # pylint: disable=no-member
        )
