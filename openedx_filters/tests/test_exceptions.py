"""
Tests for custom Hooks Exceptions.
"""
from django.test import TestCase

from openedx_filters.exceptions import HookFilterException


class TestCustomHookFilterException(TestCase):
    """
    Test class used to check flexibility when using  HookFilterException.
    """

    def test_exception_extra_arguments(self):
        """
        This method raises HookFilterException with custom dynamic arguments.

        Expected behavior:
            Custom parameters can be accessed as instance arguments.
        """
        hook_exception = HookFilterException(custom_arg="custom_argument")

        self.assertEqual(
            hook_exception.custom_arg, "custom_argument",  # pylint: disable=no-member
        )
