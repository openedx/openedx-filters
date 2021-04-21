"""
Tests for custom Hooks Exceptions.
"""
from django.test import TestCase

from ..exceptions import HookException


class TestCustomHookException(TestCase):
    """
    Test class used to check flexibility when using  HookException.
    """

    def test_exception_extra_arguments(self):
        """
        This method raises HookException with custom dynamic arguments.

        Expected behavior:
            Custom parameters can be accessed as instance arguments.
        """
        hook_exception = HookException(custom_arg="custom_argument")

        self.assertEqual(
            hook_exception.custom_arg,  # pylint: disable=no-member
            "custom_argument",
        )
